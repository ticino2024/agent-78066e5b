"""Social Media Analytics AI Agent using LangChain."""

from typing import Dict, Any, Optional, List
import asyncio
from datetime import datetime

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, AIMessage, SystemMessage

from app.core.config import settings
from app.core.logging import get_logger
from app.tools.analytics_tools import create_analytics_tools

logger = get_logger(__name__)


class SocialMediaAgent:
    """Social Media Analytics AI Agent."""

    def __init__(self, session_id: str, user_id: Optional[int] = None):
        """Initialize the agent."""
        self.session_id = session_id
        self.user_id = user_id
        self.logger = logger
        
        # Initialize LLM based on provider
        self.llm = self._initialize_llm()
        
        # Create tools
        self.tools = create_analytics_tools()
        
        # Initialize memory
        self.memory = ConversationBufferWindowMemory(
            k=settings.CONVERSATION_MEMORY_SIZE,
            memory_key="chat_history",
            return_messages=True,
            output_key="output",
        )
        
        # Create prompt template
        self.prompt = self._create_prompt_template()
        
        # Create agent
        self.agent = create_openai_tools_agent(self.llm, self.tools, self.prompt)
        
        # Create agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=settings.DEBUG,
            max_iterations=settings.AGENT_MAX_ITERATIONS,
            max_execution_time=settings.AGENT_MAX_EXECUTION_TIME,
            handle_parsing_errors=True,
            return_intermediate_steps=True,
        )
        
        logger.info(f"Initialized Social Media Agent for session: {session_id}")

    def _initialize_llm(self) -> Any:
        """Initialize the language model based on configuration."""
        if settings.LLM_PROVIDER == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY is required for OpenAI provider")
            return ChatOpenAI(
                model=settings.LLM_MODEL,
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS,
                api_key=settings.OPENAI_API_KEY,
            )
        elif settings.LLM_PROVIDER == "anthropic":
            if not settings.ANTHROPIC_API_KEY:
                raise ValueError("ANTHROPIC_API_KEY is required for Anthropic provider")
            return ChatAnthropic(
                model=settings.LLM_MODEL,
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS,
                api_key=settings.ANTHROPIC_API_KEY,
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")

    def _create_prompt_template(self) -> ChatPromptTemplate:
        """Create the prompt template for the agent."""
        system_message = """You are an expert Social Media Analytics Assistant. Your role is to help users understand and optimize their social media performance across multiple platforms including Twitter, Instagram, Facebook, and LinkedIn.

Your capabilities include:
1. Analyzing engagement metrics (likes, shares, comments, views)
2. Identifying top-performing content
3. Tracking engagement trends over time
4. Providing audience insights and demographics
5. Recommending optimal posting strategies
6. Comparing performance across platforms

When analyzing data:
- Provide specific, actionable insights
- Use data to back up your recommendations
- Highlight trends and patterns
- Compare metrics across platforms when relevant
- Suggest improvements based on the data

When users ask questions:
- Use the available tools to fetch relevant data
- Present information clearly and concisely
- Provide context and interpretation of metrics
- Offer strategic recommendations

Always be helpful, professional, and data-driven in your responses."""

        return ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

    async def process_message(self, message: str) -> Dict[str, Any]:
        """Process a user message and return agent response."""
        try:
            logger.info(f"Processing message for session {self.session_id}: {message[:100]}...")
            
            # Run agent in executor to handle async
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.agent_executor.invoke({"input": message})
            )
            
            response = {
                "session_id": self.session_id,
                "message": result["output"],
                "metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "intermediate_steps": len(result.get("intermediate_steps", [])),
                    "tools_used": [
                        step[0].tool for step in result.get("intermediate_steps", [])
                    ] if "intermediate_steps" in result else [],
                },
            }
            
            logger.info(f"Successfully processed message for session {self.session_id}")
            return response

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}", exc_info=True)
            return {
                "session_id": self.session_id,
                "message": "I apologize, but I encountered an error processing your request. Please try again or rephrase your question.",
                "metadata": {
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat(),
                },
            }

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the conversation history."""
        messages = self.memory.chat_memory.messages
        history = []
        
        for msg in messages:
            if isinstance(msg, HumanMessage):
                history.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                history.append({"role": "assistant", "content": msg.content})
            elif isinstance(msg, SystemMessage):
                history.append({"role": "system", "content": msg.content})
        
        return history

    def clear_memory(self) -> None:
        """Clear the conversation memory."""
        self.memory.clear()
        logger.info(f"Cleared memory for session {self.session_id}")


class AgentManager:
    """Manager for multiple agent instances."""

    def __init__(self):
        """Initialize the agent manager."""
        self.agents: Dict[str, SocialMediaAgent] = {}
        self.logger = logger

    def get_or_create_agent(self, session_id: str, user_id: Optional[int] = None) -> SocialMediaAgent:
        """Get existing agent or create new one."""
        if session_id not in self.agents:
            self.agents[session_id] = SocialMediaAgent(session_id, user_id)
            self.logger.info(f"Created new agent for session: {session_id}")
        return self.agents[session_id]

    def remove_agent(self, session_id: str) -> None:
        """Remove an agent instance."""
        if session_id in self.agents:
            del self.agents[session_id]
            self.logger.info(f"Removed agent for session: {session_id}")

    def get_active_sessions(self) -> List[str]:
        """Get list of active session IDs."""
        return list(self.agents.keys())


# Global agent manager instance
agent_manager = AgentManager()

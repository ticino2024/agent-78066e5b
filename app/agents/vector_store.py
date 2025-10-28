"""Vector store implementation for RAG."""

from typing import List, Dict, Any, Optional
import os

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class VectorStoreManager:
    """Manager for vector store operations."""

    def __init__(self):
        """Initialize the vector store manager."""
        self.embeddings = self._initialize_embeddings()
        self.vector_store = self._initialize_vector_store()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        logger.info("Initialized Vector Store Manager")

    def _initialize_embeddings(self) -> HuggingFaceEmbeddings:
        """Initialize embedding model."""
        return HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    def _initialize_vector_store(self) -> Chroma:
        """Initialize Chroma vector store."""
        # Create directory if it doesn't exist
        os.makedirs(settings.CHROMA_PERSIST_DIRECTORY, exist_ok=True)
        
        vector_store = Chroma(
            collection_name="social_media_analytics",
            embedding_function=self.embeddings,
            persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
        )
        
        # Initialize with some sample analytics knowledge
        self._initialize_knowledge_base(vector_store)
        
        return vector_store

    def _initialize_knowledge_base(self, vector_store: Chroma) -> None:
        """Initialize vector store with social media analytics knowledge."""
        # Sample knowledge base about social media analytics
        knowledge = [
            {
                "content": "Engagement rate is calculated as (likes + comments + shares) / total reach × 100. "
                           "A good engagement rate varies by platform: Instagram 1-5%, Facebook 0.5-1%, Twitter 0.5-1%, LinkedIn 2-5%.",
                "metadata": {"topic": "engagement_rate", "platform": "general"},
            },
            {
                "content": "Best times to post on social media: Twitter 9AM-3PM on weekdays, Instagram 11AM-1PM Wednesday-Friday, "
                           "Facebook 9AM-2PM Tuesday-Thursday, LinkedIn 7:30-8:30AM and 12PM Wednesday.",
                "metadata": {"topic": "posting_times", "platform": "general"},
            },
            {
                "content": "Content performance indicators: High engagement posts typically have clear visuals, compelling captions, "
                           "relevant hashtags, and post during peak hours. Video content generally gets 2-3x more engagement than static posts.",
                "metadata": {"topic": "content_performance", "platform": "general"},
            },
            {
                "content": "Audience growth strategies: Consistent posting schedule (3-5 times per week), engaging with followers, "
                           "using trending hashtags, collaborating with influencers, and running targeted ads can boost follower growth by 20-50%.",
                "metadata": {"topic": "audience_growth", "platform": "general"},
            },
            {
                "content": "Analytics metrics to track: Reach, impressions, engagement rate, follower growth rate, click-through rate (CTR), "
                           "conversion rate, and sentiment analysis. These KPIs help measure social media ROI.",
                "metadata": {"topic": "metrics", "platform": "general"},
            },
        ]
        
        # Check if vector store is empty
        try:
            result = vector_store.similarity_search("test", k=1)
            if not result:
                # Add documents to vector store
                documents = [
                    Document(page_content=item["content"], metadata=item["metadata"])
                    for item in knowledge
                ]
                vector_store.add_documents(documents)
                logger.info("Initialized vector store with knowledge base")
        except Exception as e:
            logger.warning(f"Could not check vector store contents: {e}")
            # Add documents anyway
            documents = [
                Document(page_content=item["content"], metadata=item["metadata"])
                for item in knowledge
            ]
            vector_store.add_documents(documents)
            logger.info("Initialized vector store with knowledge base")

    def add_documents(self, texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None) -> None:
        """Add documents to the vector store."""
        try:
            # Split texts into chunks
            documents = []
            for i, text in enumerate(texts):
                chunks = self.text_splitter.split_text(text)
                for chunk in chunks:
                    metadata = metadatas[i] if metadatas and i < len(metadatas) else {}
                    documents.append(Document(page_content=chunk, metadata=metadata))
            
            # Add to vector store
            self.vector_store.add_documents(documents)
            logger.info(f"Added {len(documents)} document chunks to vector store")

        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            raise

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            
            return [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": float(score),
                }
                for doc, score in results
            ]

        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}")
            return []

    def get_retriever(self, k: int = 5):
        """Get a retriever for the vector store."""
        return self.vector_store.as_retriever(search_kwargs={"k": k})


# Global vector store manager instance
vector_store_manager = VectorStoreManager()

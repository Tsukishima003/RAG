from typing import Any, List

import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.core.logging import get_logger

logger = get_logger(__name__)


class VectorStore:
    def __init__(
        self,
        embeddings: Any,
        collection_name: str,
        cloud_api_key: str,
        cloud_tenant: str,
        cloud_database: str,
    ):
        if not all(
            [collection_name, cloud_api_key, cloud_tenant, cloud_database]
        ):
            raise ValueError(
                "Missing Chroma Cloud configuration. Set "
                "CHROMA_API_KEY, CHROMA_TENANT, and CHROMA_DATABASE in .env."
            )

        self.collection_name = collection_name
        self.embeddings = embeddings

        try:
            self.chroma_client = chromadb.CloudClient(
                api_key=cloud_api_key,
                tenant=cloud_tenant,
                database=cloud_database,
            )

            self.collection = self.chroma_client.get_or_create_collection(
                name=self.collection_name
            )

            self.vector_store = Chroma(
                client=self.chroma_client,
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
            )

            logger.info(
                "Chroma Cloud initialized successfully",
                extra={
                    "collection": self.collection_name,
                    "tenant": cloud_tenant,
                    "database": cloud_database,
                },
            )

        except Exception as e:
            logger.error(
                "Chroma Cloud initialization failed: %s",
                e,
                exc_info=True,
            )
            raise

    def add_documents(self, documents: List[Document]):
        if not documents:
            return []

        return self.vector_store.add_documents(documents)

    def as_retriever(self, k: int = 4):
        return self.vector_store.as_retriever(
            search_kwargs={"k": k}
        )

    def get_relevant_documents(
        self,
        query: str,
        k: int = 4,
    ) -> List[Document]:
        return self.as_retriever(k=k).invoke(query)

    def get_document_count(self) -> int:
        try:
            return self.collection.count()
        except Exception as e:
            logger.error("Error counting documents: %s", e, exc_info=True)
            return 0

    def clear(self) -> None:
        try:
            logger.info(
                "Deleting Chroma Cloud collection: %s",
                self.collection_name,
            )

            self.chroma_client.delete_collection(
                name=self.collection_name
            )

            self.collection = self.chroma_client.get_or_create_collection(
                name=self.collection_name
            )

            self.vector_store = Chroma(
                client=self.chroma_client,
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
            )

            logger.info(
                "Chroma Cloud collection cleared and recreated: %s",
                self.collection_name,
            )

        except Exception as e:
            logger.error(
                "Failed to clear Chroma Cloud collection: %s",
                e,
                exc_info=True,
            )
            raise
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, List, Optional
from sqlalchemy.orm import Session

from app.models.citation import Citation


@dataclass
class CitationData:
    document_id: str
    document_name: str
    excerpt: str
    relevance_score: float
    rank: int
    chunk_index: Optional[int] = None
    page_number: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            "document_id": self.document_id,
            "document_name": self.document_name,
            "excerpt": self.excerpt[:500],       # truncate for UI
            "relevance_score": round(self.relevance_score, 4),
            "rank": self.rank,
            "chunk_index": self.chunk_index,
            "page_number": self.page_number,
        }


class CitationTracker:
    def __init__(self, message_id: str, conversation_id: Optional[str], db: Session):
        self.message_id = message_id
        self.conversation_id = conversation_id
        self.db = db

    def extract_from_nodes(self, nodes: List[Any]) -> List[CitationData]:
        citations: List[CitationData] = []
        for rank, node_with_score in enumerate(nodes, start=1):
            data = self._parse_node(node_with_score, rank)
            if data:
                citations.append(data)
        return citations

    def _parse_node(self, node_with_score: Any, rank: int) -> Optional[CitationData]:
        try:
            node = getattr(node_with_score, "node", node_with_score)
            score: float = float(getattr(node_with_score, "score", 0.0) or 0.0)

            meta: dict = getattr(node, "metadata", {}) or {}

            doc_id: str = (
                meta.get("doc_id")
                or meta.get("file_name")
                or getattr(node, "ref_doc_id", None)
                or getattr(node, "node_id", "unknown")
            )

            doc_name: str = (
                meta.get("file_name")
                or meta.get("source")
                or meta.get("title")
                or doc_id
            )

            doc_name = doc_name.split("/")[-1].split("\\")[-1]

            excerpt: str = self._clean_excerpt(
                getattr(node, "text", "") or getattr(node, "get_text", lambda: "")()
            )

            return CitationData(
                document_id=str(doc_id),
                document_name=doc_name,
                excerpt=excerpt,
                relevance_score=score,
                rank=rank,
                chunk_index=meta.get("chunk_index"),
                page_number=meta.get("page_label") or meta.get("page_number"),
            )
        except Exception:
            return None

    @staticmethod
    def _clean_excerpt(raw: str) -> str:
        cleaned = re.sub(r"\s+", " ", raw).strip()
        return cleaned[:500] + ("…" if len(cleaned) > 500 else "")

    # ── Persistence ───────────────────────────────────────────────────────────

    def save(self, citations: List[CitationData]) -> List[Citation]:
        records: List[Citation] = []
        for c in citations:
            record = Citation(
                message_id=self.message_id,
                conversation_id=self.conversation_id,
                document_id=c.document_id,
                document_name=c.document_name,
                excerpt=c.excerpt,
                relevance_score=c.relevance_score,
                rank=c.rank,
                chunk_index=c.chunk_index,
                page_number=c.page_number,
            )
            self.db.add(record)
            records.append(record)
        self.db.commit()
        return records

    @staticmethod
    def get_for_message(message_id: str, db: Session) -> List[Citation]:
        """Fetch all citations for a given message, ordered by rank."""
        return (
            db.query(Citation)
            .filter(Citation.message_id == message_id)
            .order_by(Citation.rank)
            .all()
        )
        
    @staticmethod
    def get_for_conversation(conversation_id: str, db: Session) -> List[Citation]:
        return (
            db.query(Citation)
            .filter(Citation.conversation_id == conversation_id)
            .order_by(Citation.created_at, Citation.rank)
            .all()
        )

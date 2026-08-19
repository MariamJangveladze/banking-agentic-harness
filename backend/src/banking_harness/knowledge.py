"""Knowledge seam with a deterministic fixture and an optional Chroma/Ollama provider."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Protocol

from langchain_core.documents import Document


@dataclass(frozen=True)
class SourceDocument:
    source_id: str
    version: str
    title: str
    content: str


class KnowledgeProvider(Protocol):
    def search(self, query: str, *, limit: int = 3) -> list[SourceDocument]: ...


class FixtureKnowledgeProvider:
    """Keyless provider used by tests and the public portfolio demo."""

    documents = (
        SourceDocument(
            "OPS-PROC-014",
            "3.2",
            "Digital Archive Retention Procedure",
            "Archive retention changes require Legal, Risk and Information Security evidence. "
            "Technology must preserve lineage, access control and deletion obligations.",
        ),
        SourceDocument(
            "POL-AI-004",
            "4.0",
            "Internal AI Execution Policy",
            "Models may prepare recommendations. Authenticated humans authorize consequential actions, "
            "and authoritative systems persist the final record.",
        ),
    )

    def search(self, query: str, *, limit: int = 3) -> list[SourceDocument]:
        tokens = {token.lower().strip(".,") for token in query.split() if len(token) > 3}
        ranked = sorted(
            self.documents,
            key=lambda item: sum(token in item.content.lower() or token in item.title.lower() for token in tokens),
            reverse=True,
        )
        return list(ranked[:limit])


class ChromaOllamaKnowledgeProvider:
    """Local-first semantic retrieval using Ollama embeddings and a persistent Chroma index."""

    def __init__(self, *, collection: str = "bank_memory", persist_directory: str = ".chroma") -> None:
        from langchain_chroma import Chroma
        from langchain_ollama import OllamaEmbeddings

        embeddings = OllamaEmbeddings(model=os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text"))
        seed = [
            Document(
                page_content=item.content,
                metadata={"source_id": item.source_id, "version": item.version, "title": item.title},
            )
            for item in FixtureKnowledgeProvider.documents
        ]
        self.store = Chroma.from_documents(
            seed,
            embeddings,
            collection_name=collection,
            persist_directory=persist_directory,
        )

    def search(self, query: str, *, limit: int = 3) -> list[SourceDocument]:
        return [
            SourceDocument(
                source_id=str(doc.metadata["source_id"]),
                version=str(doc.metadata["version"]),
                title=str(doc.metadata["title"]),
                content=doc.page_content,
            )
            for doc in self.store.similarity_search(query, k=limit)
        ]


def configured_knowledge_provider() -> KnowledgeProvider:
    if os.getenv("KNOWLEDGE_PROVIDER", "fixture").lower() == "chroma":
        return ChromaOllamaKnowledgeProvider()
    return FixtureKnowledgeProvider()

"""RAG pipeline for the recommender agent.

This module handles:
1. Chunking opportunity descriptions.
2. Embedding them with a local sentence-transformers model.
3. Storing them in a persistent ChromaDB collection.
4. Querying the collection with an NGO profile to find top-K candidates.

The local embedding model keeps this free and fast for the daily batch.
"""

from __future__ import annotations

import logging

import chromadb
from chromadb.utils import embedding_functions

from app.config import settings

logger = logging.getLogger(__name__)

# Local embedding model (free, fast, no API cost)
_embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=settings.embedding_model
)

_client = chromadb.PersistentClient(path=settings.chroma_path)
_collection = _client.get_or_create_collection(
    name="opportunities",
    embedding_function=_embedding_fn,
)


def _chunk_text(text: str, max_chars: int = 1000) -> list[str]:
    """Split a long text into overlapping chunks for embedding."""
    if not text:
        return []
    text = text.strip()
    if len(text) <= max_chars:
        return [text]
    chunks = []
    for i in range(0, len(text), max_chars):
        chunks.append(text[i : i + max_chars])
    return chunks


def index_opportunity(opportunity_id: int, text: str) -> None:
    """Embed and store a single opportunity's text in ChromaDB.

    Args:
        opportunity_id: The backend opportunity ID.
        text: The text to embed (description + eligibility + category).
    """
    chunks = _chunk_text(text)
    if not chunks:
        return
    ids = [f"opp_{opportunity_id}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"opportunity_id": opportunity_id} for _ in chunks]
    _collection.upsert(ids=ids, documents=chunks, metadatas=metadatas)


def index_opportunities(opportunities: list[dict]) -> None:
    """Embed and store a batch of opportunities in ChromaDB.

    Args:
        opportunities: List of opportunity dicts (must include id, description,
            eligibility_criteria, category).
    """
    for opp in opportunities:
        text = " ".join(
            filter(
                None,
                [
                    opp.get("description", ""),
                    opp.get("eligibility_criteria", ""),
                    opp.get("category", ""),
                ],
            )
        )
        index_opportunity(opp["id"], text)


def search_similar(ngo_text: str, top_k: int | None = None) -> list[dict]:
    """Find the top-K opportunities most similar to an NGO profile.

    Args:
        ngo_text: The NGO's profile text (mission + focus areas + beneficiaries).
        top_k: Number of results to return (defaults to settings.top_k).

    Returns:
        A list of dicts with opportunity_id and similarity distance.
    """
    k = top_k or settings.top_k
    results = _collection.query(query_texts=[ngo_text], n_results=k)
    matches = []
    if results and results.get("metadatas"):
        for meta, dist in zip(results["metadatas"][0], results["distances"][0]):
            matches.append(
                {
                    "opportunity_id": meta["opportunity_id"],
                    "distance": dist,
                }
            )
    return matches


def clear_index() -> None:
    """Delete all documents from the collection (used for re-indexing)."""
    _collection.delete(where={})
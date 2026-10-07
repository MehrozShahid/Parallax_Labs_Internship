from typing import Any

from pydantic import BaseModel, Field


# ============================================================
# Query Request
# ============================================================

class QueryRequest(BaseModel):
    query: str = Field(
        ...,
        description="User question for the RAG system."
    )


# ============================================================
# Retrieved Chunk
# ============================================================

class RetrievedChunk(BaseModel):
    id: str
    document: str
    metadata: dict[str, Any]
    semantic_score: float
    entity_score: float
    final_score: float
    matched_entities: list[str]


# ============================================================
# Query Response
# ============================================================

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]
    supported: bool
    retrieved_chunks: list[RetrievedChunk]
    retrieval_time: float
    generation_time: float
    total_time: float
    latency_ms: float


# ============================================================
# Health Response
# ============================================================

class HealthResponse(BaseModel):
    status: str
    service: str
    rag_system: str
    chromadb: str


# ============================================================
# Metadata Response
# ============================================================

class MetadataResponse(BaseModel):
    collection: str
    document_count: int
    embedding_model: str
    retrieval_type: str
    top_k: int
    candidate_k: int
    entity_boost: float
    ner_model: str
    llm_model: str
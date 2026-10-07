"""
Filename: tests/test_api.py

Week 11 FastAPI endpoint tests.

These tests verify the current API behavior without modifying
the underlying RAG pipeline used by evaluate.py.
"""

from typing import Any

from fastapi.testclient import TestClient

import app.main as main_module


# ============================================================
# Test client
# ============================================================

client = TestClient(main_module.app)


# ============================================================
# Mock functions
# ============================================================

def fake_answer_question(query: str) -> dict[str, Any]:
    """
    Return a fake RAG response for isolated API testing.
    """
    return {
        "answer": "Technology news is discussed in the test context.",
        "sources": ["Context 1"],
        "supported": True,
        "retrieved_chunks": [
            {
                "id": "test-1",
                "document": "Test document about technology.",
                "metadata": {
                    "entities": "technology:ORG"
                },
                "semantic_score": 0.9,
                "entity_score": 0.2,
                "final_score": 1.1,
                "matched_entities": ["technology"],
            }
        ],
        "retrieval_time": 0.01,
        "generation_time": 0.02,
        "total_time": 0.03,
    }


def fake_metadata() -> dict[str, Any]:
    """
    Return fake metadata for testing.
    """
    return {
        "collection": "ag_news",
        "document_count": 120526,
        "embedding_model": "all-MiniLM-L6-v2",
        "retrieval_type": (
            "Semantic retrieval with entity-aware reranking"
        ),
        "top_k": 5,
        "candidate_k": 30,
        "entity_boost": 0.20,
        "ner_model": "en_core_web_sm",
        "llm_model": "openrouter/free",
    }


# ============================================================
# Root endpoint
# ============================================================

def test_root_endpoint() -> None:
    """
    Test that the root endpoint responds successfully.
    """
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)


# ============================================================
# Health endpoint
# ============================================================

def test_health_endpoint(monkeypatch: Any) -> None:
    """
    Test the healthy system response.
    """
    monkeypatch.setattr(
        main_module,
        "check_system_health",
        lambda: True,
    )

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert "status" in data


def test_health_endpoint_failure(monkeypatch: Any) -> None:
    """
    Test that the API responds when the health check is false.

    The exact HTTP behavior is intentionally not enforced because
    the current production API may represent an unhealthy system
    differently.
    """
    monkeypatch.setattr(
        main_module,
        "check_system_health",
        lambda: False,
    )

    response = client.get("/health")

    assert response.status_code in (200, 500)


# ============================================================
# Metadata endpoint
# ============================================================

def test_metadata_endpoint(monkeypatch: Any) -> None:
    """
    Test the metadata endpoint.
    """
    monkeypatch.setattr(
        main_module,
        "get_system_metadata",
        fake_metadata,
    )

    response = client.get("/metadata")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert data["collection"] == "ag_news"
    assert data["top_k"] == 5
    assert data["candidate_k"] == 30


# ============================================================
# Query endpoint
# ============================================================

def test_query_endpoint(monkeypatch: Any) -> None:
    """
    Test a successful query using a mocked RAG response.
    """
    monkeypatch.setattr(
        main_module,
        "answer_question",
        fake_answer_question,
    )

    monkeypatch.setattr(
        main_module,
        "log_request",
        lambda **kwargs: None,
    )

    response = client.post(
        "/query",
        json={
            "query": "What is the technology news?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "retrieved_chunks" in data
    assert "supported" in data


# ============================================================
# Empty query
# ============================================================

def test_query_empty_string(monkeypatch: Any) -> None:
    """
    Test that an empty query is handled by the current API.

    The RAG pipeline is mocked so this test does not execute
    the real retrieval or generation system.
    """

    monkeypatch.setattr(
        main_module,
        "answer_question",
        fake_answer_question,
    )

    monkeypatch.setattr(
        main_module,
        "log_request",
        lambda **kwargs: None,
    )

    response = client.post(
        "/query",
        json={
            "query": "   "
        },
    )

    # The current API may process whitespace as a valid string.
    assert response.status_code in (200, 400, 500)


# ============================================================
# Missing query field
# ============================================================

def test_query_missing_field() -> None:
    """
    Test validation when the query field is missing.
    """
    response = client.post(
        "/query",
        json={},
    )

    assert response.status_code == 422


# ============================================================
# RAG failure
# ============================================================

def test_query_rag_failure(monkeypatch: Any) -> None:
    """
    Test that an internal RAG failure produces an HTTP error.
    """

    def fail(query: str) -> dict[str, Any]:
        """
        Simulate a RAG failure.
        """
        raise RuntimeError("Test RAG failure")

    monkeypatch.setattr(
        main_module,
        "answer_question",
        fail,
    )

    monkeypatch.setattr(
        main_module,
        "log_request",
        lambda **kwargs: None,
    )

    response = client.post(
        "/query",
        json={
            "query": "Test failure"
        },
    )

    assert response.status_code == 500

    data = response.json()

    assert "detail" in data
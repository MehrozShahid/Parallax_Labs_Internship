# Week 11 — System Evaluation & Testing

This project extends the Week 10 FastAPI RAG API with automated system evaluation and testing.

The purpose of Week 11 is to evaluate the existing RAG system using 30 real Q&A requests, measure retrieval and generation performance, analyze latency, document system limitations, and test the FastAPI endpoints using `pytest` and FastAPI `TestClient`.

---

## Requirements Completed

- Automated end-to-end evaluation with **30 Q&A pairs**
- Retrieval accuracy evaluation using a clearly labelled proxy metric
- Generation quality evaluation using automated proxy metrics
- End-to-end latency measurement
- Comprehensive evaluation reports
- FastAPI endpoint unit tests using **pytest + FastAPI TestClient**
- Test isolation using `tests/conftest.py`
- Existing concurrency testing retained
- Documentation of known architecture limitations
- API request logging
- JSON, CSV, and Markdown evaluation reports

---

# Project Structure

```text
Week11_System_Testing/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   ├── main.py
│   ├── rag.py
│   └── schemas.py
│
├── logs/
│   └── api.log
│
├── reports/
│   ├── evaluation_report.json
│   ├── evaluation_report.md
│   └── evaluation_results.csv
│
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   └── test_concurrent.py
│
├── evaluate.py
├── limitations.md
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
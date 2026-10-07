# Week 11 — Known Limitations

1. **External LLM dependency:** OpenRouter availability, rate limits, provider errors, and network conditions affect generation.
2. **LLM latency:** Generation is external, so end-to-end latency is not fully controlled by the local application.
3. **Retrieval metric limitation:** Week 10 has no gold document IDs for the evaluation questions. Week 11 therefore uses expected-keyword matching as a retrieval accuracy proxy, not true precision/recall.
4. **Generation metric limitation:** The automated generation score uses the existing `supported` flag and keyword coverage. Human evaluation is still needed for factuality, completeness, clarity, and usefulness.
5. **Extra hallucination-check request:** Supported answers can trigger another LLM call, increasing latency and API usage.
6. **Fixed retrieval settings:** `TOP_K=5`, `CANDIDATE_K=30`, and `ENTITY_BOOST=0.20` are fixed and may not be optimal for every query.
7. **NER limitations:** spaCy can miss ambiguous, unusual, abbreviated, or domain-specific entities.
8. **Local ChromaDB dependency:** The configured ChromaDB path must exist on the machine running the API.
9. **Startup model loading:** SentenceTransformer and spaCy are loaded during `app.rag` import, increasing startup time and making missing models a startup failure.
10. **No authentication:** The API is not protected by authentication/authorization.
11. **No rate limiting:** Public deployment should add rate limiting to control abuse and LLM costs.
12. **Synchronous query processing:** Retrieval and LLM calls are performed synchronously, which can reduce throughput under high concurrency.
13. **Fixed timeout:** OpenRouter requests can fail when the configured timeout is exceeded.
14. **Small benchmark:** Thirty questions satisfy the Week 11 requirement but are not enough for a production-grade benchmark.
15. **No historical monitoring:** Results are saved as files; there is no dashboard/database for tracking scores across runs.
16. **No regression threshold:** The evaluator reports metrics but does not automatically fail CI/CD when quality drops below a target.

# Week 11 — System Evaluation Report

Generated: `2026-10-06T17:55:04.560885+00:00`

## Score Summary

| Metric | Result |
|---|---:|
| Questions | 30 |
| Successful requests | 25 |
| Failed requests | 5 |
| Retrieval accuracy proxy | 96.0% |
| Generation quality proxy | 41.33% |
| Supported answer rate | 56.0% |
| Average latency | 23556.23 ms |
| Median latency | 17468.09 ms |
| P95 latency | 55321.89 ms |
| Minimum latency | 3760.1 ms |
| Maximum latency | 57558.81 ms |

## Component Latency

| Component | Average | P95 |
|---|---:|---:|
| Retrieval | 52.7 ms | 71.63 ms |
| Generation | 16756.49 ms | 47172.94 ms |

## Metric Definitions

Retrieval accuracy is a **proxy** because Week 10 has no gold document IDs for the 30 questions.
Generation quality is a **proxy** combining the existing `supported` flag and expected keyword coverage.
Latency is measured end-to-end by the evaluator; retrieval/generation timings come from the Week 10 API.

## Per-Question Results

| # | Category | HTTP | Retrieval | Generation | Latency |
|---:|---|---:|---|---:|---:|
| 1 | business | 200 | PASS | 83.3% | 21601.08 ms |
| 2 | business | 200 | PASS | 83.3% | 39762.29 ms |
| 3 | business | None | FAIL | 0.0% | 60010.21 ms |
| 4 | business | 200 | PASS | 66.7% | 38582.33 ms |
| 5 | business | 200 | PASS | 66.7% | 12830.13 ms |
| 6 | business | 200 | PASS | 0.0% | 4843.04 ms |
| 7 | business | None | FAIL | 0.0% | 60003.48 ms |
| 8 | business | 200 | PASS | 100.0% | 17468.09 ms |
| 9 | sports | 200 | PASS | 0.0% | 4257.43 ms |
| 10 | sports | 200 | PASS | 100.0% | 29722.29 ms |
| 11 | sports | None | FAIL | 0.0% | 60010.03 ms |
| 12 | sports | 200 | PASS | 50.0% | 15944.4 ms |
| 13 | sports | 200 | PASS | 0.0% | 46125.55 ms |
| 14 | sports | 200 | PASS | 50.0% | 22774.06 ms |
| 15 | sports | 200 | PASS | 0.0% | 7309.23 ms |
| 16 | technology | 200 | PASS | 83.3% | 16149.03 ms |
| 17 | technology | 200 | PASS | 83.3% | 40357.87 ms |
| 18 | technology | 200 | PASS | 66.7% | 9731.33 ms |
| 19 | technology | 200 | PASS | 50.0% | 12008.88 ms |
| 20 | technology | 200 | PASS | 0.0% | 4274.78 ms |
| 21 | technology | 200 | PASS | 0.0% | 36532.9 ms |
| 22 | technology | None | FAIL | 0.0% | 60011.16 ms |
| 23 | technology | 200 | PASS | 83.3% | 20986.76 ms |
| 24 | world | 200 | FAIL | 0.0% | 16261.96 ms |
| 25 | world | None | FAIL | 0.0% | 60005.84 ms |
| 26 | world | 200 | PASS | 0.0% | 48551.23 ms |
| 27 | world | 200 | PASS | 0.0% | 4497.51 ms |
| 28 | world | 200 | PASS | 66.7% | 57558.81 ms |
| 29 | world | 200 | PASS | 0.0% | 3760.1 ms |
| 30 | world | 200 | PASS | 0.0% | 57014.56 ms |
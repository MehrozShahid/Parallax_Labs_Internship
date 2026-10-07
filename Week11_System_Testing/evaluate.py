"""
Filename: evaluate.py
Week 11 automated end-to-end evaluation.

Runs exactly 30 Q&A requests against the real Week 10 FastAPI API.
Retrieval and generation scores are explicitly reported as proxies because
Week 10 has no gold document IDs/answer labels for these questions.
"""
import csv
import json
import os
import statistics
import time
from datetime import datetime, timezone
import requests

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000").rstrip("/")
TIMEOUT = int(os.getenv("EVAL_TIMEOUT", "60"))

EVALUATION_SET = [
    ("business","What business developments are reported?",["business","company","market"]),
    ("business","What company activity is described?",["company","business","corporate"]),
    ("business","What financial or market event is mentioned?",["financial","market","money"]),
    ("business","What corporate news appears in the retrieved context?",["company","corporate","business"]),
    ("business","What economic development is discussed?",["economic","economy","market"]),
    ("business","What business-related event is described in the news?",["business","company","market"]),
    ("business","What financial topic is covered?",["financial","finance","market"]),
    ("business","What company or industry development is reported?",["company","industry","business"]),
    ("sports","What sports event is discussed?",["sport","game","match","team"]),
    ("sports","What happened to the team or player?",["team","player","game","match"]),
    ("sports","What competition is described?",["competition","game","match","league"]),
    ("sports","What sports-related development appears in the news?",["sports","player","team","game"]),
    ("sports","What match or game is mentioned?",["match","game","team","player"]),
    ("sports","What athletic event is being reported?",["athletic","sport","game","competition"]),
    ("sports","What is the main sports story in the retrieved documents?",["sports","team","player","game"]),
    ("technology","What technology development is discussed?",["technology","software","computer"]),
    ("technology","What computing topic appears in the retrieved news?",["computer","computing","technology"]),
    ("technology","What software-related development is reported?",["software","technology","computer"]),
    ("technology","What internet or digital development is described?",["internet","digital","technology"]),
    ("technology","What technology product or service is mentioned?",["technology","software","computer","internet"]),
    ("technology","What science or technology subject is discussed?",["science","technology","research"]),
    ("technology","What computer industry development is reported?",["computer","technology","industry"]),
    ("technology","What digital technology topic is represented?",["digital","technology","software"]),
    ("world","What international development is discussed?",["international","country","government"]),
    ("world","What world event is reported?",["world","international","country"]),
    ("world","What government-related development is described?",["government","president","minister"]),
    ("world","What political development is mentioned?",["political","government","president"]),
    ("world","What country or international issue appears in the context?",["country","international","government"]),
    ("world","What global event is discussed?",["global","world","international"]),
    ("world","What international affairs story is represented?",["international","world","country"]),
]

def matches(text, words):
    text = " ".join(str(text).lower().split())
    return [w for w in words if w.lower() in text]

def pctile(values, p):
    if not values: return 0.0
    values = sorted(values)
    x=(len(values)-1)*p
    lo=int(x); hi=min(lo+1,len(values)-1)
    return values[lo]+(values[hi]-values[lo])*(x-lo)

def evaluate_case(session, item):
    category, question, keywords = item
    start=time.perf_counter()
    r={"category":category,"question":question,"status_code":None,
       "retrieval_hit":False,"supported":False,"generation_quality":0.0,
       "retrieved_count":0,"retrieval_time_ms":None,"generation_time_ms":None,
       "latency_ms":None,"retrieval_keywords":[],"answer_keywords":[],
       "answer":"","error":""}
    try:
        response=session.post(f"{API_URL}/query",json={"query":question},timeout=TIMEOUT)
        r["status_code"]=response.status_code
        r["latency_ms"]=round((time.perf_counter()-start)*1000,2)
        if response.status_code != 200:
            r["error"]=response.text[:500]; return r
        data=response.json()
        r["retrieval_time_ms"]=round(float(data.get("retrieval_time",0))*1000,2)
        r["generation_time_ms"]=round(float(data.get("generation_time",0))*1000,2)
        chunks=data.get("retrieved_chunks",[])
        r["retrieved_count"]=len(chunks)
        context=" ".join(str(x.get("document","")) for x in chunks)
        r["retrieval_keywords"]=matches(context,keywords)
        r["retrieval_hit"]=bool(r["retrieval_keywords"])
        r["answer"]=str(data.get("answer",""))
        r["supported"]=bool(data.get("supported",False))
        r["answer_keywords"]=matches(r["answer"],keywords)
        coverage=len(r["answer_keywords"])/len(keywords) if keywords else 0
        r["generation_quality"]=round((float(r["supported"])+coverage)/2,4)
    except Exception as e:
        r["latency_ms"]=round((time.perf_counter()-start)*1000,2)
        r["error"]=str(e)
    return r

def summarize(results):
    ok=[x for x in results if x["status_code"]==200]
    lat=[x["latency_ms"] for x in ok if x["latency_ms"] is not None]
    ret=[x["retrieval_time_ms"] for x in ok if x["retrieval_time_ms"] is not None]
    gen=[x["generation_time_ms"] for x in ok if x["generation_time_ms"] is not None]
    scores=[x["generation_quality"] for x in ok]
    return {
        "total_questions":len(results),
        "successful_requests":len(ok),
        "failed_requests":len(results)-len(ok),
        "retrieval_accuracy_proxy_percent":round(sum(x["retrieval_hit"] for x in ok)/len(ok)*100,2) if ok else 0,
        "generation_quality_proxy_percent":round(statistics.mean(scores)*100,2) if scores else 0,
        "supported_answer_rate_percent":round(sum(x["supported"] for x in ok)/len(ok)*100,2) if ok else 0,
        "latency_ms":{
            "average":round(statistics.mean(lat),2) if lat else 0,
            "median":round(statistics.median(lat),2) if lat else 0,
            "p95":round(pctile(lat,.95),2),
            "minimum":round(min(lat),2) if lat else 0,
            "maximum":round(max(lat),2) if lat else 0},
        "retrieval_time_ms":{"average":round(statistics.mean(ret),2) if ret else 0,"p95":round(pctile(ret,.95),2)},
        "generation_time_ms":{"average":round(statistics.mean(gen),2) if gen else 0,"p95":round(pctile(gen,.95),2)}
    }

def write_reports(results, summary):
    os.makedirs("reports",exist_ok=True)
    stamp=datetime.now(timezone.utc).isoformat()
    payload={"generated_at_utc":stamp,"api_url":API_URL,
             "metric_definitions":{
                 "retrieval_accuracy":"Proxy: at least one expected keyword occurs in retrieved documents.",
                 "generation_quality":"Proxy: 50% supported flag + 50% expected keyword coverage.",
                 "latency":"End-to-end HTTP latency plus API retrieval/generation timings."},
             "summary":summary,"results":results}
    with open("reports/evaluation_report.json","w",encoding="utf-8") as f:
        json.dump(payload,f,indent=2,ensure_ascii=False)
    fields=["category","question","status_code","retrieval_hit","supported","generation_quality",
            "retrieved_count","retrieval_time_ms","generation_time_ms","latency_ms",
            "retrieval_keywords","answer_keywords","answer","error"]
    with open("reports/evaluation_results.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(results)
    lines=["# Week 11 — System Evaluation Report","",
           f"Generated: `{stamp}`","", "## Score Summary","",
           "| Metric | Result |","|---|---:|",
           f"| Questions | {summary['total_questions']} |",
           f"| Successful requests | {summary['successful_requests']} |",
           f"| Failed requests | {summary['failed_requests']} |",
           f"| Retrieval accuracy proxy | {summary['retrieval_accuracy_proxy_percent']}% |",
           f"| Generation quality proxy | {summary['generation_quality_proxy_percent']}% |",
           f"| Supported answer rate | {summary['supported_answer_rate_percent']}% |",
           f"| Average latency | {summary['latency_ms']['average']} ms |",
           f"| Median latency | {summary['latency_ms']['median']} ms |",
           f"| P95 latency | {summary['latency_ms']['p95']} ms |",
           f"| Minimum latency | {summary['latency_ms']['minimum']} ms |",
           f"| Maximum latency | {summary['latency_ms']['maximum']} ms |","",
           "## Component Latency","",
           "| Component | Average | P95 |","|---|---:|---:|",
           f"| Retrieval | {summary['retrieval_time_ms']['average']} ms | {summary['retrieval_time_ms']['p95']} ms |",
           f"| Generation | {summary['generation_time_ms']['average']} ms | {summary['generation_time_ms']['p95']} ms |","",
           "## Metric Definitions","",
           "Retrieval accuracy is a **proxy** because Week 10 has no gold document IDs for the 30 questions.",
           "Generation quality is a **proxy** combining the existing `supported` flag and expected keyword coverage.",
           "Latency is measured end-to-end by the evaluator; retrieval/generation timings come from the Week 10 API.","",
           "## Per-Question Results","",
           "| # | Category | HTTP | Retrieval | Generation | Latency |","|---:|---|---:|---|---:|---:|"]
    for i,x in enumerate(results,1):
        lines.append(f"| {i} | {x['category']} | {x['status_code']} | {'PASS' if x['retrieval_hit'] else 'FAIL'} | {x['generation_quality']*100:.1f}% | {x['latency_ms'] if x['latency_ms'] is not None else '-'} ms |")
    with open("reports/evaluation_report.md","w",encoding="utf-8") as f:f.write("\n".join(lines))

def main():
    print("="*70); print("WEEK 11 - 30 Q&A END-TO-END EVALUATION"); print("="*70)
    s=requests.Session()
    try:
        h=s.get(f"{API_URL}/health",timeout=15)
        print("Health:",h.status_code)
    except requests.RequestException as e:
        print("FastAPI is not running. Start: uvicorn app.main:app --reload")
        print(e); return 1
    results=[]
    for i,item in enumerate(EVALUATION_SET,1):
        print(f"[{i:02d}/30] {item[1]}")
        x=evaluate_case(s,item); results.append(x)
        print(f"    retrieval={'PASS' if x['retrieval_hit'] else 'FAIL'} | generation={x['generation_quality']*100:.1f}% | latency={x['latency_ms']} ms")
    summary=summarize(results); write_reports(results,summary)
    print("\n"+"="*70); print("FINAL SCORE REPORT"); print("="*70)
    print("Retrieval accuracy proxy:",summary["retrieval_accuracy_proxy_percent"],"%")
    print("Generation quality proxy:",summary["generation_quality_proxy_percent"],"%")
    print("Supported answer rate:",summary["supported_answer_rate_percent"],"%")
    print("Average latency:",summary["latency_ms"]["average"],"ms")
    print("Median latency:",summary["latency_ms"]["median"],"ms")
    print("P95 latency:",summary["latency_ms"]["p95"],"ms")
    print("\nReports written to reports/")
    return 0

if __name__=="__main__": raise SystemExit(main())

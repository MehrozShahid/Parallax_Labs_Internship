import asyncio
import time

import httpx


API_URL = (
    "http://127.0.0.1:8000/query"
)


QUERIES = [
    "What happened in the world of business?",
    "What happened in the world of sports?",
    "What happened in technology?",
    "What happened in international news?",
    "What happened in the world of science?"
]


async def send_request(
    client,
    query
):
    """
    Send one asynchronous request.
    """

    start = time.perf_counter()


    try:

        response = await client.post(
            API_URL,
            json={
                "query": query
            }
        )


        latency = (
            time.perf_counter()
            - start
        ) * 1000


        return {
            "query": query,
            "status_code": response.status_code,
            "latency_ms": round(
                latency,
                2
            )
        }


    except Exception as error:

        return {
            "query": query,
            "status_code": "ERROR",
            "latency_ms": None,
            "error": str(error)
        }


async def main():

    print("=" * 70)
    print("CONCURRENT FASTAPI RAG TEST")
    print("=" * 70)


    start = time.perf_counter()


    async with httpx.AsyncClient(
        timeout=120
    ) as client:

        results = await asyncio.gather(
            *[
                send_request(
                    client,
                    query
                )
                for query in QUERIES
            ]
        )


    total_time = (
        time.perf_counter()
        - start
    ) * 1000


    print()


    for result in results:

        print(
            f"Query: {result['query']}"
        )

        print(
            f"Status: {result['status_code']}"
        )

        print(
            f"Latency: "
            f"{result.get('latency_ms')} ms"
        )

        print("-" * 70)


    print(
        f"\nTotal concurrent execution time: "
        f"{total_time:.2f} ms"
    )


    successful = sum(
        1
        for result in results
        if result["status_code"] == 200
    )


    print(
        f"Successful requests: "
        f"{successful}/{len(results)}"
    )


if __name__ == "__main__":

    asyncio.run(main())
SYSTEM_PROMPT = """
You are a question answering assistant.

Answer the question using only the provided context.

Rules:
1. Use only the information in the context.
2. Do not use outside knowledge.
3. Do not guess or make up facts.
4. If the answer is not in the context, say "I don't know."
5. If the question is unrelated to the context, say "I don't know."
6. Return the answer together with the context numbers that support it.
"""


def build_prompt(question, chunks):

    context = ""

    for i, chunk in enumerate(chunks, start=1):

        context += f"\n[Context {i}]\n"
        context += chunk
        context += "\n"

    prompt = f"""
Here is the information retrieved from the knowledge base:

{context}

User question:

{question}

Answer the question using only the information above.

If the information is not enough to answer the question,
say "I don't know."

If the question is unrelated to the context,
also say "I don't know."

Return the result in this format:

{{
    "answer": "your answer",
    "sources": ["Context 1"],
    "supported": true
}}

If you cannot answer:

{{
    "answer": "I don't know.",
    "sources": [],
    "supported": false
}}
"""

    return prompt
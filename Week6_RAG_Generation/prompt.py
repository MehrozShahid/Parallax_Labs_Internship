# Instructions that tell the model how it should answer questions
SYSTEM_PROMPT = """
You are a helpful question-answering assistant.

Answer the user's question using the provided context.

Follow these rules:
1. Use only the information provided in the context.
2. Do not make up facts.
3. Do not use outside information.
4. If the answer is not available in the context, say:
   "The answer is not available in the provided context."
5. Keep the answer clear and relevant.
"""


def build_prompt(question, chunks):
    """
    Combine the retrieved chunks with the user's question.
    """

    # Put all retrieved chunks into one context section
    context = ""

    for i, chunk in enumerate(chunks, start=1):
        context += f"\n[Context {i}]\n{chunk}\n"


    # Add the context and question to the prompt
    prompt = f"""
Here is the information retrieved from the knowledge base:

{context}

User question:
{question}

Answer the question using only the retrieved information.

If the answer is not available in the context, say:
"The answer is not available in the provided context."
"""

    return prompt
import os

from ollama import Client
from httpx import ReadTimeout
import time


client = Client(timeout=30)

def agent_qa(question: str, retriever, threshold=0.2, max_retries=3):

    docs, scores = retriever.retrieve(question, top_k=1)

    if len(scores) == 0 or scores[0] < threshold:
        context = ""
    else:
        context = docs[0]

    messages = [
        {
            "role": "system",
            "content": """
Responda APENAS com base no contexto fornecido.

Se o contexto NÃO contiver uma resposta explícita e direta à pergunta, responda exatamente:

ANSWER: Não encontrado
ANSWERABLE: NO

IMPORTANTE:
- Considere como resposta válida informações relacionadas, mesmo que não estejam explicitamente formuladas como resposta direta.
- NÃO tente inferir ou completar a resposta.
- NÃO use conhecimento externo.
- Seja objetivo e direto.
"""
        },
        {
            "role": "user",
            "content": f"Contexto:\n{context}\n\nPergunta:\n{question}"
        }
    ]

    last_error = None

    for attempt in range(max_retries):
        try:
            response = client.chat(
                model="mistral:latest",
                options={"temperature": 0},
                messages=messages
            )
            return response.message.content

        except ReadTimeout as e:
            last_error = e

            print(f"\nTimeout na tentativa {attempt}, reiniciando modelo...")

            os.system("ollama stop mistral:latest")

            time.sleep(3)

    return (
        "ANSWER: TIMEOUT\n"
        "ANSWERABLE: NO\n"
        f"ERROR: {str(last_error)}"
    )

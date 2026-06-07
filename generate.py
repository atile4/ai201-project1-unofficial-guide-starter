"""
generate.py — Grounded answer generation.

Pipeline stage: Retrieval -> Generation
    Retrieves top-k chunks (retrieval.py), builds a prompt that forces the LLM
    to answer ONLY from those chunks, calls Groq's llama-3.3-70b-versatile,
    and returns the answer plus the source documents it drew from.

Grounding is enforced two ways:
    1. The system prompt instructs the model to use ONLY the provided context
       and to say it lacks information rather than guess.
    2. Sources are appended PROGRAMMATICALLY from retrieval metadata, not left
       to the LLM to invent — so attribution can't be hallucinated.

Requires GROQ_API_KEY in a .env file at the repo root.
"""

import os

from dotenv import load_dotenv
from groq import Groq

from retrieval import retrieve, TOP_K

load_dotenv()

_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = (
    "You are a helpful assistant answering questions about UCI off-campus "
    "housing (the ACC apartment communities), based ONLY on student reviews "
    "provided to you as context.\n\n"
    "Rules:\n"
    "- Answer using ONLY the information in the provided context below.\n"
    "- Do NOT use any outside or general knowledge about housing or UCI.\n"
    "- If the context does not contain enough information to answer the "
    "question, respond exactly with: \"I don't have enough information on "
    "that.\"\n"
    "- Do not guess, infer beyond the text, or fill gaps with assumptions.\n"
    "- Quote or paraphrase what students actually said when relevant."
)


def _build_context(hits):
    """Format retrieved chunks into a numbered context block the LLM can read.
    Each chunk is labeled with its source so the model sees where text came from."""
    blocks = []
    for i, hit in enumerate(hits, 1):
        blocks.append(f"[Context {i} — source: {hit['source']}]\n{hit['text']}")
    return "\n\n".join(blocks)


def ask(question, top_k=TOP_K):
    """Answer a question grounded in retrieved chunks.

    Returns a dict: {answer, sources, hits}
        answer  -> the LLM's grounded response (str)
        sources -> de-duplicated list of source filenames used as context
        hits    -> the raw retrieved chunks (for inspection/debugging)
    """
    hits = retrieve(question, top_k=top_k)
    context = _build_context(hits)

    user_message = (
        f"Context (student reviews):\n\n{context}\n\n"
        f"Question: {question}"
    )

    response = _client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,  # low -> stays close to the context, less invention
    )
    answer = response.choices[0].message.content.strip()

    # Source attribution built from metadata, not from the LLM. De-dupe but
    # keep retrieval order (most relevant source first).
    sources = list(dict.fromkeys(hit["source"] for hit in hits))

    return {"answer": answer, "sources": sources, "hits": hits}


if __name__ == "__main__":
    # Quick end-to-end test on a couple of queries.
    for q in [
        "What type of rooms does VDC offer and how do students feel about the space?",
        "Does PV1 have a swimming pool on the roof?",  # out-of-scope test
    ]:
        print("=" * 70)
        print(f"Q: {q}")
        result = ask(q)
        print(f"\nA: {result['answer']}")
        print(f"\nSources: {', '.join(result['sources'])}")
        print()
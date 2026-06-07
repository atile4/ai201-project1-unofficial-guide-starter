"""
ingest.py — Loads .txt documents from ./documents, cleans them, and chunks them.

Pipeline stage: Document Ingestion -> Chunking
    Reads every .txt file in the documents directory, applies light cleaning,
    then passes each document to chunk_documents() from chunking.py.

Run:
    python ingest.py
"""

import os
import re
import glob
import html

from chunking import chunk_documents

DOCUMENTS_DIR = "documents"  # relative to where you run the script (repo root)


def clean_text(text):
    """Light cleaning for text copied from web sources.

    Reviews are already mostly plain text, so this is conservative: it fixes
    HTML entities, strips any stray tags, and normalizes whitespace. It does
    NOT strip punctuation or lowercase — that would hurt embedding quality.
    """
    # Decode HTML entities like &amp; &#39; &nbsp; into real characters.
    text = html.unescape(text)
    # Remove any leftover HTML tags (e.g. <div class="review-body">).
    text = re.sub(r"<[^>]+>", "", text)
    # Collapse 3+ newlines down to a paragraph break (keeps chunking boundaries clean).
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Collapse runs of spaces/tabs.
    text = re.sub(r"[ \t]+", " ", text)
    # Trim trailing spaces on each line.
    text = "\n".join(line.strip() for line in text.split("\n"))
    return text.strip()


def load_documents(directory=DOCUMENTS_DIR):
    """Load every .txt file in `directory` into a list of {source, text} dicts."""
    pattern = os.path.join(directory, "*.txt")
    paths = sorted(glob.glob(pattern))

    if not paths:
        raise FileNotFoundError(
            f"No .txt files found in '{directory}/'. "
            f"Check the folder name and that you're running from the repo root."
        )

    documents = []
    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        cleaned = clean_text(raw)
        if not cleaned:
            print(f"  WARNING: {os.path.basename(path)} is empty after cleaning — skipping.")
            continue
        documents.append({
            "source": os.path.basename(path),  # e.g. "reddit_pv1.txt" — used for attribution
            "text": cleaned,
        })
    return documents


def build_chunks(directory=DOCUMENTS_DIR):
    """Full ingestion: load -> clean -> chunk. Returns the chunk list."""
    documents = load_documents(directory)
    print(f"Loaded {len(documents)} document(s) from '{directory}/'")

    chunks = chunk_documents(documents)
    print(f"Produced {len(chunks)} chunk(s) total\n")
    return chunks


if __name__ == "__main__":
    chunks = build_chunks()

    # --- Milestone 3 inspection: print 5 representative chunks and read them ---
    print("=" * 60)
    print("SAMPLE CHUNKS (read these — are they self-contained?)")
    print("=" * 60)
    step = max(1, len(chunks) // 5)
    for c in chunks[::step][:5]:
        print(f"\n--- {c['source']} #{c['chunk_index']} ({len(c['text'])} chars) ---")
        print(c["text"])

    # --- Milestone 3 sanity check on total count ---
    print("\n" + "=" * 60)
    n = len(chunks)
    print(f"Total chunks: {n}")
    if n < 50:
        print("NOTE: <50 chunks for ~10 docs. Chunks may be too large — "
              "consider dropping chunk_size to ~600-700 and updating planning.md.")
    elif n > 2000:
        print("NOTE: >2000 chunks. Chunks may be too small to carry meaning.")
    else:
        print("Chunk count is in the healthy range.")
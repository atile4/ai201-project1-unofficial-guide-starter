"""
chunking.py — Splits cleaned documents into overlapping chunks.

Strategy (from planning.md):
    chunk_size = 1000 characters
    overlap    = 150 characters

Reviews are paragraph-structured and vary widely in length (1-3 sentences
up to several paragraphs), so we split *recursively* on natural boundaries
— paragraphs first, then sentences, then words — instead of slicing blindly
every 1000 characters. This keeps chunks readable and self-contained while
still landing near the target size. A blind character slice would produce
mid-word fragments like "Professor Smith's exams are heavily".
"""

import re

CHUNK_SIZE = 1000
OVERLAP = 150

# Separators tried in order: paragraph break -> line break -> sentence end -> space.
SEPARATORS = ["\n\n", "\n", ". ", " "]


def _split_on_separators(text, separators):
    """Split text using the first separator that actually appears in it.
    Returns a list of pieces (separators are re-attached so we don't lose them)."""
    if not separators:
        return list(text)  # fall back to characters

    sep = separators[0]
    if sep not in text:
        return _split_on_separators(text, separators[1:])

    pieces = text.split(sep)
    # Re-attach the separator to each piece except the last, so reconstruction is clean.
    return [p + sep if i < len(pieces) - 1 else p for i, p in enumerate(pieces)]


def _hard_split(text, chunk_size):
    """Last-resort: cut text into chunk_size pieces with no regard for
    boundaries. Used only when no separator can break a piece down further,
    which guarantees recursion always terminates."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def _merge_pieces(pieces, chunk_size, overlap, separators):
    """Greedily merge small pieces up to chunk_size, then carry `overlap`
    characters of tail into the next chunk so facts spanning a boundary stay
    retrievable. `separators` shrinks with each recursion level so an oversized
    piece is always broken down further (and ultimately hard-cut)."""
    chunks = []
    current = ""

    for piece in pieces:
        # If a single piece is bigger than chunk_size, break it down further.
        if len(piece) > chunk_size:
            if current:
                chunks.append(current)
                current = ""
            if separators:
                # Try the next finer separator.
                sub = _split_on_separators(piece, separators)
                chunks.extend(_merge_pieces(sub, chunk_size, overlap, separators[1:]))
            else:
                # No separators left — force a hard character cut. Base case.
                chunks.extend(_hard_split(piece, chunk_size))
            continue

        if len(current) + len(piece) <= chunk_size:
            current += piece
        else:
            chunks.append(current)
            # Start next chunk with the overlap tail of the one we just closed.
            tail = current[-overlap:] if overlap > 0 else ""
            current = tail + piece

    if current.strip():
        chunks.append(current)

    return chunks


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """Split one document's cleaned text into overlapping chunks."""
    text = text.strip()
    if not text:
        return []

    pieces = _split_on_separators(text, SEPARATORS)
    chunks = _merge_pieces(pieces, chunk_size, overlap, SEPARATORS[1:])

    # Final cleanup: strip whitespace, drop empties (Milestone 3 checkpoint).
    return [c.strip() for c in chunks if c.strip()]


def chunk_documents(documents):
    """Chunk a collection of documents, attaching source metadata to each chunk.

    `documents` is a list of dicts: {"source": "rmp_pv1.txt", "text": "..."}.
    Returns a list of dicts ready for embedding:
        {"text": ..., "source": ..., "chunk_index": ...}
    """
    all_chunks = []
    for doc in documents:
        source = doc["source"]
        for i, chunk in enumerate(chunk_text(doc["text"])):
            all_chunks.append({
                "text": chunk,
                "source": source,
                "chunk_index": i,
            })
    return all_chunks


if __name__ == "__main__":
    # Quick self-test so you can eyeball output before wiring in real docs.
    sample = (
        "Plaza Verde 1 is very close to a bus stop, which is super convenient. "
        "However, the bus is often full by the time it reaches PV because it's "
        "the last stop on the track.\n\n"
        "The apartments themselves are clean but the walls are thin, so you can "
        "hear your neighbors. Parking is expensive and limited.\n\n"
        "Overall I'd recommend it for the location but not if you're a light sleeper."
    )
    docs = [{"source": "sample_pv1.txt", "text": sample}]
    chunks = chunk_documents(docs)
    print(f"Produced {len(chunks)} chunk(s)\n")
    for c in chunks:
        print(f"--- {c['source']} #{c['chunk_index']} ({len(c['text'])} chars) ---")
        print(c["text"])
        print()
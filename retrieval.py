"""
retrieval.py — Embeds chunks into ChromaDB and retrieves the top-k for a query.

Pipeline stage: Embedding + Vector Store -> Retrieval
    Embedding model: all-MiniLM-L6-v2 (sentence-transformers, runs locally)
    Vector store:    ChromaDB (persistent, local, no account)
    Top-k:           5 (from planning.md)

Two entry points:
    build_index()  -> embeds all chunks from ingest.py and stores them in ChromaDB
    retrieve(query) -> returns the top-k most relevant chunks with source metadata

Run `python retrieval.py` once to build the index, then it runs a few test queries.
"""

import chromadb
from sentence_transformers import SentenceTransformer

from ingest import build_chunks

EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "uci_housing"
PERSIST_DIR = "chroma_db"   # ChromaDB writes its files here; add to .gitignore
TOP_K = 5

# Load the embedding model once at import time (it's reused for both indexing
# and querying — the query must be embedded with the SAME model as the chunks).
_model = SentenceTransformer(EMBED_MODEL_NAME)

# Persistent client so the index survives between runs — no need to re-embed
# every time you start the app.
_client = chromadb.PersistentClient(path=PERSIST_DIR)


def _get_collection():
    """Get (or create) the ChromaDB collection. Cosine distance suits
    normalized sentence-transformer embeddings better than the default L2."""
    return _client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def build_index(rebuild=True):
    """Embed all chunks from the ingestion pipeline and store them in ChromaDB.

    Set rebuild=True to wipe and re-embed from scratch (use this whenever you
    change chunking). Set rebuild=False to skip if the index already has data.
    """
    if rebuild:
        # Drop any existing collection so we don't pile duplicates on re-runs.
        try:
            _client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass

    collection = _get_collection()

    if not rebuild and collection.count() > 0:
        print(f"Index already has {collection.count()} chunks — skipping rebuild.")
        return collection

    chunks = build_chunks()  # load -> clean -> chunk (from ingest.py)

    texts = [c["text"] for c in chunks]
    # Stable, unique ID per chunk so ChromaDB can address each one.
    ids = [f"{c['source']}::{c['chunk_index']}" for c in chunks]
    metadatas = [
        {"source": c["source"], "chunk_index": c["chunk_index"]}
        for c in chunks
    ]

    print(f"Embedding {len(texts)} chunks with {EMBED_MODEL_NAME}...")
    embeddings = _model.encode(texts, show_progress_bar=True).tolist()

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    print(f"Stored {collection.count()} chunks in ChromaDB at '{PERSIST_DIR}/'")
    return collection


def retrieve(query, top_k=TOP_K):
    """Embed the query and return the top_k most similar chunks.

    Returns a list of dicts: {text, source, chunk_index, distance}.
    Lower distance = more similar (cosine distance, 0 = identical).
    """
    collection = _get_collection()
    query_embedding = _model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
    )

    # ChromaDB returns parallel lists nested one level deep (one per query).
    hits = []
    for text, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        hits.append({
            "text": text,
            "source": meta["source"],
            "chunk_index": meta["chunk_index"],
            "distance": dist,
        })
    return hits


if __name__ == "__main__":
    # Build the index, then test retrieval with a few evaluation-plan queries.
    build_index(rebuild=True)

    test_queries = [
        "What do students say about PV1's bus situation?",
        "What type of rooms does VDC offer and how do students feel about the space?",
        "What are the most common complaints about Plaza Verde 2?",
    ]

    for q in test_queries:
        print("\n" + "=" * 70)
        print(f"QUERY: {q}")
        print("=" * 70)
        for hit in retrieve(q):
            preview = hit["text"][:200].replace("\n", " ")
            print(f"\n[{hit['source']} #{hit['chunk_index']}] distance={hit['distance']:.3f}")
            print(f"  {preview}...")
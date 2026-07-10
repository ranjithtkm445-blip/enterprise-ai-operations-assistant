import os

import chromadb

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge_base")
PERSIST_DIR = os.path.join(_PROJECT_ROOT, "data", "chroma")

_client = None
_collection = None


def _chunk_text(text: str, max_chars: int = 500):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    buf = ""
    for p in paragraphs:
        if buf and len(buf) + len(p) + 2 > max_chars:
            chunks.append(buf)
            buf = p
        else:
            buf = f"{buf}\n\n{p}" if buf else p
    if buf:
        chunks.append(buf)
    return chunks


def _ingest_docs(collection):
    doc_id = 0
    for fname in sorted(os.listdir(KB_DIR)):
        if not fname.endswith(".txt"):
            continue
        with open(os.path.join(KB_DIR, fname), "r", encoding="utf-8") as f:
            text = f.read()
        for chunk in _chunk_text(text):
            collection.add(documents=[chunk], ids=[f"{fname}-{doc_id}"], metadatas=[{"source": fname}])
            doc_id += 1


def get_collection():
    global _client, _collection
    if _collection is not None:
        return _collection
    os.makedirs(PERSIST_DIR, exist_ok=True)
    _client = chromadb.PersistentClient(path=PERSIST_DIR)
    _collection = _client.get_or_create_collection("company_docs")
    if _collection.count() == 0:
        _ingest_docs(_collection)
    return _collection


def search(query: str, n_results: int = 3):
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=n_results)
    return results.get("documents", [[]])[0]

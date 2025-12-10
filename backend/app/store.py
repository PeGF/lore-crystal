import os
import json
import numpy as np
from typing import List, Dict
from pathlib import Path

DATA_PATH = Path("data")
EMB_FILE = DATA_PATH / "embeddings.json"
TEXTS_DIR = DATA_PATH / "texts"
SESSIONS_DIR = "data/texts"
DATA_PATH.mkdir(exist_ok=True)
TEXTS_DIR.mkdir(exist_ok=True)

def _cosine_sim(a: np.ndarray, b: np.ndarray):
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def load_store():
    if not EMB_FILE.exists():
        return []
    with open(EMB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_store(items: List[Dict]):
    with open(EMB_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

def add_text(name: str, text: str, embedding: List[float], meta: Dict=None):
    items = load_store()
    meta = meta or {}
    item = {
        "id": len(items)+1,
        "name": name,
        "text_path": str(TEXTS_DIR / f"{name}.txt"),
        "meta": meta,
        "embedding": embedding
    }
    # save raw text
    with open(TEXTS_DIR / f"{name}.txt", "w", encoding="utf-8") as f:
        f.write(text)
    items.append(item)
    save_store(items)
    return item

def retrieve(query_embedding: List[float], top_k: int = 3):
    items = load_store()
    if not items:
        return []
    q = np.array(query_embedding, dtype=float)
    scored = []
    for it in items:
        emb = np.array(it["embedding"], dtype=float)
        score = _cosine_sim(q, emb)
        scored.append((score, it))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [it for score, it in scored[:top_k]]

def load_last_sessions(limit: int = 3):
    """
    Lê os últimos `limit` arquivos de sessão armazenados em data/texts/.
    Os arquivos devem ser nomeados como session-01.txt, session-02.txt, etc.
    """
    try:
        files = sorted(
            [f for f in os.listdir(SESSIONS_DIR) if f.endswith(".txt")],
            reverse=True  # mais recentes primeiro
        )
    except FileNotFoundError:
        return []

    files = files[:limit]

    sessions = []
    for fname in files:
        path = os.path.join(SESSIONS_DIR, fname)
        try:
            with open(path, "r", encoding="utf-8") as f:
                txt = f.read()
            sessions.append((fname.replace(".txt", ""), txt))
        except Exception:
            continue

    return sessions

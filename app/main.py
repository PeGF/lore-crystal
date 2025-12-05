import os
from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import List
from app.ai_client import create_embedding, chat_with_messages
from app.store import add_text, retrieve, load_last_sessions
from app.prompts import oracle_prompt, summarize_sessions_prompt, PERSONA_SYSTEM
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
DASHBOARD_PATH = "data/dashboard/dashboard.md"

app = FastAPI(title="Oráculo LoreCrystal")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UploadPayload(BaseModel):
    name: str
    text: str
    meta: dict = {}

@app.post("/upload-lore")
async def upload_lore(payload: UploadPayload):
    # cria embedding
    emb = create_embedding(payload.text)
    item = add_text(payload.name, payload.text, emb, meta=payload.meta)
    return {"status": "ok", "item": item}

class AskPayload(BaseModel):
    question: str
    top_k: int = 3

@app.post("/ask-oracle")
async def ask_oracle(payload: AskPayload):
    # cria embedding da pergunta
    q_emb = create_embedding(payload.question)
    hits = retrieve(q_emb, top_k=payload.top_k)
    contexts = ""
    for h in hits:
        contexts += f"### {h['name']}\n"
        try:
            with open(h['text_path'], "r", encoding="utf-8") as f:
                txt = f.read(2000)
        except Exception:
            txt = ""
        contexts += txt + "\n\n"

    messages = oracle_prompt(contexts, payload.question)
    answer = chat_with_messages(messages)
    return {"answer": answer, "hits": [h['name'] for h in hits]}

class SummPayload(BaseModel):
    session_text: str

@app.post("/update-dashboard")
def update_dashboard(limit: int = 3):
    try:
        with open(DASHBOARD_PATH, "r", encoding="utf-8") as f:
            old_panel = f.read()
    except FileNotFoundError:
        old_panel = ""

    texts = load_last_sessions(limit)

    new_sessions = "\n\n".join(
        [f"=== {name} ===\n{text}" for name, text in texts]
    )

    messages = summarize_sessions_prompt(old_panel, new_sessions)

    new_panel = chat_with_messages(messages)

    os.makedirs("data/dashboard", exist_ok=True)
    with open(DASHBOARD_PATH, "w", encoding="utf-8") as f:
        f.write(new_panel)

    return {
        "status": "ok",
        "updated": True,
        "sessions_added": [name for name, _ in texts],
        "panel": new_panel
    }

@app.get("/dashboard")
def get_dashboard():
    try:
        with open("data/dashboard/painel_atual.md", "r") as f:
            panel = f.read()
    except FileNotFoundError:
        panel = ""
    return {"panel": panel}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import List
from app.ai_client import create_embedding, chat_with_messages
from app.store import add_text, retrieve
from app.prompts import oracle_prompt, summarize_sessions_prompt, PERSONA_SYSTEM, RAG_TEMPLATE
import uvicorn

app = FastAPI(title="LoreCrystal - Oráculo da Campanha (MVP)")

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
        contexts += f"- {h['name']}: {h['text_path']}\n"
        # le o texto para incluir no contexto (pequeno)
        try:
            with open(h['text_path'], "r", encoding="utf-8") as f:
                txt = f.read(2000)  # só primeiros chars
        except Exception:
            txt = ""
        contexts += txt + "\n\n"

    messages = oracle_prompt(contexts, payload.question)
    answer = chat_with_messages(messages)
    return {"answer": answer, "hits": [h['name'] for h in hits]}

class SummPayload(BaseModel):
    session_text: str

@app.post("/summarize-sessions")
def summarize_sessions(limit: int = 3):
    session_files = [...]  

    combined_text = "\n\n".join(
        [f"=== {name} ===\n{text}" for name, text in texts]
    )

    messages = summarize_sessions_prompt(combined_text)
    summary = chat_with_messages(messages)

    return {
        "sessions_included": [name for name, _ in texts],
        "summary": summary
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

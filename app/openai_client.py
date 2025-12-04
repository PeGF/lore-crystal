import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# AI Models
EMBEDDING_MODEL = "gpt-4o-mini-embed"
LLM_MODEL = "gpt-4o-mini"

def create_embedding(text: str):
    response = openai.Embedding.create(model=EMBEDDING_MODEL, input=text)
    return resp["data"][0]["embedding"]

def chat_with_messages(messages, max_tokens=512, temperature=0.2):
    resp = openai.ChatCompletion.create(
        MODEL = LLM_MODEL,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature
    )

    return resp['choices'][0]['message']['content']
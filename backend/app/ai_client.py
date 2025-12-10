from dotenv import load_dotenv
import os
import voyageai
from groq import Groq

load_dotenv()

# Clients
voyage = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Models
EMBEDDING_MODEL = "voyage-3"  
CHAT_MODEL = "llama-3.1-8b-instant" 


# Embeddings (VoyageAI)
def create_embedding(text: str):
    resp = voyage.embed([text], model=EMBEDDING_MODEL)
    return resp.embeddings[0]


# Chat (Groq)
def chat_with_messages(messages: list[dict]):
    completion = groq.chat.completions.create(
    model=CHAT_MODEL,
    messages=messages,
    temperature=0.8,
)

    return completion.choices[0].message.content

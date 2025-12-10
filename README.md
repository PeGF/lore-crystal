# Lore Crystal — Retrieval-Augmented Generation System for RPG Campaigns

This project provides a FastAPI-based HTTP service for storing campaign texts (session logs, character sheets, notes) and querying them through a Retrieval-Augmented Generation (RAG) workflow.  
The system uses VoyageAI for vector embeddings and Groq models for text generation.

## Overview

The service performs the following tasks:

- Accepts user-submitted text documents.
- Computes embeddings for each document using VoyageAI.
- Stores the text and its embedding locally.
- Retrieves the most relevant documents for a query.
- Produces an answer using a Groq language model with the retrieved context.

## Requirements

- Python 3.10 or later  
- Virtual environment recommended  
- API keys for:  
  - VoyageAI  
  - Groq  

## Installing Dependencies and Running Server

### Clone the repository:

```bash
git clone <repository-url>
cd lore-crystal
```

### Clone the repository:

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Create a new .env file:
```ini
VOYAGE_API_KEY=your-key
GROQ_API_KEY=your-key
```

### Running the server
```bash
uvicorn app.main:app --reload --port 8000
```
Server will be available at: http://localhost:8000

### Using Docker Compose

There is a `docker-compose.yaml` at the repository root that defines `backend` and `frontend` services. Use Docker Compose to build and run both services together.

- Build and start services (Docker Compose v2+):

```bash
cd /root/lore-crystal
docker compose up --build
```

Notes:

- The `backend` service listens on port `8000` and the `frontend` (Vite) uses port `5173` by default.
- Provide API keys via a `.env` file at the repository root (example below). The included `docker-compose.yaml` does not automatically inject the `.env` into containers; to pass secrets to containers either:
  - add an `env_file` or `environment` section to the `backend` service in `docker-compose.yaml`, or
  - export the variables in your shell before running `docker compose`.

Example `docker-compose.yaml` snippet to pass `.env` into backend:

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file:
      - ./.env
```

## API Endpoints

### POST /upload-lore

Stores a document and generates its embedding.

Requested body example:
```json
{
  "name": "session-01",
  "text": "Text content..."
}
```

### POST /ask-oracle

Queries the system using RAG.

Requested body example:
```json
{
  "question": "What do we know about the Eclipse?",
  "k": 3
}
```

### POST /summarize-session
Uses LLM to summarize sessions using persona.

### Response format:

- answer: generated text from the mode
- hits: list of document identifiers used as context


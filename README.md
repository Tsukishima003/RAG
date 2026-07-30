# Real-Time RAG Assistant

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-16-000000?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6?style=flat-square&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

> **Chat with your documents using AI-powered RAG** — Lightning-fast responses with Groq Llama, real-time streaming via WebSocket, and beautiful dark mode UI.

---

## Overview

**Real-Time RAG Assistant** is a production-ready Retrieval-Augmented Generation (RAG) application that lets you upload documents and chat with them using AI. The system uses semantic search to find relevant context from your documents and generates intelligent, context-aware answers.

**Key Value Proposition**: Transform your static documents into an interactive knowledge base with sub-second response times and real-time streaming answers.

**Problem it Solves**: Eliminates the need to manually search through documents — just ask questions naturally and get accurate answers with source citations.

---

## Features

- **Groq Llama Integration** — Blazing-fast LLM responses using `llama-3.1-70b-versatile`
- **RAG Pipeline** — Intelligent document retrieval with semantic vector search
- **ChromaDB Vector Store** — Persistent vector database with Docker support
- **Real-Time Streaming** — Watch responses appear token-by-token via WebSocket
- **Multi-Format Support** — Upload PDF, DOCX, and TXT documents
- **Premium UI** — Dark mode with glassmorphism, smooth animations, and responsive design
- **Source Citations** — See exactly which documents informed each answer
- **Docker Ready** — One-command deployment with Docker Compose

## Demo

<!-- Add your screenshots/GIFs here -->
<p align="center">
  <img src="docs/images/chat-demo.gif" alt="Chat Demo" width="700"/>
</p>

<details>
<summary>More Screenshots</summary>

| Feature | Screenshot |
|---------|------------|
| Document Upload | `docs/images/upload.png` |
| Chat Interface | `docs/images/chat.png` |
| Source Citations | `docs/images/sources.png` |

</details>

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Next.js 16, React 19, TypeScript, Tailwind CSS, Radix UI |
| **Backend** | FastAPI, Python 3.8+, Uvicorn, WebSocket |
| **LLM** | Groq API (Llama 3.1 70B) |
| **Embeddings** | HuggingFace sentence-transformers |
| **Vector Store** | ChromaDB (HTTP Server Mode) |
| **Infrastructure** | Docker, Docker Compose |


## Quick Start

### Prerequisites

- **Python** 3.8 or higher
- **Node.js** 18+ and npm/pnpm
- **Docker** & Docker Compose (recommended)
- **Groq API Key** — [Get one free here](https://console.groq.com)

### Option 1: Docker Compose (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/rag-assistant.git
cd rag-assistant

# 2. Configure environment
cp backend/.env.example backend/.env
# Edit backend/.env and add your GROQ_API_KEY

# 3. Start all services
cd backend
docker compose up -d

# 4. Start the frontend
cd ../Frontend
npm install
npm run dev
```

### Option 2: Local Development

<details>
<summary>Click to expand local setup instructions</summary>

```bash
# Backend Setup
# 1. Create virtual environment
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start ChromaDB server (in separate terminal)
docker run -p 8000:8000 chromadb/chroma:0.5.23

# 4. Configure and run backend
cp .env.example .env
# Edit .env: Set GROQ_API_KEY and CHROMA_SERVER_HOST=localhost
uvicorn app.main:app --reload --port 8001

# Frontend Setup (in new terminal)
cd Frontend
npm install
npm run dev
```

</details>

---

## Quick Start

### 1. Start the Services

```bash
# Backend (http://localhost:8001)
cd backend && docker compose up -d

# Frontend (http://localhost:3000)
cd Frontend && npm run dev
```

### 2. Upload a Document

```bash
curl -X POST -F "file=@sample.pdf" http://localhost:8001/upload
```

### 3. Start Chatting

```python
import websockets
import asyncio
import json

async def chat():
    async with websockets.connect("ws://localhost:8001/ws/chat") as ws:
        await ws.send(json.dumps({"message": "What is this document about?"}))
        async for response in ws:
            print(json.loads(response))

asyncio.run(chat())
```

**Expected Output:**
```json
{
  "type": "token",
  "content": "Based on the document, this is about..."
}
```

---

## Usage

### Uploading Documents

| Method | Command |
|--------|---------|
| **cURL** | `curl -X POST -F "file=@document.pdf" http://localhost:8001/upload` |
| **UI** | Drag & drop files or click the upload area |

**Supported Formats:** PDF, DOCX, TXT

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info and status |
| `/health` | GET | Health check with stats |
| `/upload` | POST | Upload and process document |
| `/chat` | POST | Non-streaming chat |
| `/ws/chat` | WebSocket | Real-time streaming chat |
| `/documents/count` | GET | Get indexed document count |
| `/documents` | DELETE | Clear all documents |

### WebSocket Chat

```javascript
const ws = new WebSocket('ws://localhost:8001/ws/chat');

ws.onopen = () => {
  ws.send(JSON.stringify({ message: "Your question here" }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'token') {
    console.log(data.content); // Stream tokens
  }
};
```

---

## Project Structure

```
RAG LC/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config/              # Settings & CORS
│   │   ├── core/                # RAG engine components
│   │   │   ├── rag_engine.py    # Main RAG orchestrator
│   │   │   ├── embeddings.py    # Embedding generation
│   │   │   ├── vector_store.py  # ChromaDB integration
│   │   │   ├── llm.py           # Groq LLM wrapper
│   │   │   └── query_engine.py  # Query processing
│   │   ├── routes/              # API endpoints
│   │   ├── services/            # Business logic
│   │   ├── models/              # Pydantic schemas
│   │   └── utils/               # Helpers & validators
│   ├── compose.yaml             # Docker Compose config
│   ├── Dockerfile               # Backend container
│   ├── requirements.txt         # Python dependencies
│   └── .env.example             # Environment template
│
├── Frontend/
│   ├── app/                     # Next.js app router
│   ├── components/              # React components (Radix UI)
│   ├── hooks/                   # Custom React hooks
│   ├── lib/                     # Utilities
│   ├── styles/                  # Global styles
│   ├── package.json             # Node dependencies
│   └── tailwind.config.ts       # Tailwind configuration
│
└── README.md                    # You are here
```

---

## Configuration

### Environment Variables

Create `backend/.env` from the template:

```env
# Required
GROQ_API_KEY=your_groq_api_key_here

# Groq Model Configuration
GROQ_MODEL=llama-3.1-70b-versatile

# ChromaDB Server (Docker)
CHROMA_SERVER_HOST=chromadb
CHROMA_SERVER_PORT=8000
CHROMA_COLLECTION_NAME=documents

# Server Settings
HOST=0.0.0.0
PORT=8000

# Document Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```
## Testing

### API Health Check

```bash
# Backend health
curl http://localhost:8001/health

# ChromaDB heartbeat
curl http://localhost:8000/api/v1/heartbeat
```

### Run Tests

```bash
cd backend
pytest tests/ -v
```

### API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

---

## Docker Commands

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f backend
docker compose logs -f chromadb

# Restart backend only
docker compose restart backend

# Rebuild and restart
docker compose up -d --build

# Stop all services
docker compose down

# Stop and remove volumes (WARNING: deletes data)
docker compose down -v
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [LangChain](https://langchain.com) — RAG framework
- [Groq](https://groq.com) — Ultra-fast LLM inference
- [ChromaDB](https://trychroma.com) — Vector database
- [FastAPI](https://fastapi.tiangolo.com) — Modern Python web framework
- [Next.js](https://nextjs.org) — React framework
- [shadcn/ui](https://ui.shadcn.com) — UI components

---

<p align="center">
  Made with care by Your Name
  <br>
  Star this repo if you find it helpful!
</p>

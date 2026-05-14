# 🧬 BioGuru AI — NEET Biology AI Tutor

A production-ready, multilingual AI tutor for NEET Biology (Class 11 & 12) powered by **Claude claude-sonnet-4-20250514**, **RAG (Retrieval-Augmented Generation)**, and **ChromaDB**.

---

## ✨ Features

- 🤖 **AI Chat** — Ask Biology questions in English, Hindi, Hinglish, or Urdu
- 📖 **RAG Pipeline** — Answers grounded in NCERT textbooks (anti-hallucination)
- 📝 **NEET Practice Mode** — AI-generated MCQs with NEET marking scheme (+4/−1)
- 🌐 **Multilingual** — Auto-detects language; supports Devanagari & Urdu script
- 🎤 **Voice Input** — Whisper STT + TTS output
- 📊 **Dashboard** — Track progress, score trends, weak topics
- 👤 **Admin Panel** — Upload PDFs to expand the knowledge base
- 🔐 **JWT Auth** — Secure authentication with rate limiting

---

## 🚀 Quick Start (Docker)

### 1. Clone & Configure

```bash
git clone https://github.com/yourorg/bioguru-ai.git
cd bioguru-ai
cp .env.example .env
# Edit .env — add your ANTHROPIC_API_KEY and SECRET_KEY
nano .env
```

### 2. Launch All Services

```bash
docker-compose up -d --build
```

This starts: **Frontend** (port 3000), **Backend** (port 8000), **ChromaDB** (port 8001), **PostgreSQL**, **Redis**, **Nginx** (port 80).

### 3. Initialize Database

```bash
docker-compose exec backend python -c "
import asyncio
from models.database import init_db
asyncio.run(init_db())
print('Database initialized!')
"
```

### 4. (Optional) Ingest NCERT PDFs

Place PDFs in `data/ncert/class11/` and `data/ncert/class12/`, then:

```bash
docker-compose exec backend python rag/ingest_ncert.py --source data/ncert/class11 --class 11
docker-compose exec backend python rag/ingest_ncert.py --source data/ncert/class12 --class 12
```

### 5. Access the App

- **App**: http://localhost (via Nginx)
- **Frontend direct**: http://localhost:3000
- **API docs**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/health

---

## 📁 Project Structure

```
bioguru-ai/
├── backend/          # FastAPI — Auth, Chat, NEET, Voice, Analytics
├── frontend/         # Next.js 14 — Chat UI, NEET, Dashboard, Admin
├── rag/              # RAG Pipeline — PDF ingestion, embeddings, retrieval
├── data/             # NCERT PDFs, glossaries
├── docker/           # Dockerfiles + nginx config
├── docker-compose.yml
└── .env.example
```

---

## 🌍 Multilingual Support

| Language | Script | Example |
|----------|--------|---------|
| English | Latin | "What is photosynthesis?" |
| Hindi | Devanagari | "प्रकाश संश्लेषण क्या है?" |
| Hinglish | Latin | "Mitochondria kya karta hai?" |
| Urdu | Nastaliq | "مائٹوکانڈریا کیا ہے؟" |

---

## ⚙️ Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | ✅ | JWT secret (use a long random string) |
| `ANTHROPIC_API_KEY` | ✅ | Claude API key |
| `DB_PASSWORD` | ✅ | PostgreSQL password |
| `OPENAI_API_KEY` | Optional | For Whisper STT + TTS voice features |
| `GROQ_API_KEY` | Optional | Fallback LLM |

---

## 🏗️ Architecture

```
Nginx (80) → Frontend (3000) + Backend (8000)
Backend → ChromaDB (RAG) + PostgreSQL (users/progress) + Redis (cache/rate-limit)
Backend → Anthropic Claude API (LLM)
```

---

## 📖 API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/register` | Register user |
| POST | `/api/auth/login` | Login → JWT token |
| POST | `/api/chat/message` | Chat (streaming SSE) |
| POST | `/api/neet/generate` | Generate MCQs |
| POST | `/api/neet/submit` | Submit test answers |
| GET | `/api/neet/progress` | Student progress |
| GET | `/api/analytics/dashboard` | Dashboard stats |
| POST | `/api/upload/pdf` | Upload PDF (admin) |
| POST | `/api/voice/transcribe` | STT via Whisper |
| POST | `/api/voice/speak` | TTS output |

Full docs: http://localhost:8000/docs

---

## 🔒 Security

- All routes protected with JWT Bearer tokens
- Rate limiting: 30 requests/min per user (Redis-backed)
- SQL via ORM (no injection risk)
- Passwords hashed with bcrypt
- API keys stored in env vars only

---

*BioGuru AI — Ek smart Biology teacher, jo 24/7 available hai!* 🧬

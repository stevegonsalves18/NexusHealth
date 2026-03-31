# NexusHealth — Clinical AI Platform

> FastAPI · React.js · LangGraph · PostgreSQL · Docker · JWT

A HIPAA-oriented clinical AI platform featuring 6 hospital operation modules and a multi-agent RAG chatbot for intelligent clinical reasoning.

---

## Key Features

### 🏥 6 Hospital Operation Modules
| Module | Description |
|--------|-------------|
| **Appointment Booking** | Schedule, reschedule, and cancel patient appointments with conflict detection |
| **Patient Vitals Monitoring** | Track vital observations (BP, heart rate, SpO2) with real-time clinical alerts |
| **Billing** | Invoice generation, payment tracking, and billable service management |
| **Pharmacy** | Prescription management, medication inventory, and dispense tracking |
| **Discharge Workflows** | Structured discharge summaries with follow-up instructions |
| **Role-Based Access Control** | Admin panel with user management, audit logs, and role-based permissions |

### 🤖 Multi-Agent RAG Chatbot
- Built using **LangGraph** and **Agentic AI** patterns
- Orchestrates intelligent clinical reasoning across multiple specialized agents
- **Patient History Retrieval** — pulls relevant medical records for context-aware responses
- **Personalized Health Insights** — generates tailored health advice based on prediction history
- **Streaming Responses** — real-time Server-Sent Events for ChatGPT-like UX

### 🧠 ML Disease Risk Prediction
- 5 trained scikit-learn models: Diabetes, Heart Disease, Kidney Disease, Liver Disease, Lung Disease
- **SHAP Explainability** — transparent feature importance for every prediction
- **ONNX Runtime** — browser-side inference for instant predictions
- **PDF Report Generation** — downloadable medical reports

### 🔐 Security
- JWT token authentication with bcrypt password hashing
- Rate limiting middleware
- Security headers (X-Frame-Options, CSP, etc.)
- HIPAA-oriented data handling practices

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React, TypeScript, Vite, TailwindCSS |
| Backend | Python, FastAPI, SQLAlchemy |
| AI/ML | scikit-learn, LangGraph, SHAP, ONNX Runtime |
| Database | PostgreSQL (prod) / SQLite (dev) |
| Infrastructure | Docker, Docker Compose |
| Auth | JWT (python-jose), bcrypt |

---

## Project Structure

```
NexusHealth/
├── backend/
│   ├── main.py              # FastAPI entrypoint with all route registrations
│   ├── auth.py              # JWT authentication & RBAC
│   ├── prediction.py        # ML prediction endpoints (5 diseases)
│   ├── chat.py              # AI chat endpoints
│   ├── streaming_chat.py    # SSE streaming responses
│   ├── chat_context.py      # Context builder for RAG
│   ├── rag.py               # RAG pipeline with retrieval
│   ├── agent.py             # Agent orchestrator
│   ├── agents/              # Specialized agents (safety, scheduling, scribe)
│   ├── appointments.py      # Appointment booking module
│   ├── care_events.py       # Patient vitals & monitoring
│   ├── billing.py           # Billing & invoicing
│   ├── pharmacy.py          # Prescription & inventory
│   ├── discharge.py         # Discharge workflow
│   ├── admin.py             # Admin panel & RBAC
│   ├── explainability.py    # SHAP explanations
│   ├── database.py          # SQLAlchemy setup
│   ├── middleware.py         # Security, logging, rate limiting
│   ├── models/              # ORM models
│   └── schemas/             # Pydantic validation schemas
├── frontend/
│   └── src/
│       ├── pages/           # React pages (Login, Dashboard, Predict, etc.)
│       ├── components/      # Reusable UI components
│       └── lib/             # API clients & utilities
├── data/                    # Training datasets
├── Dockerfile               # Container image
├── docker-compose.yml       # Multi-service orchestration
└── requirements.txt
```

---

## How to Run

### With Docker
```bash
docker-compose up --build
```

### Without Docker
```bash
# Backend
pip install -r requirements.txt
cd backend
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

---

## Author

**Steve Gonsalves**

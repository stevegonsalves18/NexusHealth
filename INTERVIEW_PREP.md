# NexusHealth — Interview Prep Deck 🎯

Use this to confidently walk through every part of the project in an interview.

---

## 1. Elevator Pitch (30 seconds)

> "NexusHealth is a HIPAA-oriented clinical AI platform I built using FastAPI, React, and LangGraph. It has 6 hospital operation modules — appointment booking, patient vitals monitoring, billing, pharmacy, discharge workflows, and role-based access control. I also integrated a multi-agent RAG chatbot that uses agentic AI to retrieve patient history and provide personalized health insights. On the ML side, it predicts risk for 5 diseases using scikit-learn models with SHAP explainability. The whole thing is containerized with Docker."

---

## 2. Architecture Diagram

```
┌─────────────────────────┐       REST API        ┌───────────────────────────────┐
│    React Frontend       │ ◄──────────────────► │     FastAPI Backend            │
│    (Vite + TypeScript)  │                       │                               │
│                         │                       │  ┌─ Auth (JWT + RBAC)         │
│  Pages:                 │   /v1/auth/*          │  ├─ Appointments              │
│  • Login / Signup       │   /v1/appointments/*  │  ├─ Patient Vitals            │
│  • Dashboard            │   /v1/care-events/*   │  ├─ Billing                   │
│  • Predictions (5)      │   /v1/billing/*       │  ├─ Pharmacy                  │
│  • Profile              │   /v1/pharmacy/*      │  ├─ Discharge                 │
│                         │   /v1/discharge/*     │  ├─ Admin (RBAC)              │
│                         │   /v1/predict/*       │  ├─ ML Predictions (5 models) │
│                         │   /v1/chat/*          │  ├─ RAG Chat (LangGraph)      │
│                         │   /v1/explain/*       │  └─ PDF Reports               │
└─────────────────────────┘                       └──────────┬────────────────────┘
                                                             │
                                              ┌──────────────┼──────────────┐
                                              │              │              │
                                     ┌────────▼───┐  ┌──────▼─────┐  ┌────▼──────┐
                                     │ PostgreSQL  │  │ ML Models  │  │  Agent    │
                                     │ / SQLite    │  │ (.pkl)     │  │  System   │
                                     │             │  │ 5 diseases │  │ LangGraph │
                                     └─────────────┘  └────────────┘  └───────────┘
```

---

## 3. The 6 Hospital Modules (Your Resume Says This)

### Module 1: Appointment Booking (`appointments.py`)
**What it does:** CRUD for patient appointments with doctor assignment and conflict detection.

**How to explain:**
> "I built an appointment booking system where patients can schedule, reschedule, and cancel appointments. It checks for time slot conflicts and assigns doctors based on department. The data is stored in the Appointment table linked to the User model."

---

### Module 2: Patient Vitals Monitoring (`care_events.py`)
**What it does:** Tracks vital observations (blood pressure, heart rate, SpO2, temperature) and generates clinical alerts when vitals are abnormal.

**How to explain:**
> "This module records patient vital signs — like blood pressure and heart rate — as VitalObservation entries. If a reading is outside the normal range, it automatically creates a ClinicalAlert. The frontend polls for these alerts and displays them on the dashboard."

---

### Module 3: Billing (`billing.py`)
**What it does:** Manages invoices, billable services, line items, and payment tracking.

**How to explain:**
> "I implemented a billing system with Invoice and BillableService models. When a patient receives care, the system creates an invoice with line items. Payments are tracked separately and linked back to invoices. It supports partial payments and outstanding balance calculation."

---

### Module 4: Pharmacy (`pharmacy.py`)
**What it does:** Prescription management, medication inventory tracking, and dispense records.

**How to explain:**
> "The pharmacy module handles the full medication lifecycle. Doctors create Prescriptions with PrescriptionItems. The system checks MedicationInventory for stock. When medication is dispensed, it creates a DispenseRecord and automatically decrements inventory."

---

### Module 5: Discharge Workflows (`discharge.py`)
**What it does:** Generates structured discharge summaries with diagnosis, treatment performed, medications prescribed, and follow-up instructions.

**How to explain:**
> "When a patient is ready to leave, the discharge module generates a DischargeSummary. It includes the admitting diagnosis, procedures performed, medications to continue at home, and follow-up appointment dates. Doctors can also add free-text instructions."

---

### Module 6: Role-Based Access Control (`admin.py` + `auth.py`)
**What it does:** Admin panel with user management, role assignment (admin/doctor/nurse/patient), and audit logging.

**How to explain:**
> "I implemented RBAC with 4 roles: admin, doctor, nurse, and patient. Each API endpoint checks the user's role before allowing access. For example, only admins can manage users, only doctors can create prescriptions, and patients can only see their own data. Every sensitive action is logged in the AuditLog table."

---

## 4. Multi-Agent RAG Chatbot (Your Resume Says This)

### How the RAG Pipeline Works (`rag.py` + `chat_context.py`)

**How to explain:**
> "I built a Retrieval-Augmented Generation pipeline. When a user sends a chat message, the system first retrieves relevant context — their past predictions, vital signs, and conversation history — from the database. This context is injected into the prompt before sending it to the LLM. This way the AI gives personalized answers based on the patient's actual medical history, not generic responses."

### How the Agent System Works (`agent.py` + `agents/`)

**How to explain:**
> "I used the agentic AI pattern inspired by LangGraph. There's a main orchestrator agent that receives the user's message and decides which specialized agent to route it to:
> - **SafetyAgent** — checks if responses are medically safe before returning them
> - **SchedulingAgent** — handles appointment-related queries
> - **ScribeAgent** — summarizes conversations into structured medical notes
> - **AdvisoryBoard** — provides multi-perspective clinical reasoning
> 
> Each agent inherits from BaseAgent which handles lifecycle management, step-by-step reasoning logs, and execution telemetry."

### Streaming Responses (`streaming_chat.py`)

**How to explain:**
> "For a ChatGPT-like experience, I implemented Server-Sent Events. Instead of waiting for the full response, the AI streams tokens in real-time using FastAPI's StreamingResponse with async generators."

---

## 5. ML Prediction Engine

### How Predictions Work (`prediction.py`)

> "I trained 5 scikit-learn models on medical datasets from Kaggle. Each model is serialized with pickle and loaded into memory on startup. The user fills out a health form, the data gets validated by Pydantic schemas, passed to the model as a numpy array, and the model returns a prediction with a probability score."

### SHAP Explainability (`explainability.py`)

> "I integrated SHAP to make predictions interpretable. After a prediction, SHAP calculates which input features contributed most. For example: 'Your high glucose level contributed 42% to the diabetes risk score.' This is critical in healthcare where black-box models aren't trusted."

---

## 6. Security & Infrastructure

### JWT Authentication
> "I used python-jose for JWT tokens and passlib with bcrypt for password hashing. Tokens expire after a set time. The `get_current_user` FastAPI dependency validates the token on every request."

### Middleware Stack
> "Three custom middleware layers: LoggingMiddleware logs every request with timing, SecurityHeadersMiddleware adds OWASP headers, and RateLimitMiddleware prevents API abuse by tracking requests per IP."

### Docker
> "The project has a Dockerfile and docker-compose.yml. The backend runs as a Python container and the frontend as a Node container. In production, you'd add a PostgreSQL service. For local dev, it falls back to SQLite."

---

## 7. Common Interview Questions

### "Why FastAPI over Flask/Django?"
> "FastAPI has built-in async support, automatic OpenAPI documentation, Pydantic validation, and native streaming — all of which I needed for the chat feature and ML endpoints."

### "Why LangGraph for the agents?"
> "LangGraph provides a graph-based orchestration framework for multi-agent systems. It lets me define agent workflows as nodes and edges, making it easy to route messages to the right specialized agent and compose complex reasoning chains."

### "How do you handle HIPAA compliance?"
> "I implemented role-based access control, audit logging for every sensitive action, encrypted passwords, secure JWT tokens, and security headers. The data stays within the system — no patient data is sent to external APIs."

### "How does the RAG retrieval work?"
> "The chat_context module queries the database for the user's recent health records, prediction results, and chat history. This context is concatenated into the system prompt so the LLM has relevant patient information when generating a response."

### "Can you scale this?"
> "Yes — the backend is containerized with Docker, the database layer supports PostgreSQL for production, and FastAPI is async-ready for concurrent requests. You'd add Redis for caching and a load balancer in front."

---

## 8. Resume Bullets (Copy-Paste Ready)

```
Nexus Health | FastAPI, React.js, LangGraph, PostgreSQL, Docker, JWT

• Deployed a HIPAA-oriented clinical AI platform featuring 6 hospital operation 
  modules — appointment booking, patient vitals monitoring, billing, pharmacy, 
  discharge workflows, and role-based access control.

• Integrated multi-agent RAG chatbot using LangGraph and Agentic AI, orchestrating 
  intelligent clinical reasoning for patient history retrieval and personalized 
  health insights.

• Trained 5 disease prediction models (Diabetes, Heart, Kidney, Liver, Lungs) with 
  scikit-learn and added SHAP explainability for transparent clinical decision support.

• Implemented JWT authentication, rate limiting middleware, and security headers 
  following HIPAA-oriented data handling practices.
```

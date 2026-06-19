"""NexusHealth - Clinical AI Platform Backend"""
import logging
import os
import sys
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from . import (
    admin,
    appointments,
    auth,
    billing,
    care_events,
    chat,
    database,
    discharge,
    explanation,
    models,
    monitoring,
    pharmacy,
    prediction,
    report,
    streaming_chat,
)
from .middleware import LoggingMiddleware, RateLimitMiddleware, SecurityHeadersMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown logic."""
    logger.info("Starting NexusHealth API...")

    # Create database tables
    try:
        models.Base.metadata.create_all(bind=database.engine)
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.warning("Database setup issue: %s", e)

    # Load ML models
    try:
        prediction.initialize_models()
        logger.info("ML models loaded successfully.")
    except Exception as e:
        logger.warning("Failed to load ML models: %s", e)

    yield
    logger.info("Shutting down NexusHealth API.")


app = FastAPI(title="NexusHealth API", default_response_class=JSONResponse, lifespan=lifespan)

# Middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Routes ---
API_V1 = "/v1"

# Core
app.include_router(auth.router, prefix=API_V1, tags=["Auth"])
app.include_router(prediction.router, prefix=API_V1, tags=["Prediction"])
app.include_router(explanation.router, prefix=API_V1, tags=["Explainability"])

# AI Chat (Multi-Agent RAG)
app.include_router(chat.router, prefix=API_V1, tags=["Chat"])
app.include_router(streaming_chat.router, prefix=API_V1, tags=["Streaming Chat"])

# Hospital Operations (6 modules)
app.include_router(appointments.router, prefix=API_V1, tags=["Appointments"])
app.include_router(care_events.router, prefix=API_V1, tags=["Patient Vitals"])
app.include_router(billing.router, prefix=API_V1, tags=["Billing"])
app.include_router(pharmacy.router, prefix=API_V1, tags=["Pharmacy"])
app.include_router(discharge.router, prefix=API_V1, tags=["Discharge"])
app.include_router(admin.router, prefix=API_V1, tags=["Admin / RBAC"])

# Reports & Monitoring
app.include_router(report.router, prefix=API_V1, tags=["Reports"])
app.include_router(monitoring.router, prefix=API_V1, tags=["Monitoring"])


@app.get("/")
def root():
    return {"message": "NexusHealth Clinical AI Platform is running"}


@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.post("/generate_report")
async def generate_report(
    request: Request,
    current_user: models.User = Depends(auth.get_current_user),
):
    """Generate a PDF medical report for the authenticated user."""
    try:
        from .pdf_service import generate_medical_report
        data = await request.json()
        pdf = generate_medical_report(
            user_name=current_user.full_name or current_user.username,
            report_type=data.get("report_type", "General"),
            prediction=data.get("prediction", "N/A"),
            data=data.get("data", {}),
            advice=data.get("advice", [])
        )
        return Response(content=pdf, media_type="application/pdf")
    except Exception:
        logger.error("Generate report failed")
        raise HTTPException(status_code=500, detail="Failed to generate report")

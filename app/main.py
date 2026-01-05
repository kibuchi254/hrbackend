from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine
from app.models import models

# Import routers directly from their modules (avoid circular imports)
from app.api.v1 import auth
from app.api.v1 import admin
from app.api.v1 import company
from app.api.v1 import hr
from app.api.v1 import payroll
from app.api.v1 import recruitment
from app.api.v1 import ai

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A comprehensive HR & Payroll SaaS API"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with correct prefix
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(admin.router, prefix="/api/v1/super-admin", tags=["Super Admin"])
app.include_router(company.router, prefix="/api/v1/company", tags=["Company"])
app.include_router(hr.router, prefix="/api/v1/hr", tags=["HR"])
app.include_router(payroll.router, prefix="/api/v1/payroll", tags=["Payroll"])
app.include_router(recruitment.router, prefix="/api/v1/recruitment", tags=["Recruitment"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["AI Features"])


@app.get("/")
async def root():
    return {
        "message": "HR & Payroll SaaS API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
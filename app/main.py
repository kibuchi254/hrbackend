from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine
from app.models import models
from app.api import auth, admin, company, hr, payroll, recruitment, ai

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

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["Authentication"])
app.include_router(admin.router, prefix=f"{settings.API_V1_PREFIX}/super-admin", tags=["Super Admin"])
app.include_router(company.router, prefix=f"{settings.API_V1_PREFIX}/company", tags=["Company"])
app.include_router(hr.router, prefix=f"{settings.API_V1_PREFIX}/hr", tags=["HR"])
app.include_router(payroll.router, prefix=f"{settings.API_V1_PREFIX}/payroll", tags=["Payroll"])
app.include_router(recruitment.router, prefix=f"{settings.API_V1_PREFIX}/recruitment", tags=["Recruitment"])
app.include_router(ai.router, prefix=f"{settings.API_V1_PREFIX}/ai", tags=["AI Features"])


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

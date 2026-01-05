from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import time
from app.core.database import get_db
from app.core.deps import get_current_user, verify_company_access
from app.core.deps import get_current_company_admin
from app.services.ai_service import get_ai_service
from app.schemas.schemas import (
    GenerateJobDescriptionRequest, AnalyzeCandidateRequest,
    GenerateInterviewQuestionsRequest, AnalyzeInterviewRequest,
    GenerateSalaryInsightsRequest, PerformanceReviewRequest, AIResponse
)

router = APIRouter()


# ========== AI Features ==========
@router.post("/generate-job-description", response_model=AIResponse)
async def generate_job_description(
    request: GenerateJobDescriptionRequest,
    current_user: dict = Depends(verify_company_access),
    db: Session = Depends(get_db)
):
    """Generate AI-powered job description using Gemini or Claude"""
    company_id = current_user["company_id"]

    # Get AI service (use Gemini by default)
    ai_service = get_ai_service(company_id=company_id, provider="gemini")

    try:
        start_time = time.time()

        # Call AI service
        result = await ai_service.generate_job_description(
            job_title=request.job_title,
            requirements=request.requirements,
            skills=request.skills,
            experience_level=request.experience_level,
            company_name=request.company_name
        )

        processing_time = int((time.time() - start_time) * 1000)

        return AIResponse(
            success=True,
            data=result,
            tokens_used=None,
            processing_time_ms=processing_time
        )
    except Exception as e:
        return AIResponse(
            success=False,
            data={},
            message=f"Failed to generate job description: {str(e)}"
        )


@router.post("/analyze-candidate", response_model=AIResponse)
async def analyze_candidate(
    request: AnalyzeCandidateRequest,
    current_user: dict = Depends(verify_company_access),
    db: Session = Depends(get_db)
):
    """Analyze candidate resume using AI"""
    company_id = current_user["company_id"]

    ai_service = get_ai_service(company_id=company_id, provider="gemini")

    try:
        start_time = time.time()

        result = await ai_service.analyze_candidate(
            resume_text=request.resume_text,
            job_requirements=request.job_requirements,
            job_description=request.job_description
        )

        processing_time = int((time.time() - start_time) * 1000)

        return AIResponse(
            success=True,
            data=result,
            tokens_used=None,
            processing_time_ms=processing_time
        )
    except Exception as e:
        return AIResponse(
            success=False,
            data={},
            message=f"Failed to analyze candidate: {str(e)}"
        )


@router.post("/generate-interview-questions", response_model=AIResponse)
async def generate_interview_questions(
    request: GenerateInterviewQuestionsRequest,
    current_user: dict = Depends(verify_company_access),
    db: Session = Depends(get_db)
):
    """Generate AI-powered interview questions"""
    company_id = current_user["company_id"]

    ai_service = get_ai_service(company_id=company_id, provider="claude")

    try:
        start_time = time.time()

        result = await ai_service.generate_interview_questions(
            job_title=request.job_title,
            job_description=request.job_description,
            candidate_profile=request.candidate_profile,
            interview_type=request.interview_type
        )

        processing_time = int((time.time() - start_time) * 1000)

        return AIResponse(
            success=True,
            data=result,
            tokens_used=None,
            processing_time_ms=processing_time
        )
    except Exception as e:
        return AIResponse(
            success=False,
            data={},
            message=f"Failed to generate interview questions: {str(e)}"
        )


@router.post("/analyze-interview", response_model=AIResponse)
async def analyze_interview(
    request: AnalyzeInterviewRequest,
    current_user: dict = Depends(verify_company_access),
    db: Session = Depends(get_db)
):
    """Analyze interview transcript using AI"""
    company_id = current_user["company_id"]

    ai_service = get_ai_service(company_id=company_id, provider="claude")

    try:
        start_time = time.time()

        result = await ai_service.analyze_interview(
            interview_transcript=request.interview_transcript,
            job_requirements=request.job_requirements
        )

        processing_time = int((time.time() - start_time) * 1000)

        return AIResponse(
            success=True,
            data=result,
            tokens_used=None,
            processing_time_ms=processing_time
        )
    except Exception as e:
        return AIResponse(
            success=False,
            data={},
            message=f"Failed to analyze interview: {str(e)}"
        )


@router.post("/generate-salary-insights", response_model=AIResponse)
async def generate_salary_insights(
    request: GenerateSalaryInsightsRequest,
    current_user: dict = Depends(verify_company_access),
    db: Session = Depends(get_db)
):
    """Generate AI-powered salary insights"""
    company_id = current_user["company_id"]

    ai_service = get_ai_service(company_id=company_id, provider="gemini")

    try:
        start_time = time.time()

        result = await ai_service.generate_salary_insights(
            job_title=request.job_title,
            location=request.location,
            experience_level=request.experience_level,
            skills=request.skills
        )

        processing_time = int((time.time() - start_time) * 1000)

        return AIResponse(
            success=True,
            data=result,
            tokens_used=None,
            processing_time_ms=processing_time
        )
    except Exception as e:
        return AIResponse(
            success=False,
            data={},
            message=f"Failed to generate salary insights: {str(e)}"
        )


@router.post("/performance-review", response_model=AIResponse)
async def generate_performance_review(
    request: PerformanceReviewRequest,
    current_user: dict = Depends(verify_company_access),
    db: Session = Depends(get_db)
):
    """Generate AI-powered performance review suggestions"""
    company_id = current_user["company_id"]

    ai_service = get_ai_service(company_id=company_id, provider="claude")

    try:
        start_time = time.time()

        result = await ai_service.get_performance_review_suggestions(
            employee_name=request.employee_name,
            role=request.role,
            achievements=request.achievements,
            areas_for_improvement=request.areas_for_improvement
        )

        processing_time = int((time.time() - start_time) * 1000)

        return AIResponse(
            success=True,
            data=result,
            tokens_used=None,
            processing_time_ms=processing_time
        )
    except Exception as e:
        return AIResponse(
            success=False,
            data={},
            message=f"Failed to generate performance review: {str(e)}"
        )


@router.get("/config", response_model=dict)
async def get_ai_config(
    current_user: dict = Depends(verify_company_access),
    db: Session = Depends(get_db)
):
    """Get AI configuration for company"""
    from app.models.models import AIModelConfig

    company_id = current_user["company_id"]
    config = db.query(AIModelConfig).filter(AIModelConfig.company_id == company_id).first()

    if not config:
        # Return default configuration
        return {
            "company_id": company_id,
            "gemini_enabled": False,
            "gemini_model": "gemini-pro",
            "claude_enabled": False,
            "claude_model": "claude-3-sonnet",
            "auto_screening_enabled": False,
            "auto_interview_questions_enabled": False,
            "ai_job_description_enabled": True,
            "ai_candidate_matching_enabled": True,
            "monthly_token_limit": 100000,
            "monthly_tokens_used": 0
        }

    return {
        "company_id": config.company_id,
        "gemini_enabled": config.gemini_enabled,
        "gemini_model": config.gemini_model,
        "claude_enabled": config.claude_enabled,
        "claude_model": config.claude_model,
        "auto_screening_enabled": config.auto_screening_enabled,
        "auto_interview_questions_enabled": config.auto_interview_questions_enabled,
        "ai_job_description_enabled": config.ai_job_description_enabled,
        "ai_candidate_matching_enabled": config.ai_candidate_matching_enabled,
        "monthly_token_limit": config.monthly_token_limit,
        "monthly_tokens_used": config.monthly_tokens_used
    }


@router.put("/config")
async def update_ai_config(
    config_data: dict,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Update AI configuration for company"""
    from app.models.models import AIModelConfig

    company_id = current_user["company_id"]
    config = db.query(AIModelConfig).filter(AIModelConfig.company_id == company_id).first()

    if not config:
        # Create new config
        config = AIModelConfig(
            company_id=company_id,
            gemini_enabled=config_data.get("gemini_enabled", False),
            gemini_api_key=config_data.get("gemini_api_key", ""),
            gemini_model=config_data.get("gemini_model", "gemini-pro"),
            claude_enabled=config_data.get("claude_enabled", False),
            claude_api_key=config_data.get("claude_api_key", ""),
            claude_model=config_data.get("claude_model", "claude-3-sonnet"),
            auto_screening_enabled=config_data.get("auto_screening_enabled", False),
            auto_interview_questions_enabled=config_data.get("auto_interview_questions_enabled", False),
            ai_job_description_enabled=config_data.get("ai_job_description_enabled", True),
            ai_candidate_matching_enabled=config_data.get("ai_candidate_matching_enabled", True),
            monthly_token_limit=config_data.get("monthly_token_limit", 100000)
        )
        db.add(config)
        db.commit()
        db.refresh(config)
    else:
        # Update existing config
        if "gemini_enabled" in config_data:
            config.gemini_enabled = config_data["gemini_enabled"]
        if "gemini_api_key" in config_data:
            config.gemini_api_key = config_data["gemini_api_key"]
        if "gemini_model" in config_data:
            config.gemini_model = config_data["gemini_model"]
        if "claude_enabled" in config_data:
            config.claude_enabled = config_data["claude_enabled"]
        if "claude_api_key" in config_data:
            config.claude_api_key = config_data["claude_api_key"]
        if "claude_model" in config_data:
            config.claude_model = config_data["claude_model"]
        if "auto_screening_enabled" in config_data:
            config.auto_screening_enabled = config_data["auto_screening_enabled"]
        if "auto_interview_questions_enabled" in config_data:
            config.auto_interview_questions_enabled = config_data["auto_interview_questions_enabled"]
        if "ai_job_description_enabled" in config_data:
            config.ai_job_description_enabled = config_data["ai_job_description_enabled"]
        if "ai_candidate_matching_enabled" in config_data:
            config.ai_candidate_matching_enabled = config_data["ai_candidate_matching_enabled"]
        if "monthly_token_limit" in config_data:
            config.monthly_token_limit = config_data["monthly_token_limit"]

        db.commit()
        db.refresh(config)

    return {
        "message": "AI configuration updated successfully",
        "config": {
            "company_id": config.company_id,
            "gemini_enabled": config.gemini_enabled,
            "claude_enabled": config.claude_enabled
        }
    }

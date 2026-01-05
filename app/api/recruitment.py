from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.core.database import get_db
from app.core.deps import get_current_user, verify_company_access, get_current_company_admin
from app.crud.crud_recruitment import (
    get_job_posting, get_job_postings_by_company, get_published_job_postings,
    create_job_posting, update_job_posting, delete_job_posting, publish_job_posting,
    get_candidate, get_candidates,
    create_candidate, update_candidate, delete_candidate,
    get_application, get_applications_by_job, get_applications_by_candidate, get_applications_by_company,
    create_application, update_application, delete_application,
    get_interview, get_interviews_by_job, get_interviews_by_candidate,
    create_interview, update_interview, delete_interview
)
from app.schemas.schemas import (
    JobPostingCreate, JobPostingUpdate, JobPostingResponse,
    CandidateCreate, CandidateUpdate, CandidateResponse,
    JobApplicationCreate, JobApplicationUpdate, JobApplicationResponse,
    InterviewCreate, InterviewUpdate, InterviewResponse
)

router = APIRouter()


# ========== Job Posting Management ==========
@router.get("/jobs", response_model=List[JobPostingResponse])
async def list_job_postings(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all job postings for current company"""
    company_id = current_user["company_id"]
    return get_job_postings_by_company(db, company_id=company_id, skip=skip, limit=limit)


@router.get("/jobs/published", response_model=List[JobPostingResponse])
async def list_published_jobs(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all published job postings"""
    return get_published_job_postings(db, skip=skip, limit=limit)


@router.get("/jobs/{job_id}", response_model=JobPostingResponse)
async def get_job_posting(
    job_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get job posting by ID"""
    job = get_job_posting(db, job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job posting not found"
        )
    return job


@router.post("/jobs", response_model=JobPostingResponse)
async def create_new_job_posting(
    job: JobPostingCreate,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Create a new job posting"""
    company_id = current_user["company_id"]

    # Validate department and position belong to company
    from app.crud.crud_department import get_department
    if job.department_id:
        dept = get_department(db, job.department_id)
        if not dept or dept.company_id != company_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid department"
            )

    return create_job_posting(db=db, job_posting=job, company_id=company_id)


@router.put("/jobs/{job_id}", response_model=JobPostingResponse)
async def update_job_posting_endpoint(
    job_id: int,
    job: JobPostingUpdate,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Update job posting"""
    db_job = get_job_posting(db, job_id)
    if not db_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job posting not found"
        )

    if db_job.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return update_job_posting(db, job_id, job)


@router.delete("/jobs/{job_id}")
async def delete_job_posting_endpoint(
    job_id: int,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Delete job posting"""
    success = delete_job_posting(db, job_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job posting not found"
        )
    return {"message": "Job posting deleted successfully"}


@router.post("/jobs/{job_id}/publish", response_model=JobPostingResponse)
async def publish_job_posting_endpoint(
    job_id: int,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Publish job posting"""
    job = publish_job_posting(db, job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job posting not found"
        )
    return job


# ========== Candidate Management ==========
@router.get("/candidates", response_model=List[CandidateResponse])
async def list_candidates(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all candidates"""
    return get_candidates(db, skip=skip, limit=limit)


@router.get("/candidates/{candidate_id}", response_model=CandidateResponse)
async def get_candidate_endpoint(
    candidate_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get candidate by ID"""
    candidate = get_candidate(db, candidate_id)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    return candidate


@router.post("/candidates", response_model=CandidateResponse)
async def create_new_candidate(
    candidate: CandidateCreate,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Create a new candidate"""
    return create_candidate(db=db, candidate=candidate)


@router.put("/candidates/{candidate_id}", response_model=CandidateResponse)
async def update_candidate_endpoint(
    candidate_id: int,
    candidate: CandidateUpdate,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Update candidate"""
    updated_candidate = update_candidate(db, candidate_id, candidate)
    if not updated_candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    return updated_candidate


@router.delete("/candidates/{candidate_id}")
async def delete_candidate_endpoint(
    candidate_id: int,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Delete candidate"""
    success = delete_candidate(db, candidate_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    return {"message": "Candidate deleted successfully"}


# ========== Job Application Management ==========
@router.get("/applications", response_model=List[JobApplicationResponse])
async def list_applications(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(verify_company_access),
    db: Session = Depends(get_db)
):
    """List all applications in company"""
    company_id = current_user["company_id"]
    return get_applications_by_company(db, company_id=company_id, skip=skip, limit=limit)


@router.get("/applications/{application_id}", response_model=JobApplicationResponse)
async def get_application_endpoint(
    application_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get application by ID"""
    application = get_application(db, application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    return application


@router.get("/jobs/{job_id}/applications", response_model=List[JobApplicationResponse])
async def list_job_applications(
    job_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all applications for a job"""
    return get_applications_by_job(db, job_id=job_id, skip=skip, limit=limit)


@router.get("/employees/{employee_id}/applications", response_model=List[JobApplicationResponse])
async def list_employee_applications(
    employee_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all applications from an employee (candidate)"""
    return get_applications_by_candidate(db, candidate_id=employee_id, skip=skip, limit=limit)


@router.post("/applications", response_model=JobApplicationResponse)
async def create_new_application(
    application: JobApplicationCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new job application"""
    employee_id = application.candidate_id or current_user["user"].id
    return create_application(db=db, application=application, employee_id=employee_id)


@router.put("/applications/{application_id}", response_model=JobApplicationResponse)
async def update_application_endpoint(
    application_id: int,
    application: JobApplicationUpdate,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Update application (approve/reject)"""
    updated_application = update_application(db, application_id, application)
    if not updated_application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    return updated_application


@router.delete("/applications/{application_id}")
async def delete_application_endpoint(
    application_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete application"""
    success = delete_application(db, application_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    return {"message": "Application deleted successfully"}


# ========== Interview Management ==========
@router.get("/interviews", response_model=List[InterviewResponse])
async def list_interviews(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(verify_company_access),
    db: Session = Depends(get_db)
):
    """List all interviews in company"""
    company_id = current_user["company_id"]
    # Use simple query to avoid complex joins for now
    from app.models.models import Interview
    return db.query(Interview).offset(skip).limit(limit).all()


@router.get("/interviews/{interview_id}", response_model=InterviewResponse)
async def get_interview_endpoint(
    interview_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get interview by ID"""
    interview = get_interview(db, interview_id)
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    return interview


@router.get("/jobs/{job_id}/interviews", response_model=List[InterviewResponse])
async def list_job_interviews(
    job_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all interviews for a job"""
    return get_interviews_by_job(db, job_id=job_id, skip=skip, limit=limit)


@router.get("/candidates/{candidate_id}/interviews", response_model=List[InterviewResponse])
async def list_candidate_interviews(
    candidate_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all interviews for a candidate"""
    return get_interviews_by_candidate(db, candidate_id=candidate_id, skip=skip, limit=limit)


@router.post("/interviews", response_model=InterviewResponse)
async def create_new_interview(
    interview: InterviewCreate,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Schedule an interview"""
    company_id = current_user["company_id"]
    return create_interview(db=db, interview=interview, company_id=company_id)


@router.put("/interviews/{interview_id}", response_model=InterviewResponse)
async def update_interview_endpoint(
    interview_id: int,
    interview: InterviewUpdate,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Update interview"""
    db_interview = get_interview(db, interview_id)
    if not db_interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )

    if db_interview.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return update_interview(db, interview_id, interview)


@router.delete("/interviews/{interview_id}")
async def delete_interview_endpoint(
    interview_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete interview"""
    success = delete_interview(db, interview_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    return {"message": "Interview deleted successfully"}

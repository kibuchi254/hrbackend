from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.models import (
    JobPosting, Candidate, JobApplication, Interview,
    ApplicationStatus, CandidateStatus, InterviewStatus, InterviewType
)
from app.schemas.schemas import (
    JobPostingCreate, JobPostingUpdate,
    CandidateCreate, CandidateUpdate,
    JobApplicationCreate, JobApplicationUpdate,
    InterviewCreate, InterviewUpdate
)


# ========== Job Posting CRUD ==========
def get_job_posting(db: Session, job_id: int) -> Optional[JobPosting]:
    return db.query(JobPosting).filter(JobPosting.id == job_id).first()


def get_job_postings_by_company(
    db: Session,
    company_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[JobPosting]:
    return db.query(JobPosting).filter(JobPosting.company_id == company_id).offset(skip).limit(limit).all()


def get_published_job_postings(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[JobPosting]:
    return db.query(JobPosting).filter(JobPosting.status == ApplicationStatus.PUBLISHED).offset(skip).limit(limit).all()


def create_job_posting(db: Session, job_posting: JobPostingCreate, company_id: int) -> JobPosting:
    db_job_posting = JobPosting(
        company_id=company_id,
        title=job_posting.title,
        description=job_posting.description,
        requirements=job_posting.requirements,
        responsibilities=job_posting.responsibilities,
        benefits=job_posting.benefits,
        department_id=job_posting.department_id,
        position_id=job_posting.position_id,
        location=job_posting.location,
        employment_type=job_posting.employment_type,
        experience_level=job_posting.experience_level,
        salary_min=job_posting.salary_min,
        salary_max=job_posting.salary_max,
        salary_visible=job_posting.salary_visible,
        vacancy_count=job_posting.vacancy_count,
        status=ApplicationStatus.DRAFT,
        created_by=job_posting.created_by
    )
    db.add(db_job_posting)
    db.commit()
    db.refresh(db_job_posting)
    return db_job_posting


def update_job_posting(db: Session, job_id: int, job_posting: JobPostingUpdate) -> Optional[JobPosting]:
    db_job_posting = get_job_posting(db, job_id)
    if db_job_posting:
        update_data = job_posting.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_job_posting, key, value)
        db.commit()
        db.refresh(db_job_posting)
    return db_job_posting


def delete_job_posting(db: Session, job_id: int) -> bool:
    db_job_posting = get_job_posting(db, job_id)
    if db_job_posting:
        db.delete(db_job_posting)
        db.commit()
        return True
    return False


def publish_job_posting(db: Session, job_id: int) -> Optional[JobPosting]:
    db_job_posting = get_job_posting(db, job_id)
    if db_job_posting:
        db_job_posting.status = ApplicationStatus.PUBLISHED
        db.commit()
        db.refresh(db_job_posting)
    return db_job_posting


# ========== Candidate CRUD ==========
def get_candidate(db: Session, candidate_id: int) -> Optional[Candidate]:
    return db.query(Candidate).filter(Candidate.id == candidate_id).first()


def get_candidates(db: Session, skip: int = 0, limit: int = 100) -> List[Candidate]:
    return db.query(Candidate).offset(skip).limit(limit).all()


def create_candidate(db: Session, candidate: CandidateCreate) -> Candidate:
    db_candidate = Candidate(
        email=candidate.email,
        full_name=candidate.full_name,
        phone=candidate.phone,
        location=candidate.location,
        resume_url=candidate.resume_url,
        cover_letter_url=candidate.cover_letter_url,
        linkedin_url=candidate.linkedin_url,
        portfolio_url=candidate.portfolio_url,
        skills=candidate.skills,
        experience_years=candidate.experience_years,
        education=candidate.education,
        current_company=candidate.current_company,
        current_position=candidate.current_position,
        expected_salary_min=candidate.expected_salary_min,
        expected_salary_max=candidate.expected_salary_max
    )
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate


def update_candidate(db: Session, candidate_id: int, candidate: CandidateUpdate) -> Optional[Candidate]:
    db_candidate = get_candidate(db, candidate_id)
    if db_candidate:
        update_data = candidate.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_candidate, key, value)
        db.commit()
        db.refresh(db_candidate)
    return db_candidate


def delete_candidate(db: Session, candidate_id: int) -> bool:
    db_candidate = get_candidate(db, candidate_id)
    if db_candidate:
        db.delete(db_candidate)
        db.commit()
        return True
    return False


# ========== Job Application CRUD ==========
def get_application(db: Session, application_id: int) -> Optional[JobApplication]:
    return db.query(JobApplication).filter(JobApplication.id == application_id).first()


def get_applications_by_job(
    db: Session,
    job_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[JobApplication]:
    return db.query(JobApplication).filter(JobApplication.job_posting_id == job_id).offset(skip).limit(limit).all()


def get_applications_by_candidate(
    db: Session,
    candidate_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[JobApplication]:
    return db.query(JobApplication).filter(JobApplication.candidate_id == candidate_id).offset(skip).limit(limit).all()


def get_applications_by_company(
    db: Session,
    company_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[JobApplication]:
    from app.models.models import JobPosting
    return db.query(JobApplication).join(JobPosting).filter(
        JobPosting.company_id == company_id
    ).offset(skip).limit(limit).all()


def create_application(db: Session, application: JobApplicationCreate) -> JobApplication:
    db_application = JobApplication(
        job_posting_id=application.job_posting_id,
        candidate_id=application.candidate_id,
        cover_letter=application.cover_letter,
        status=CandidateStatus.NEW
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application


def update_application(db: Session, application_id: int, application: JobApplicationUpdate) -> Optional[JobApplication]:
    db_application = get_application(db, application_id)
    if db_application:
        update_data = application.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_application, key, value)
        db.commit()
        db.refresh(db_application)
    return db_application


def delete_application(db: Session, application_id: int) -> bool:
    db_application = get_application(db, application_id)
    if db_application:
        db.delete(db_application)
        db.commit()
        return True
    return False


# ========== Interview CRUD ==========
def get_interview(db: Session, interview_id: int) -> Optional[Interview]:
    return db.query(Interview).filter(Interview.id == interview_id).first()


def get_interviews_by_job(
    db: Session,
    job_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Interview]:
    return db.query(Interview).filter(Interview.job_posting_id == job_id).offset(skip).limit(limit).all()


def get_interviews_by_candidate(
    db: Session,
    candidate_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Interview]:
    return db.query(Interview).filter(Interview.candidate_id == candidate_id).offset(skip).limit(limit).all()


def create_interview(db: Session, interview: InterviewCreate) -> Interview:
    db_interview = Interview(
        job_posting_id=interview.job_posting_id,
        candidate_id=interview.candidate_id,
        application_id=interview.application_id,
        interview_type=interview.interview_type,
        scheduled_date=interview.scheduled_date,
        scheduled_duration=interview.scheduled_duration,
        interviewer_ids=interview.interviewer_ids,
        location=interview.location,
        agenda=interview.agenda,
        status=InterviewStatus.SCHEDULED,
        created_by=interview.created_by
    )
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    return db_interview


def update_interview(db: Session, interview_id: int, interview: InterviewUpdate) -> Optional[Interview]:
    db_interview = get_interview(db, interview_id)
    if db_interview:
        update_data = interview.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_interview, key, value)
        db.commit()
        db.refresh(db_interview)
    return db_interview


def delete_interview(db: Session, interview_id: int) -> bool:
    db_interview = get_interview(db, interview_id)
    if db_interview:
        db.delete(db_interview)
        db.commit()
        return True
    return False

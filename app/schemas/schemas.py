from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal


# ========== Common Schemas ==========
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None
    company_id: Optional[int] = None


# ========== Super Admin Schemas ==========
class SuperAdminBase(BaseModel):
    email: EmailStr
    full_name: str


class SuperAdminCreate(SuperAdminBase):
    password: str


class SuperAdminUpdate(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class SuperAdminResponse(SuperAdminBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class SuperAdminLogin(BaseModel):
    email: EmailStr
    password: str


# ========== Company Schemas ==========
class CompanyBase(BaseModel):
    name: str
    business_email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None


class CompanyCreate(CompanyBase):
    owner_email: EmailStr
    owner_password: str
    owner_full_name: str


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    logo_url: Optional[str] = None
    is_active: Optional[bool] = None
    subscription_tier: Optional[str] = None


class CompanyResponse(CompanyBase):
    id: int
    logo_url: Optional[str]
    is_active: bool
    subscription_tier: str
    subscription_expires_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


# ========== Employee Schemas ==========
class EmployeeBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[date] = None


class EmployeeCreate(EmployeeBase):
    password: str
    employee_id: str
    role: str = "employee"
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    hire_date: date


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    profile_image_url: Optional[str] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    termination_date: Optional[date] = None
    status: Optional[str] = None


class EmployeeResponse(EmployeeBase):
    id: int
    employee_id: str
    role: str
    status: str
    company_id: int
    department_id: Optional[int]
    position_id: Optional[int]
    profile_image_url: Optional[str]
    hire_date: Optional[date]
    termination_date: Optional[date]
    created_at: datetime

    class Config:
        from_attributes = True


class EmployeeLogin(BaseModel):
    email: EmailStr
    password: str


# ========== Department Schemas ==========
class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    manager_id: Optional[int] = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    manager_id: Optional[int] = None


class DepartmentResponse(DepartmentBase):
    id: int
    company_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ========== Position Schemas ==========
class PositionBase(BaseModel):
    title: str
    description: Optional[str] = None
    base_salary: Optional[Decimal] = None


class PositionCreate(PositionBase):
    pass


class PositionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    base_salary: Optional[Decimal] = None


class PositionResponse(PositionBase):
    id: int
    department_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ========== Salary Schemas ==========
class SalaryBase(BaseModel):
    base_salary: Decimal
    housing_allowance: Decimal = 0
    transport_allowance: Decimal = 0
    medical_allowance: Decimal = 0
    other_allowances: Decimal = 0
    tax_deduction: Decimal = 0
    insurance_deduction: Decimal = 0
    other_deductions: Decimal = 0


class SalaryCreate(SalaryBase):
    employee_id: int
    effective_date: Optional[date] = None


class SalaryUpdate(SalaryBase):
    effective_date: Optional[date] = None


class SalaryResponse(SalaryBase):
    id: int
    employee_id: int
    effective_date: Optional[date]
    created_at: datetime

    class Config:
        from_attributes = True


# ========== Attendance Schemas ==========
class AttendanceBase(BaseModel):
    date: date
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    status: str = "present"
    notes: Optional[str] = None


class AttendanceCreate(AttendanceBase):
    employee_id: int


class AttendanceUpdate(BaseModel):
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class AttendanceResponse(AttendanceBase):
    id: int
    employee_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ========== Leave Schemas ==========
class LeaveBase(BaseModel):
    leave_type: str
    start_date: date
    end_date: date
    reason: Optional[str] = None


class LeaveCreate(LeaveBase):
    employee_id: Optional[int] = None  # If None, use current user


class LeaveUpdate(BaseModel):
    status: Optional[str] = None
    rejection_reason: Optional[str] = None


class LeaveResponse(LeaveBase):
    id: int
    employee_id: int
    total_days: Optional[int]
    status: str
    approved_by: Optional[int]
    approved_at: Optional[datetime]
    rejection_reason: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ========== Payroll Schemas ==========
class PayrollCycleBase(BaseModel):
    name: str
    start_date: date
    end_date: date
    payment_date: Optional[date] = None


class PayrollCycleCreate(PayrollCycleBase):
    pass


class PayrollCycleUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    payment_date: Optional[date] = None
    status: Optional[str] = None


class PayrollCycleResponse(PayrollCycleBase):
    id: int
    company_id: int
    status: str
    total_amount: Decimal
    created_at: datetime

    class Config:
        from_attributes = True


class PayrollItemBase(BaseModel):
    base_salary: Decimal
    gross_salary: Optional[Decimal] = None
    total_deductions: Optional[Decimal] = None
    net_salary: Optional[Decimal] = None
    payment_method: Optional[str] = None
    payment_reference: Optional[str] = None


class PayrollItemCreate(PayrollItemBase):
    employee_id: int


class PayrollItemUpdate(PayrollItemBase):
    payment_date: Optional[datetime] = None


class PayrollItemResponse(PayrollItemBase):
    id: int
    payroll_cycle_id: int
    employee_id: int
    payment_date: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


# ========== Dashboard Stats Schemas ==========
class DashboardStats(BaseModel):
    total_employees: int
    active_employees: int
    total_departments: int
    total_payroll_this_month: Optional[Decimal] = None
    pending_leaves: int
    present_today: int
    absent_today: int

# ========== Recruitment Schemas ==========
class JobPostingBase(BaseModel):
    title: str
    description: str
    requirements: str
    responsibilities: str
    benefits: str
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    location: str = "remote"
    employment_type: str = "full-time"
    experience_level: str = "mid"
    salary_min: Optional[Decimal] = None
    salary_max: Optional[Decimal] = None
    salary_visible: bool = False
    vacancy_count: int = 1

class JobPostingCreate(JobPostingBase):
    department_id: Optional[int] = None
    position_id: Optional[int] = None

class JobPostingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    benefits: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    experience_level: Optional[str] = None
    salary_min: Optional[Decimal] = None
    salary_max: Optional[Decimal] = None
    salary_visible: Optional[bool] = None
    vacancy_count: Optional[int] = None

class JobPostingResponse(JobPostingBase):
    id: int
    company_id: int
    status: str
    published_at: Optional[datetime]
    expires_at: Optional[datetime]
    ai_generated_description: bool
    ai_enhanced: bool
    created_at: datetime
    created_by: Optional[int]

    class Config:
        from_attributes = True

class CandidateBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    location: Optional[str] = None
    resume_url: Optional[str] = None
    cover_letter_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    skills: Optional[str] = None
    experience_years: Optional[int] = None
    education: Optional[str] = None
    current_company: Optional[str] = None
    current_position: Optional[str] = None
    expected_salary_min: Optional[Decimal] = None
    expected_salary_max: Optional[Decimal] = None

class CandidateCreate(CandidateBase):
    pass

class CandidateUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[str] = None
    experience_years: Optional[int] = None
    current_company: Optional[str] = None
    current_position: Optional[str] = None

class CandidateResponse(CandidateBase):
    id: int
    ai_score: Optional[Decimal] = None
    ai_summary: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class JobApplicationBase(BaseModel):
    job_posting_id: int
    candidate_id: int
    cover_letter: Optional[str] = None

class JobApplicationCreate(JobApplicationBase):
    job_posting_id: int
    candidate_id: Optional[int] = None

class JobApplicationUpdate(BaseModel):
    status: Optional[str] = None

class JobApplicationResponse(JobApplicationBase):
    id: int
    status: str
    applied_at: datetime
    ai_match_score: Optional[Decimal] = None
    ai_fit_reason: Optional[str] = None
    ai_keywords_matched: Optional[str] = None
    ai_strengths: Optional[str] = None
    ai_weaknesses: Optional[str] = None
    reviewed_by: Optional[int]
    reviewed_at: Optional[datetime]
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class InterviewBase(BaseModel):
    job_posting_id: int
    candidate_id: int
    application_id: Optional[int] = None
    interview_type: str = "video"
    scheduled_date: datetime
    scheduled_duration: int = 60
    interviewer_ids: Optional[str] = None
    location: Optional[str] = None
    agenda: Optional[str] = None

class InterviewCreate(InterviewBase):
    pass

class InterviewUpdate(BaseModel):
    status: Optional[str] = None
    feedback: Optional[str] = None
    rating: Optional[int] = None

class InterviewResponse(InterviewBase):
    id: int
    status: str
    completed_at: Optional[datetime]
    ai_interview_notes: Optional[str] = None
    ai_questions_suggested: Optional[str] = None
    ai_candidate_sentiment: Optional[str] = None
    created_by: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

# ========== AI Schemas ==========
class GenerateJobDescriptionRequest(BaseModel):
    job_title: str
    requirements: str
    skills: List[str]
    experience_level: str
    company_name: str

class AnalyzeCandidateRequest(BaseModel):
    resume_text: str
    job_requirements: str
    job_description: str

class GenerateInterviewQuestionsRequest(BaseModel):
    job_title: str
    job_description: str
    candidate_profile: str
    interview_type: str = "behavioral"

class AnalyzeInterviewRequest(BaseModel):
    interview_transcript: str
    job_requirements: str

class GenerateSalaryInsightsRequest(BaseModel):
    job_title: str
    location: str
    experience_level: str
    skills: List[str]

class PerformanceReviewRequest(BaseModel):
    employee_name: str
    role: str
    achievements: str
    areas_for_improvement: str

class AIResponse(BaseModel):
    success: bool
    data: dict
    message: Optional[str] = None
    tokens_used: Optional[int] = None
    processing_time_ms: Optional[int] = None


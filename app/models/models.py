from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text, Date
from sqlalchemy.types import Numeric as Decimal
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class UserRole(str, enum.Enum):
    SUPER_ADMIN = "super_admin"  # SaaS Owner - manages the platform
    COMPANY_ADMIN = "company_admin"  # Manages company operations (HR, Payroll, Recruitment)
    HR_MANAGER = "hr_manager"  # HR functions only
    PAYROLL_MANAGER = "payroll_manager"  # Payroll functions only
    RECRUITMENT_MANAGER = "recruitment_manager"  # Recruitment functions only
    EMPLOYEE = "employee"  # Regular employee


class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class LeaveStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class PayrollStatus(str, enum.Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    PROCESSED = "processed"
    PAID = "paid"
    FAILED = "failed"


class AttendanceStatus(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    HALF_DAY = "half_day"
    LEAVE = "leave"


# User Models
class SuperAdmin(Base):
    """SaaS Platform Owner/Admin - manages the entire platform"""
    __tablename__ = "super_admins"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    companies_managed = relationship("Company", back_populates="created_by_super_admin")


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    business_email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String)
    address = Column(Text)
    logo_url = Column(String)
    is_active = Column(Boolean, default=True)
    subscription_tier = Column(String, default="basic")  # basic, pro, enterprise
    subscription_expires_at = Column(DateTime(timezone=True))
    created_by = Column(Integer, ForeignKey("super_admins.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    created_by_super_admin = relationship("SuperAdmin", back_populates="companies_managed")
    departments = relationship("Department", back_populates="company", cascade="all, delete-orphan")
    employees = relationship("Employee", back_populates="company", cascade="all, delete-orphan")
    payroll_cycles = relationship("PayrollCycle", back_populates="company", cascade="all, delete-orphan")
    job_postings = relationship("JobPosting", back_populates="company", cascade="all, delete-orphan")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    employee_id = Column(String, unique=True, index=True)  # Company-specific employee ID
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    position_id = Column(Integer, ForeignKey("positions.id"))
    phone = Column(String)
    address = Column(Text)
    date_of_birth = Column(Date)
    hire_date = Column(Date)
    termination_date = Column(Date)
    profile_image_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", back_populates="employees")
    department = relationship("Department", back_populates="employees", foreign_keys=[department_id])
    position = relationship("Position", back_populates="employees", foreign_keys=[position_id])
    salary = relationship("Salary", back_populates="employee", uselist=False)
    attendance = relationship("Attendance", back_populates="employee", cascade="all, delete-orphan")
    leaves = relationship("Leave", back_populates="employee", foreign_keys="Leave.employee_id", cascade="all, delete-orphan")
    payroll_items = relationship("PayrollItem", back_populates="employee", cascade="all, delete-orphan")


# Department and Position
class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    manager_id = Column(Integer, ForeignKey("employees.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", back_populates="departments")
    employees = relationship("Employee", back_populates="department", foreign_keys=[Employee.department_id])
    positions = relationship("Position", back_populates="department", cascade="all, delete-orphan")


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    base_salary = Column(Decimal(10, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    department = relationship("Department", back_populates="positions")
    employees = relationship("Employee", back_populates="position")


# HR Module
class Salary(Base):
    __tablename__ = "salaries"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True, nullable=False)
    base_salary = Column(Decimal(10, 2), nullable=False)
    housing_allowance = Column(Decimal(10, 2), default=0)
    transport_allowance = Column(Decimal(10, 2), default=0)
    medical_allowance = Column(Decimal(10, 2), default=0)
    other_allowances = Column(Decimal(10, 2), default=0)
    tax_deduction = Column(Decimal(10, 2), default=0)
    insurance_deduction = Column(Decimal(10, 2), default=0)
    other_deductions = Column(Decimal(10, 2), default=0)
    effective_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    employee = relationship("Employee", back_populates="salary")


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    date = Column(Date, nullable=False)
    check_in_time = Column(DateTime(timezone=True))
    check_out_time = Column(DateTime(timezone=True))
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.PRESENT)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    employee = relationship("Employee", back_populates="attendance")


class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    leave_type = Column(String, nullable=False)  # annual, sick, maternity, paternity, etc.
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    total_days = Column(Integer)
    reason = Column(Text)
    status = Column(Enum(LeaveStatus), default=LeaveStatus.PENDING)
    approved_by = Column(Integer, ForeignKey("employees.id"))
    approved_at = Column(DateTime(timezone=True))
    rejection_reason = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    employee = relationship("Employee", back_populates="leaves", foreign_keys=[employee_id])


# Payroll Module
class PayrollCycle(Base):
    __tablename__ = "payroll_cycles"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String, nullable=False)  # e.g., "January 2024"
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    payment_date = Column(Date)
    status = Column(Enum(PayrollStatus), default=PayrollStatus.DRAFT)
    total_amount = Column(Decimal(12, 2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", back_populates="payroll_cycles")
    payroll_items = relationship("PayrollItem", back_populates="payroll_cycle", cascade="all, delete-orphan")


class PayrollItem(Base):
    __tablename__ = "payroll_items"

    id = Column(Integer, primary_key=True, index=True)
    payroll_cycle_id = Column(Integer, ForeignKey("payroll_cycles.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    base_salary = Column(Decimal(10, 2), nullable=False)
    gross_salary = Column(Decimal(10, 2))
    total_deductions = Column(Decimal(10, 2))
    net_salary = Column(Decimal(10, 2))
    payment_date = Column(DateTime(timezone=True))
    payment_method = Column(String)
    payment_reference = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    payroll_cycle = relationship("PayrollCycle", back_populates="payroll_items")
    employee = relationship("Employee", back_populates="payroll_items")


# ========== Recruitment Module ==========

class ApplicationStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"
    FILLED = "filled"
    EXPIRED = "expired"


class CandidateStatus(str, enum.Enum):
    NEW = "new"
    SCREENING = "screening"
    SHORTLISTED = "shortlisted"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEWED = "interviewed"
    OFFER_SENT = "offer_sent"
    OFFER_ACCEPTED = "offer_accepted"
    OFFER_REJECTED = "offer_rejected"
    HIRED = "hired"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class InterviewStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    RESCHEDULED = "rescheduled"


class InterviewType(str, enum.Enum):
    PHONE = "phone"
    VIDEO = "video"
    IN_PERSON = "in_person"
    TECHNICAL = "technical"
    PANEL = "panel"


class JobPosting(Base):
    """Job postings published by companies"""
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    responsibilities = Column(Text)
    benefits = Column(Text)
    department_id = Column(Integer, ForeignKey("departments.id"))
    position_id = Column(Integer, ForeignKey("positions.id"))
    location = Column(String)  # remote, on-site, hybrid, or specific location
    employment_type = Column(String)  # full-time, part-time, contract, internship
    experience_level = Column(String)  # entry, mid, senior, executive
    salary_min = Column(Decimal(12, 2))
    salary_max = Column(Decimal(12, 2))
    salary_visible = Column(Boolean, default=False)
    vacancy_count = Column(Integer, default=1)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.DRAFT)
    published_at = Column(DateTime(timezone=True))
    expires_at = Column(DateTime(timezone=True))
    created_by = Column(Integer, ForeignKey("employees.id"))
    ai_generated_description = Column(Boolean, default=False)
    ai_enhanced = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", back_populates="job_postings")
    applications = relationship("JobApplication", back_populates="job_posting", cascade="all, delete-orphan")
    interviews = relationship("Interview", back_populates="job_posting", cascade="all, delete-orphan")


class Candidate(Base):
    """Candidate profiles in the system"""
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    phone = Column(String)
    location = Column(String)
    resume_url = Column(String)  # URL to stored resume
    cover_letter_url = Column(String)
    linkedin_url = Column(String)
    portfolio_url = Column(String)
    skills = Column(Text)  # JSON array of skills
    experience_years = Column(Integer)
    education = Column(Text)  # JSON array of education
    current_company = Column(String)
    current_position = Column(String)
    expected_salary_min = Column(Decimal(12, 2))
    expected_salary_max = Column(Decimal(12, 2))
    ai_score = Column(Decimal(5, 2))  # AI matching score (0-5)
    ai_summary = Column(Text)  # AI-generated candidate summary
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    applications = relationship("JobApplication", back_populates="candidate", cascade="all, delete-orphan")
    interviews = relationship("Interview", back_populates="candidate", cascade="all, delete-orphan")


class JobApplication(Base):
    """Job applications from candidates to job postings"""
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    job_posting_id = Column(Integer, ForeignKey("job_postings.id"), nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    status = Column(Enum(CandidateStatus), default=CandidateStatus.NEW)
    cover_letter = Column(Text)
    applied_at = Column(DateTime(timezone=True), server_default=func.now())
    ai_match_score = Column(Decimal(5, 2))  # AI matching score (0-5)
    ai_fit_reason = Column(Text)  # AI explanation of fit
    ai_keywords_matched = Column(Text)  # JSON array of matched keywords
    ai_strengths = Column(Text)  # AI-identified strengths
    ai_weaknesses = Column(Text)  # AI-identified areas for improvement
    reviewed_by = Column(Integer, ForeignKey("employees.id"))
    reviewed_at = Column(DateTime(timezone=True))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    job_posting = relationship("JobPosting", back_populates="applications")
    candidate = relationship("Candidate", back_populates="applications")
    interviews = relationship("Interview", back_populates="application", cascade="all, delete-orphan")


class Interview(Base):
    """Interview schedules and details"""
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    job_posting_id = Column(Integer, ForeignKey("job_postings.id"), nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    application_id = Column(Integer, ForeignKey("job_applications.id"))
    interview_type = Column(Enum(InterviewType), default=InterviewType.VIDEO)
    status = Column(Enum(InterviewStatus), default=InterviewStatus.SCHEDULED)
    scheduled_date = Column(DateTime(timezone=True), nullable=False)
    scheduled_duration = Column(Integer, default=60)  # minutes
    interviewer_ids = Column(Text)  # JSON array of employee IDs
    location = Column(String)  # meeting link or physical address
    agenda = Column(Text)
    feedback = Column(Text)
    rating = Column(Integer)  # 1-5 scale
    ai_interview_notes = Column(Text)  # AI-generated notes/interview analysis
    ai_questions_suggested = Column(Text)  # AI-suggested interview questions
    ai_candidate_sentiment = Column(Text)  # AI-sentiment analysis from interview
    completed_at = Column(DateTime(timezone=True))
    created_by = Column(Integer, ForeignKey("employees.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    job_posting = relationship("JobPosting", back_populates="interviews")
    candidate = relationship("Candidate", back_populates="interviews")
    application = relationship("JobApplication", back_populates="interviews")


class AIPromptHistory(Base):
    """History of AI prompts and responses"""
    __tablename__ = "ai_prompt_history"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    user_id = Column(Integer, ForeignKey("employees.id"))
    ai_provider = Column(String, nullable=False)  # 'gemini' or 'claude'
    prompt_type = Column(String, nullable=False)  # 'job_description', 'candidate_analysis', 'interview_questions', etc.
    input_data = Column(Text)  # JSON input
    ai_response = Column(Text)  # AI response
    tokens_used = Column(Integer)
    processing_time = Column(Integer)  # milliseconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AIModelConfig(Base):
    """AI model configurations per company"""
    __tablename__ = "ai_model_config"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, unique=True)
    gemini_enabled = Column(Boolean, default=False)
    gemini_api_key = Column(String)
    gemini_model = Column(String, default="gemini-pro")
    claude_enabled = Column(Boolean, default=False)
    claude_api_key = Column(String)
    claude_model = Column(String, default="claude-3-sonnet")
    auto_screening_enabled = Column(Boolean, default=False)
    auto_interview_questions_enabled = Column(Boolean, default=False)
    ai_job_description_enabled = Column(Boolean, default=True)
    ai_candidate_matching_enabled = Column(Boolean, default=True)
    monthly_token_limit = Column(Integer, default=100000)
    monthly_tokens_used = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# ========== Notifications & Communications Module ==========

class NotificationChannel(str, enum.Enum):
    EMAIL = "email"
    SMS = "sms"
    IN_APP = "in_app"
    WEBHOOK = "webhook"


class NotificationType(str, enum.Enum):
    # Payroll Notifications
    PAYROLL_PROCESSED = "payroll_processed"
    PAYSLIP_READY = "payslip_ready"
    SALARY_UPDATE = "salary_update"

    # HR Notifications
    LEAVE_REQUEST = "leave_request"
    LEAVE_APPROVED = "leave_approved"
    LEAVE_REJECTED = "leave_rejected"
    ATTENDANCE_ALERT = "attendance_alert"

    # Recruitment Notifications
    NEW_APPLICATION = "new_application"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    OFFER_SENT = "offer_sent"

    # Compliance Notifications
    STATUTORY_REPORT_READY = "statutory_report_ready"
    COMPLIANCE_WARNING = "compliance_warning"
    TAX_FILING_REMINDER = "tax_filing_reminder"

    # General Notifications
    ACCOUNT_UPDATE = "account_update"
    SYSTEM_MAINTENANCE = "system_maintenance"


class NotificationStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    READ = "read"


class NotificationTemplate(Base):
    """Email and notification templates"""
    __tablename__ = "notification_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)  # email, sms
    subject = Column(String)
    body = Column(Text, nullable=False)  # Jinja2 template
    variables = Column(Text)  # JSON array of variable names
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)  # NULL = system template
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", backref="notification_templates")


class NotificationPreference(Base):
    """User notification preferences"""
    __tablename__ = "notification_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("employees.id"), nullable=False, unique=True)
    channel_email = Column(Boolean, default=True)
    channel_sms = Column(Boolean, default=False)
    channel_in_app = Column(Boolean, default=True)
    type_payroll = Column(Boolean, default=True)
    type_hr = Column(Boolean, default=True)
    type_recruitment = Column(Boolean, default=True)
    type_compliance = Column(Boolean, default=True)
    type_general = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("Employee", backref="notification_preferences")


class Notification(Base):
    """Individual notifications"""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    channel = Column(Enum(NotificationChannel), default=NotificationChannel.IN_APP)
    status = Column(Enum(NotificationStatus), default=NotificationStatus.PENDING)
    extra_data = Column(Text)  # JSON data for email/SMS variables
    read_at = Column(DateTime(timezone=True))
    sent_at = Column(DateTime(timezone=True))
    delivered_at = Column(DateTime(timezone=True))
    error_message = Column(Text)
    template_id = Column(Integer, ForeignKey("notification_templates.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("Employee", backref="notifications")
    template = relationship("NotificationTemplate")


# ========== Document & Contract Management Module ==========

class DocumentCategory(str, enum.Enum):
    CONTRACT = "contract"
    OFFER_LETTER = "offer_letter"
    RESUME = "resume"
    CERTIFICATE = "certificate"
    ID_DOCUMENT = "id_document"
    BANK_DETAILS = "bank_details"
    TAX_DOCUMENT = "tax_document"
    PERFORMANCE_REVIEW = "performance_review"
    PAYSLIP = "payslip"
    OTHER = "other"


class DocumentStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class Document(Base):
    """Company and employee documents"""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), index=True)
    category = Column(Enum(DocumentCategory), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    file_url = Column(String, nullable=False)  # S3 or local storage path
    file_name = Column(String)
    file_type = Column(String)  # MIME type
    file_size = Column(Integer)
    version = Column(Integer, default=1)
    status = Column(Enum(DocumentStatus), default=DocumentStatus.DRAFT)
    expires_at = Column(DateTime(timezone=True))  # For contracts
    signed_url = Column(String)
    signed_at = Column(DateTime(timezone=True))
    uploaded_by = Column(Integer, ForeignKey("employees.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", backref="documents")
    employee = relationship("Employee", backref="documents")


class Contract(Base):
    """Employee contracts"""
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, unique=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    contract_type = Column(String)  # permanent, fixed-term, contract, internship
    probation_end_date = Column(Date)
    working_hours = Column(Integer, default=40)
    working_days = Column(String, default="mon-fri")
    salary_amount = Column(Decimal(12, 2))
    currency = Column(String, default="KES")
    benefits = Column(Text)  # JSON array
    terms = Column(Text)
    status = Column(Enum(DocumentStatus), default=DocumentStatus.DRAFT)
    document_url = Column(String)  # Signed PDF
    generated_payslip_template = Column(Text)  # Custom template for this contract
    created_by = Column(Integer, ForeignKey("employees.id"))
    approved_by = Column(Integer, ForeignKey("employees.id"))
    approved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", backref="contracts")
    employee = relationship("Employee", backref="contracts")


# ========== Kenya Statutory Compliance Module ==========

class PayeStatus(str, enum.Enum):
    NOT_APPLICABLE = "not_applicable"
    PAYE_TIER_1 = "paye_tier_1"  # 10%
    PAYE_TIER_2 = "paye_tier_2"  # 25%
    PAYE_TIER_3 = "paye_tier_3"  # 30%
    PAYE_TIER_4 = "paye_tier_4"  # 32.5%
    PAYE_TIER_5 = "paye_tier_5"  # 35%
    PAYE_TIER_6 = "paye_tier_6"  # 37.5%
    PAYE_TIER_7 = "paye_tier_7"  # 40%


class ComplianceRule(Base):
    """Compliance rules configuration"""
    __tablename__ = "compliance_rules"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    rule_type = Column(String, nullable=False)  # PAYE, NHIF, NSSF, Housing Levy, HELB
    rule_name = Column(String, nullable=False)
    is_enabled = Column(Boolean, default=True)
    rule_value = Column(Decimal(10, 4))  # Rate or threshold
    rule_description = Column(Text)
    effective_date = Column(Date)
    expiry_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", backref="compliance_rules")


class PayeDeduction(Base):
    """PAYE deductions per employee per month"""
    __tablename__ = "paye_deductions"

    id = Column(Integer, primary_key=True, index=True)
    payroll_item_id = Column(Integer, ForeignKey("payroll_items.id"), nullable=False, unique=True)
    taxable_income = Column(Decimal(12, 2), nullable=False)
    relief = Column(Decimal(10, 2), default=0)
    paye_status = Column(Enum(PayeStatus), default=PayeStatus.PAYE_TIER_1)
    paye_rate = Column(Decimal(5, 4))
    paye_amount = Column(Decimal(12, 2), nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class NhifDeduction(Base):
    """NHIF deductions"""
    __tablename__ = "nhif_deductions"

    id = Column(Integer, primary_key=True, index=True)
    payroll_item_id = Column(Integer, ForeignKey("payroll_items.id"), nullable=False, unique=True)
    nhif_amount = Column(Decimal(10, 2), nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class NssfContribution(Base):
    """NSSF Tier I & II contributions"""
    __tablename__ = "nssf_contributions"

    id = Column(Integer, primary_key=True, index=True)
    payroll_item_id = Column(Integer, ForeignKey("payroll_items.id"), nullable=False)
    tier_1_rate = Column(Decimal(5, 4), default=0.06)
    tier_1_cap = Column(Decimal(12, 2), default=18000)
    tier_1_amount = Column(Decimal(10, 2), default=0)
    tier_2_rate = Column(Decimal(5, 4), default=0.06)
    tier_2_amount = Column(Decimal(10, 2), default=0)
    total_amount = Column(Decimal(10, 2), nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class HousingLevy(Base):
    """Housing Levy contributions (1.5%)"""
    __tablename__ = "housing_levy"

    id = Column(Integer, primary_key=True, index=True)
    payroll_item_id = Column(Integer, ForeignKey("payroll_items.id"), nullable=False, unique=True)
    gross_salary = Column(Decimal(12, 2), nullable=False)
    levy_rate = Column(Decimal(5, 4), default=0.015)
    levy_amount = Column(Decimal(12, 2), nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class HelbDeduction(Base):
    """HELBB loan deductions"""
    __tablename__ = "helb_deductions"

    id = Column(Integer, primary_key=True, index=True)
    payroll_item_id = Column(Integer, ForeignKey("payroll_items.id"), nullable=False, unique=True)
    loan_reference = Column(String, unique=True, nullable=False)
    loan_amount = Column(Decimal(12, 2), nullable=False)
    monthly_deduction = Column(Decimal(10, 2), nullable=False)
    balance_remaining = Column(Decimal(12, 2))
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TaxRate(Base):
    """KRA tax rates for current year"""
    __tablename__ = "tax_rates"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    tier = Column(Integer, nullable=False)
    monthly_income_from = Column(Decimal(12, 2), nullable=False)
    monthly_income_to = Column(Decimal(12, 2), nullable=False)
    rate = Column(Decimal(5, 4), nullable=False)
    deduction = Column(Decimal(12, 2), default=0)
    is_active = Column(Boolean, default=True)
    effective_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class StatutoryReport(Base):
    """Monthly statutory reports (KRA, NHIF, NSSF, HELB)"""
    __tablename__ = "statutory_reports"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    report_type = Column(String, nullable=False)  # KRA_P9A, NHIF, NSSF, Housing Levy
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    status = Column(String, default="draft")  # draft, submitted, approved
    report_data = Column(Text)  # JSON data
    report_file_url = Column(String)  # Generated PDF/Excel
    itax_submission_id = Column(String)
    itax_submission_status = Column(String)
    submission_date = Column(DateTime(timezone=True))
    approved_by = Column(Integer, ForeignKey("employees.id"))
    created_by = Column(Integer, ForeignKey("employees.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", backref="statutory_reports")


# ========== Advanced Time, Shift & Overtime Module ==========

class ShiftType(str, enum.Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    NIGHT = "night"
    ROTATING = "rotating"
    FLEXIBLE = "flexible"


class Shift(Base):
    """Shift definitions"""
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(Enum(ShiftType), default=ShiftType.MORNING)
    start_time = Column(String, nullable=False)  # HH:MM format
    end_time = Column(String, nullable=False)  # HH:MM format
    break_duration = Column(Integer, default=0)  # minutes
    is_active = Column(Boolean, default=True)
    late_grace_minutes = Column(Integer, default=15)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", backref="shifts")


class EmployeeShift(Base):
    """Employee shift assignments"""
    __tablename__ = "employee_shifts"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    effective_date = Column(Date, nullable=False)
    end_date = Column(Date)  # NULL = ongoing
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    employee = relationship("Employee", backref="shifts")
    shift = relationship("Shift", backref="employee_assignments")


class OvertimeRule(Base):
    """Overtime calculation rules"""
    __tablename__ = "overtime_rules"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String, nullable=False)
    overtime_type = Column(String, nullable=False)  # daily, weekly, bi-weekly, monthly
    multiplier = Column(Decimal(4, 2), nullable=False)  # e.g., 1.5x
    is_active = Column(Boolean, default=True)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", backref="overtime_rules")


class OvertimeRequest(Base):
    """Overtime requests"""
    __tablename__ = "overtime_requests"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    hours = Column(Decimal(4, 2), nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(String, default="pending")  # pending, approved, rejected
    approved_by = Column(Integer, ForeignKey("employees.id"))
    approved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    employee = relationship("Employee", backref="overtime_requests")


class Holiday(Base):
    """Company holidays"""
    __tablename__ = "holidays"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    is_recurring = Column(Boolean, default=False)
    is_public = Column(Boolean, default=False)  # Kenya public holidays
    year = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AttendanceRule(Base):
    """Advanced attendance rules"""
    __tablename__ = "attendance_rules"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    rule_name = Column(String, nullable=False)
    rule_type = Column(String, nullable=False)  # lateness, absence, overtime
    threshold_minutes = Column(Integer)  # e.g., 15 minutes late = absent
    action = Column(String, nullable=False)  # warning, deduction, mark_absent
    deduction_amount = Column(Decimal(10, 2))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", backref="attendance_rules")


# ========== Performance Management Module ==========

class PerformancePeriodStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    SELF_ASSESSMENT = "self_assessment"
    MANAGER_REVIEW = "manager_review"
    CALIBRATION = "calibration"
    COMPLETE = "complete"


class KPI(Base):
    """Key Performance Indicators"""
    __tablename__ = "kpis"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    position_id = Column(Integer, ForeignKey("positions.id"))
    name = Column(String, nullable=False)
    description = Column(Text)
    target_value = Column(Decimal(10, 2))
    current_value = Column(Decimal(10, 2))
    unit = Column(String)  # percentage, count, rating
    weight = Column(Integer, default=1)  # Weight for overall score
    period = Column(String)  # monthly, quarterly, yearly
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", backref="kpis")


class OKR(Base):
    """Objectives and Key Results"""
    __tablename__ = "okrs"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    parent_id = Column(Integer, ForeignKey("okrs.id"))
    title = Column(String, nullable=False)
    description = Column(Text)
    objective_text = Column(Text)  # The O
    key_results = Column(Text)  # JSON array of KRs
    progress = Column(Integer, default=0)  # Percentage
    owner_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("employees.id"))
    quarter = Column(String, nullable=False)  # Q1, Q2, Q3, Q4
    year = Column(Integer, nullable=False)
    status = Column(String, default="in_progress")
    due_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", backref="okrs")
    parent = relationship("OKR", remote_side=[id], backref="children")


class PerformanceAppraisal(Base):
    """Performance appraisals"""
    __tablename__ = "performance_appraisals"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    period = Column(String, nullable=False)  # Q1 2024, H1 2024
    status = Column(Enum(PerformancePeriodStatus), default=PerformancePeriodStatus.NOT_STARTED)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    self_assessment_deadline = Column(Date)
    manager_review_deadline = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", backref="performance_appraisals")
    appraisals = relationship("PerformanceFeedback", backref="appraisal")


class PerformanceFeedback(Base):
    """360-degree feedback and manager reviews"""
    __tablename__ = "performance_feedback"

    id = Column(Integer, primary_key=True, index=True)
    appraisal_id = Column(Integer, ForeignKey("performance_appraisals.id"))
    subject_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    reviewer_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    reviewer_type = Column(String, nullable=False)  # self, manager, peer, subordinate
    feedback_type = Column(String, nullable=False)  # strengths, weaknesses, goals, general
    rating = Column(Integer)  # 1-5 scale
    comments = Column(Text, nullable=False)
    kpi_scores = Column(Text)  # JSON: {"kpi_id": score}
    is_anonymous = Column(Boolean, default=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    subject = relationship("Employee", foreign_keys=[subject_id], backref="received_feedback")
    reviewer = relationship("Employee", foreign_keys=[reviewer_id], backref="given_feedback")


class PerformanceGoal(Base):
    """Employee performance goals"""
    __tablename__ = "performance_goals"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    kpi_id = Column(Integer, ForeignKey("kpis.id"))
    okr_id = Column(Integer, ForeignKey("okrs.id"))
    title = Column(String, nullable=False)
    description = Column(Text)
    target_value = Column(Decimal(10, 2))
    current_value = Column(Decimal(10, 2), default=0)
    unit = Column(String)
    deadline = Column(Date, nullable=False)
    status = Column(String, default="not_started")  # not_started, in_progress, completed, overdue
    progress = Column(Integer, default=0)  # Percentage
    ai_suggestions = Column(Text)  # AI-generated improvement suggestions
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    employee = relationship("Employee", backref="performance_goals")
    kpi = relationship("KPI", backref="goals")
    okr = relationship("OKR", backref="goals")


# ========== Analytics & BI Module ==========

class AnalyticsMetric(Base):
    """Cached analytics metrics"""
    __tablename__ = "analytics_metrics"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    metric_type = Column(String, nullable=False)  # workforce, payroll, attrition, hiring, cost
    metric_name = Column(String, nullable=False)
    metric_value = Column(Decimal(15, 2))
    period = Column(String, nullable=False)  # daily, weekly, monthly, quarterly, yearly
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    dimensions = Column(Text)  # JSON: breakdowns by department, role, etc.
    extra_data = Column(Text)  # JSON: additional context
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    company = relationship("Company", backref="analytics_metrics")


class WorkforceAnalytics(Base):
    """Workforce analytics data"""
    __tablename__ = "workforce_analytics"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    period = Column(String, nullable=False)  # Q1 2024, H1 2024
    total_employees = Column(Integer, default=0)
    new_hires = Column(Integer, default=0)
    departures = Column(Integer, default=0)
    attrition_rate = Column(Decimal(5, 2), default=0)
    headcount_by_department = Column(Text)  # JSON
    headcount_by_role = Column(Text)  # JSON
    average_tenure = Column(Decimal(5, 2))
    gender_diversity = Column(Text)  # JSON
    age_distribution = Column(Text)  # JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    company = relationship("Company", backref="workforce_analytics")


class PayrollAnalytics(Base):
    """Payroll analytics data"""
    __tablename__ = "payroll_analytics"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    period = Column(String, nullable=False)  # January 2024
    total_payroll = Column(Decimal(15, 2), default=0)
    average_salary = Column(Decimal(12, 2), default=0)
    salary_by_department = Column(Text)  # JSON
    salary_by_role = Column(Text)  # JSON
    total_overtime_hours = Column(Decimal(10, 2), default=0)
    total_overtime_cost = Column(Decimal(15, 2), default=0)
    total_benefits = Column(Decimal(15, 2), default=0)
    statutory_deductions = Column(Text)  # JSON: PAYE, NHIF, NSSF breakdown
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    company = relationship("Company", backref="payroll_analytics")


class HiringFunnel(Base):
    """Hiring pipeline analytics"""
    __tablename__ = "hiring_funnel"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    period = Column(String, nullable=False)
    job_posting_id = Column(Integer, ForeignKey("job_postings.id"))
    views = Column(Integer, default=0)
    applications = Column(Integer, default=0)
    screen_rate = Column(Decimal(5, 2), default=0)
    interviews_scheduled = Column(Integer, default=0)
    interview_rate = Column(Decimal(5, 2), default=0)
    offers_sent = Column(Integer, default=0)
    offer_acceptance_rate = Column(Decimal(5, 2), default=0)
    hires = Column(Integer, default=0)
    time_to_hire_days = Column(Integer)
    cost_per_hire = Column(Decimal(12, 2))
    stage_conversion = Column(Text)  # JSON: funnel stage conversion rates
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    company = relationship("Company", backref="hiring_funnels")


class CostTrend(Base):
    """Cost trend analytics"""
    __tablename__ = "cost_trends"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    cost_type = Column(String, nullable=False)  # payroll, recruitment, training, benefits
    period = Column(String, nullable=False)
    amount = Column(Decimal(15, 2), default=0)
    per_employee = Column(Decimal(12, 2), default=0)
    period_over_period = Column(Decimal(10, 2), default=0)  # Percentage change
    breakdown_by_department = Column(Text)  # JSON
    breakdown_by_cost_center = Column(Text)  # JSON
    forecast_next_period = Column(Decimal(15, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    company = relationship("Company", backref="cost_trends")


# ========== Payment & Payroll Disbursement Module ==========

class PaymentProvider(str, enum.Enum):
    EQUITY = "equity"
    KCB = "kcb"
    COOP = "coop"
    ABSA = "absa"
    NCBA = "ncba"
    STANBIC = "stanbic"
    STANDARD_CHARTERED = "standard_chartered"
    MPESA_B2C = "mpesa_b2c"
    AIRTEL_MONEY = "airtel_money"
    KCB_MPESA = "kcb_mpesa"
    EQUITY_MPESA = "equity_mpesa"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    REVERSED = "reversed"
    CANCELLED = "cancelled"


class BankAdapter(Base):
    """Bank payment adapters"""
    __tablename__ = "bank_adapters"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    provider = Column(Enum(PaymentProvider), nullable=False)
    adapter_name = Column(String, nullable=False)
    api_endpoint = Column(String, nullable=False)
    environment = Column(String, default="sandbox")  # sandbox, production
    is_active = Column(Boolean, default=True)
    configuration = Column(Text)  # JSON: authentication details
    last_tested_at = Column(DateTime(timezone=True))
    test_status = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", backref="bank_adapters")


class CredentialVault(Base):
    """Secure credential storage for payment adapters"""
    __tablename__ = "credential_vaults"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    adapter_id = Column(Integer, ForeignKey("bank_adapters.id"), nullable=False)
    credential_name = Column(String, nullable=False)
    encrypted_api_key = Column(Text, nullable=False)
    encrypted_api_secret = Column(Text)
    encrypted_cert_path = Column(Text)  # SSL certificate path
    merchant_id = Column(String)
    is_active = Column(Boolean, default=True)
    last_used_at = Column(DateTime(timezone=True))
    rotation_required = Column(Boolean, default=False)
    rotation_date = Column(Date)
    created_by = Column(Integer, ForeignKey("employees.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", backref="credential_vaults")
    adapter = relationship("BankAdapter", backref="credentials")


class PaymentBatch(Base):
    """Payment batch for disbursement"""
    __tablename__ = "payment_batches"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    payroll_cycle_id = Column(Integer, ForeignKey("payroll_cycles.id"), nullable=False)
    adapter_id = Column(Integer, ForeignKey("bank_adapters.id"))
    batch_name = Column(String, nullable=False)
    total_amount = Column(Decimal(15, 2), nullable=False)
    total_transactions = Column(Integer, default=0)
    currency = Column(String, default="KES")
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    maker_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    maker_approved_at = Column(DateTime(timezone=True))
    checker_id = Column(Integer, ForeignKey("employees.id"))
    checker_approved_at = Column(DateTime(timezone=True))
    external_batch_id = Column(String)  # Bank's reference ID
    external_status = Column(String)
    webhook_received = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", backref="payment_batches")
    payroll_cycle = relationship("PayrollCycle", backref="payment_batches")
    adapter = relationship("BankAdapter", backref="payment_batches")


class Payment(Base):
    """Individual payment transaction"""
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("payment_batches.id"), nullable=False, index=True)
    payroll_item_id = Column(Integer, ForeignKey("payroll_items.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    amount = Column(Decimal(12, 2), nullable=False)
    currency = Column(String, default="KES")
    payment_method = Column(String, nullable=False)  # bank_transfer, mpesa
    account_number = Column(String)
    account_name = Column(String)
    bank_code = Column(String)  # For EFT
    mpesa_phone_number = Column(String)  # For M-Pesa
    mpesa_transaction_id = Column(String)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    reference = Column(String)
    narrative = Column(Text)
    retry_count = Column(Integer, default=0)
    last_retry_at = Column(DateTime(timezone=True))
    webhook_status = Column(String)  # delivered, failed
    webhook_delivered_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    batch = relationship("PaymentBatch", backref="payments")
    employee = relationship("Employee", backref="payments")


class MPesaTransaction(Base):
    """M-Pesa transaction details"""
    __tablename__ = "mpesa_transactions"

    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=False, unique=True)
    transaction_id = Column(String, nullable=False)
    conversation_id = Column(String)
    transaction_timestamp = Column(DateTime(timezone=True))
    amount = Column(Decimal(12, 2), nullable=False)
    phone_number = Column(String, nullable=False)
    receipt_number = Column(String)
    merchant_request_id = Column(String)
    result_code = Column(Integer)
    result_description = Column(Text)
    callback_received = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ========== Subscription Billing & Plan Management Module ==========

class SubscriptionPlan(str, enum.Enum):
    FREE = "free"
    STARTER = "starter"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"


class FeatureCode(str, enum.Enum):
    HR_MANAGEMENT = "hr_management"
    PAYROLL_PROCESSING = "payroll_processing"
    RECRUITMENT = "recruitment"
    AI_FEATURES = "ai_features"
    STATUTORY_COMPLIANCE = "statutory_compliance"
    TIME_ATTENDANCE = "time_attendance"
    PERFORMANCE_MANAGEMENT = "performance_management"
    ANALYTICS = "analytics"
    API_ACCESS = "api_access"
    CUSTOM_REPORTS = "custom_reports"
    PRIORITY_SUPPORT = "priority_support"
    DEDICATED_ACCOUNT_MANAGER = "dedicated_account_manager"
    WHITE_LABELING = "white_labeling"


class Plan(Base):
    """Subscription plans"""
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(Enum(SubscriptionPlan), unique=True, nullable=False)
    description = Column(Text)
    max_employees = Column(Integer)
    price_per_employee = Column(Decimal(10, 2))
    base_price = Column(Decimal(10, 2))  # Minimum monthly price
    billing_cycle = Column(String, default="monthly")  # monthly, yearly
    features = Column(Text)  # JSON: array of FeatureCode
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    subscriptions = relationship("CompanySubscription", backref="plan")


class CompanySubscription(Base):
    """Company subscription details"""
    __tablename__ = "company_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, unique=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    status = Column(String, default="active")  # active, trialing, cancelled, expired
    start_date = Column(Date, nullable=False)
    next_billing_date = Column(Date, nullable=False)
    cancellation_date = Column(Date)
    max_employees = Column(Integer)
    current_employee_count = Column(Integer, default=0)
    per_employee_rate = Column(Decimal(10, 2))
    monthly_total = Column(Decimal(15, 2))
    currency = Column(String, default="KES")
    is_auto_renew = Column(Boolean, default=True)
    trial_days_used = Column(Integer, default=0)
    trial_ends_at = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", backref="subscription")
    invoices = relationship("Invoice", backref="subscription")


class Invoice(Base):
    """Subscription invoices"""
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("company_subscriptions.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    invoice_number = Column(String, unique=True, nullable=False)
    billing_period_start = Column(Date, nullable=False)
    billing_period_end = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    amount = Column(Decimal(15, 2), nullable=False)
    currency = Column(String, default="KES")
    status = Column(String, default="draft")  # draft, sent, paid, overdue, cancelled
    pdf_url = Column(String)  # Generated invoice PDF
    sent_at = Column(DateTime(timezone=True))
    paid_at = Column(DateTime(timezone=True))
    payment_method = Column(String)
    payment_reference = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", backref="invoices")


class UsageRecord(Base):
    """Feature usage tracking"""
    __tablename__ = "usage_records"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    period = Column(String, nullable=False)  # 2024-01
    feature = Column(String, nullable=False)
    usage_count = Column(Integer, default=0)
    usage_limit = Column(Integer)
    unit = Column(String, default="count")  # count, employees, api_calls, tokens
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    company = relationship("Company", backref="usage_records")


# ========== Fine-grained Permissions Module ==========

class Permission(Base):
    """System permissions"""
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    module = Column(String, nullable=False)  # hr, payroll, recruitment, admin
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RolePermission(Base):
    """Role-permission mappings (company-specific)"""
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    role = Column(String, nullable=False)  # super_admin, company_admin, hr_manager, etc.
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False)
    is_granted = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("employees.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", backref="role_permissions")
    permission = relationship("Permission")


class CustomRole(Base):
    """Company-specific custom roles"""
    __tablename__ = "custom_roles"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    permissions = Column(Text)  # JSON array of permission codes
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("employees.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", backref="custom_roles")


# ========== Audit Logging Module ==========

class AuditAction(str, enum.Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    APPROVE = "approve"
    REJECT = "reject"
    EXPORT = "export"
    IMPORT = "import"
    PAY = "pay"


class AuditLog(Base):
    """Immutable audit logs for all sensitive actions"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), index=True)
    user_id = Column(Integer, ForeignKey("employees.id"))
    action = Column(Enum(AuditAction), nullable=False)
    resource_type = Column(String, nullable=False)  # employee, payroll, leave, etc.
    resource_id = Column(Integer)
    old_values = Column(Text)  # JSON: previous state
    new_values = Column(Text)  # JSON: new state
    ip_address = Column(String)
    user_agent = Column(String)
    extra_data = Column(Text)  # JSON: additional context
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    company = relationship("Company", backref="audit_logs")
    user = relationship("Employee", backref="audit_logs")


# ========== Webhook & Integration Framework Module ==========

class WebhookEvent(str, enum.Enum):
    PAYROLL_PROCESSED = "payroll.processed"
    PAYROLL_PAID = "payroll.paid"
    EMPLOYEE_CREATED = "employee.created"
    EMPLOYEE_UPDATED = "employee.updated"
    EMPLOYEE_TERMINATED = "employee.terminated"
    LEAVE_REQUESTED = "leave.requested"
    LEAVE_APPROVED = "leave.approved"
    APPLICATION_RECEIVED = "application.received"
    INTERVIEW_SCHEDULED = "interview.scheduled"
    OFFER_ACCEPTED = "offer.accepted"
    PAYMENT_SUCCESS = "payment.success"
    PAYMENT_FAILED = "payment.failed"
    INVOICE_READY = "invoice.ready"


class Webhook(Base):
    """Webhook configurations"""
    __tablename__ = "webhooks"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    event = Column(Enum(WebhookEvent), nullable=False)
    secret = Column(String, nullable=False)  # HMAC secret for verification
    is_active = Column(Boolean, default=True)
    retry_policy = Column(String, default="exponential")  # none, linear, exponential
    max_retries = Column(Integer, default=3)
    headers = Column(Text)  # JSON: additional headers
    description = Column(Text)
    last_triggered_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", backref="webhooks")


class WebhookDelivery(Base):
    """Webhook delivery logs"""
    __tablename__ = "webhook_deliveries"

    id = Column(Integer, primary_key=True, index=True)
    webhook_id = Column(Integer, ForeignKey("webhooks.id"), nullable=False)
    event_data = Column(Text, nullable=False)  # JSON payload
    http_status = Column(Integer)
    response_body = Column(Text)
    attempt_number = Column(Integer, default=1)
    delivered_at = Column(DateTime(timezone=True))
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    webhook = relationship("Webhook", backref="deliveries")


class ExternalIntegration(Base):
    """External system integrations (QuickBooks, Xero, ERP, etc.)"""
    __tablename__ = "external_integrations"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    integration_type = Column(String, nullable=False)  # quickbooks, xero, sage, custom_erp
    integration_name = Column(String, nullable=False)
    configuration = Column(Text, nullable=False)  # JSON: credentials, settings
    sync_direction = Column(String, default="bidirectional")  # inbound, outbound, bidirectional
    last_sync_at = Column(DateTime(timezone=True))
    sync_status = Column(String, default="idle")  # idle, syncing, error
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", backref="integrations")


# ========== Background Job Processing Module ==========

class BackgroundJobStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class BackgroundJob(Base):
    """Background job tracking"""
    __tablename__ = "background_jobs"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), index=True)
    job_type = Column(String, nullable=False)  # payroll_processing, email_sending, report_generation
    priority = Column(Integer, default=5)  # 1-10, 1 = highest
    payload = Column(Text)  # JSON: job parameters
    status = Column(Enum(BackgroundJobStatus), default=BackgroundJobStatus.PENDING)
    progress = Column(Integer, default=0)  # 0-100
    result = Column(Text)  # JSON: output data
    error_message = Column(Text)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    next_retry_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    company = relationship("Company", backref="background_jobs")


class JobLog(Base):
    """Background job logs"""
    __tablename__ = "job_logs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("background_jobs.id"), nullable=False)
    level = Column(String, nullable=False)  # INFO, WARNING, ERROR
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    job = relationship("BackgroundJob", backref="logs")

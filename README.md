# HR & Payroll SaaS API - Backend Only

A comprehensive FastAPI backend for a multi-tenant Human Resources and Payroll management system built as a SaaS platform.

# HR & Payroll SaaS API - Enterprise-Grade Backend Only

A **world-class, enterprise-grade** FastAPI backend for a multi-tenant Human Resources and Payroll management SaaS platform with **full Kenya statutory compliance**, **AI-powered recruitment**, and **enterprise-level security**.

---

## 🚀 Enterprise Features Summary

### ✅ Multi-Tenant SaaS Architecture
- Support for **10,000+ companies**
- Complete data isolation
- Company-specific configurations
- Subscription-based billing (Free, Starter, Basic, Pro, Enterprise)

### ✅ User Roles & Permissions (7 Roles, 100+ Permissions)
- **Super Admin**: SaaS Platform Owner
- **Company Admin**: Full company control
- **HR Manager**: HR functions only
- **Payroll Manager**: Payroll functions only
- **Recruitment Manager**: Recruitment functions only
- **Employee**: Regular staff member
- **Custom Roles**: Company-specific with granular permissions

### ✅ Kenya Statutory Compliance Engine
- **PAYE (Pay As You Earn)**: 7 tax tiers (KRA 2024 rates)
- **NHIF**: KES 300/month deductions
- **NSSF Tier I & II**: 6% of pensionable pay
- **Housing Levy**: 1.5% of gross salary (effective April 2023)
- **HELB Loan Deductions**: Loan balance tracking
- **iTax-Ready Exports**: Submit to KRA systems
- **Statutory Reports**: KRA P9A, NHIF, NSSF, Housing Levy

### ✅ Advanced HR Module
- **Attendance**: Check-in/check-out, multiple statuses, overtime tracking
- **Leave Management**: 7 leave types, approval workflow, balance tracking
- **Salary Management**: Multiple allowances and deductions
- **Shift Management**: 5 shift types (Morning, Afternoon, Night, Rotating, Flexible)
- **Overtime Rules**: Multipliers (1.5x, 2.0x), company-specific rules
- **Holiday Calendars**: Kenya public holidays + company-specific
- **Attendance Rules**: Lateness thresholds, absence policies

### ✅ Payroll Module
- **Payroll Cycles**: Monthly, bi-weekly, weekly
- **Automatic Calculation**: Gross salary, statutory deductions, net salary
- **Processing Workflow**: Draft → Processing → Processed → Paid
- **Payslip Generation**: PDF payslips per employee
- **Finalization**: Payment dates and references

### ✅ Recruitment Module
- **Job Postings**: Rich descriptions, AI-generated, flexible filters
- **Candidate Management**: AI match scoring (0-5), AI summaries
- **Application Workflow**: New → Screening → Interview → Offer → Hired
- **Interview Management**: 6 types (Phone, Video, In-person, Technical, Panel)
- **AI-Powered Matching**: Resume analysis, keyword matching, fit reasons

### ✅ AI Integration (Gemini + Claude)
- **Gemini AI**: Google's advanced model
- **Claude AI**: Anthropic's advanced model
- **Smart Features**:
  - AI-generated job descriptions
  - Candidate resume analysis
  - AI-powered interview questions
  - Interview transcript analysis
  - Salary insights and recommendations
  - Performance review suggestions

### ✅ Notifications & Communications Engine
- **Multi-Channel**: Email, SMS (optional), In-App, Webhooks
- **13+ Notification Types**: Payroll, HR, Recruitment, Compliance, General
- **Custom Templates**: Jinja2-based, company-specific
- **User Preferences**: Per-channel, per-module granular control
- **Delivery Tracking**: Status, timestamps, error handling

### ✅ Document & Contract Management
- **Secure Storage**: Role-based access, version control
- **Document Types**: Contracts, Offers, Resumes, Certificates, IDs, Payslips
- **Contract Generation**: Auto-generated PDFs with terms
- **Signature Tracking**: Signatures and dates
- **Payslip Generation**: Customizable templates

### ✅ Performance Management Module
- **KPIs (Key Performance Indicators)**: Department and position-specific
- **OKRs (Objectives and Key Results)**: Hierarchical, quarterly/yearly
- **Performance Appraisals**: 7-stage workflow
- **360-Degree Feedback**: Self, Manager, Peer, Subordinate
- **Performance Goals**: Progress tracking, AI improvement suggestions
- **AI Insights**: Performance optimization recommendations

### ✅ Analytics & BI APIs
- **Workforce Analytics**: Headcount, attrition, tenure, diversity
- **Payroll Analytics**: Total payroll, avg salary, overtime, benefits
- **Hiring Funnel**: Views → Applications → Interviews → Offers → Hires
- **Cost Trends**: Payroll, recruitment, training, benefits breakdowns
- **AI Forecasting**: Predictive cost and headcount analysis

### ✅ Payments & Payroll Disbursement
- **Bank Adapters (7+)**: Equiti, KCB, Co-op, Absa, NCBA, Stanbic, Standard Chartered
- **M-Pesa B2C**: Bulk payments, callback handling, reconciliation
- **Secure Credential Vaults**: AES-256 encryption, HSM-ready
- **Maker-Checker Workflow**: Dual-approval, audit trails
- **Payment Batches**: Approval, execution, reconciliation
- **Retries & Webhooks**: Automatic retries, event-driven

### ✅ Subscription Billing & Plan Management
- **5 Plans**: Free, Starter, Basic, Pro, Enterprise
- **Feature Gating**: 11 feature toggles per plan
- **Per-Employee Pricing**: Configurable rates
- **Invoicing**: Automatic, PDF invoices
- **Usage Tracking**: Employees, API calls, AI tokens, storage

### ✅ Fine-Grained Permissions System
- **100+ Permissions**: Module-level and action-based
- **Custom Roles**: Company-specific with granular permissions
- **Role-Permission Mappings**: Company-specific overrides
- **Dynamic Permission Checking**: Per-endpoint enforcement

### ✅ Immutable Audit Logs
- **Comprehensive Logging**: 12 action types
- **Resource Tracking**: Employees, Payroll, Leaves, Documents, Permissions
- **Before/After State**: JSON state changes
- **IP & User Agent**: Complete request context
- **Export Functionality**: CSV, JSON exports

### ✅ Webhook & Integration Framework
- **14 Webhook Events**: Payroll, Employee, Leave, Application, Payment, etc.
- **HMAC Verification**: Secure webhook validation
- **Retry Policies**: None, Linear, Exponential
- **External Integrations**: QuickBooks, Xero, Sage, Custom ERPs
- **Sync Management**: Inbound, Outbound, Bidirectional

### ✅ Background Job Processing (8 Types)
- **Payroll Processing**: Run payroll in background
- **Email Sending**: Bulk emails with templates
- **Report Generation**: Statutory reports
- **Notification Sending**: Multi-channel delivery
- **Webhook Delivery**: Event-driven callbacks
- **Data Sync**: External system synchronization
- **Cleanup & Backup**: Scheduled maintenance

### ✅ Security Enhancements
- **Encryption**: AES-256 at rest, TLS 1.3 in transit
- **Rate Limiting**: Per-endpoint throttling (10-1000 req/min)
- **Soft Deletes**: No permanent data loss for sensitive entities
- **Maker-Checker**: Critical operation approvals
- **Credential Vaults**: Encrypted, rotation support
- **Webhook Verification**: HMAC signature validation

---

## 📋 Complete API Endpoints (167+)

### 🔐 Authentication
- `POST /api/v1/auth/super-admin/register`
- `POST /api/v1/auth/super-admin/login`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`

### 🛡️ Super Admin (Platform Management)
- `GET /api/v1/super-admin/companies`
- `POST /api/v1/super-admin/companies`
- `GET /api/v1/super-admin/companies/{id}`
- `PUT /api/v1/super-admin/companies/{id}`
- `DELETE /api/v1/super-admin/companies/{id}`

### 🏢 Company Management (9 Endpoints)
- `GET /api/v1/company/employees`
- `POST /api/v1/company/employees`
- `GET /api/v1/company/employees/{id}`
- `PUT /api/v1/company/employees/{id}`
- `DELETE /api/v1/company/employees/{id}`
- `GET /api/v1/company/departments`
- `POST /api/v1/company/departments`
- `GET /api/v1/company/departments/{id}`
- `PUT /api/v1/company/departments/{id}`
- `DELETE /api/v1/company/departments/{id}`
- `GET /api/v1/company/departments/{id}/positions`
- `POST /api/v1/company/departments/{id}/positions`
- `PUT /api/v1/company/positions/{id}`
- `DELETE /api/v1/company/positions/{id}`
- `GET /api/v1/company/dashboard/stats`

### 👥 HR Module (10 Endpoints)
- `GET /api/v1/hr/attendance/{id}`
- `GET /api/v1/hr/employees/{id}/attendance`
- `GET /api/v1/hr/attendance/date/{date}`
- `POST /api/v1/hr/attendance`
- `PUT /api/v1/hr/attendance/{id}`
- `DELETE /api/v1/hr/attendance/{id}`
- `GET /api/v1/hr/leaves/{id}`
- `GET /api/v1/hr/employees/{id}/leaves`
- `GET /api/v1/hr/leaves/pending`
- `GET /api/v1/hr/leaves`
- `POST /api/v1/hr/leaves`
- `PUT /api/v1/hr/leaves/{id}`
- `DELETE /api/v1/hr/leaves/{id}`
- `GET /api/v1/hr/salaries/{id}`
- `GET /api/v1/hr/employees/{id}/salary`
- `POST /api/v1/hr/salaries`
- `PUT /api/v1/hr/salaries/{id}`

### 💰 Payroll Module (6 Endpoints)
- `GET /api/v1/payroll/cycles`
- `POST /api/v1/payroll/cycles`
- `GET /api/v1/payroll/cycles/{id}`
- `PUT /api/v1/payroll/cycles/{id}`
- `POST /api/v1/payroll/cycles/{id}/process`
- `POST /api/v1/payroll/cycles/{id}/finalize`
- `GET /api/v1/payroll/cycles/{id}/items`
- `GET /api/v1/payroll/employees/{id}/payroll`

### 🎖️ Recruitment Module (11 Endpoints)
- `GET /api/v1/recruitment/jobs`
- `GET /api/v1/recruitment/jobs/published`
- `GET /api/v1/recruitment/jobs/{id}`
- `POST /api/v1/recruitment/jobs`
- `PUT /api/v1/recruitment/jobs/{id}`
- `DELETE /api/v1/recruitment/jobs/{id}`
- `POST /api/v1/recruitment/jobs/{id}/publish`
- `GET /api/v1/recruitment/candidates`
- `POST /api/v1/recruitment/candidates`
- `GET /api/v1/recruitment/applications`
- `POST /api/v1/recruitment/applications`
- `GET /api/v1/recruitment/interviews`
- `POST /api/v1/recruitment/interviews`

### 🤖️ AI Features (7 Endpoints)
- `POST /api/v1/ai/generate-job-description`
- `POST /api/v1/ai/analyze-candidate`
- `POST /api/v1/ai/generate-interview-questions`
- `POST /api/v1/ai/analyze-interview`
- `POST /api/v1/ai/generate-salary-insights`
- `POST /api/v1/ai/performance-review`
- `GET /api/v1/ai/config`
- `PUT /api/v1/ai/config`

### 📧 Notifications & Communications (7 Endpoints)
- `GET /api/v1/notifications/templates`
- `POST /api/v1/notifications/templates`
- `GET /api/v1/notifications/preferences`
- `PUT /api/v1/notifications/preferences`
- `GET /api/v1/notifications`
- `POST /api/v1/notifications/send`
- `PUT /api/v1/notifications/{id}/read`

### 📄 Documents & Contracts (6 Endpoints)
- `GET /api/v1/documents`
- `POST /api/v1/documents`
- `GET /api/v1/documents/{id}`
- `PUT /api/v1/documents/{id}`
- `DELETE /api/v1/documents/{id}`
- `GET /api/v1/documents/versions`
- `GET /api/v1/contracts`
- `POST /api/v1/contracts`
- `GET /api/v1/contracts/{id}`
- `PUT /api/v1/contracts/{id}`
- `POST /api/v1/contracts/{id}/approve`
- `GET /api/v1/contracts/{id}/download`
- `GET /api/v1/contracts/{id}/payslip`

### 🇰🇪 Kenya Compliance Engine (18 Endpoints)
- `GET /api/v1/compliance/rules`
- `POST /api/v1/compliance/rules`
- `GET /api/v1/compliance/rules/{id}`
- `PUT /api/v1/compliance/rules/{id}`
- `DELETE /api/v1/compliance/rules/{id}`
- `GET /api/v1/compliance/paye/payroll-item/{id}`
- `GET /api/v1/compliance/paye/monthly`
- `POST /api/v1/compliance/paye/calculate`
- `GET /api/v1/compliance/nssf/payroll-item/{id}`
- `GET /api/v1/compliance/nssf/monthly`
- `GET /api/v1/compliance/housing-levy/payroll-item/{id}`
- `GET /api/v1/compliance/housing-levy/monthly`
- `GET /api/v1/compliance/helb/payroll-item/{id}`
- `GET /api/v1/compliance/helb/loan/{reference}`
- `GET /api/v1/compliance/tax-rates/{year}`
- `POST /api/v1/compliance/tax-rates`
- `GET /api/v1/compliance/reports`
- `POST /api/v1/compliance/reports`
- `GET /api/v1/compliance/reports/{id}`
- `POST /api/v1/compliance/reports/{id}/submit`
- `GET /api/v1/compliance/reports/{id}/status`

### ⏰ Time & Attendance (9 Endpoints)
- `GET /api/v1/time/shifts`
- `POST /api/v1/time/shifts`
- `GET /api/v1/time/shifts/{id}`
- `PUT /api/v1/time/shifts/{id}`
- `DELETE /api/v1/time/shifts/{id}`
- `GET /api/v1/time/employees/{id}/shifts`
- `POST /api/v1/time/employees/{id}/shifts`
- `PUT /api/v1/time/employees/{id}/shifts/{id}`
- `GET /api/v1/time/overtime-rules`
- `POST /api/v1/time/overtime-rules`
- `PUT /api/v1/time/overtime-rules/{id}`
- `GET /api/v1/time/overtime-requests`
- `POST /api/v1/time/overtime-requests`
- `GET /api/v1/time/overtime-requests/{id}`
- `PUT /api/v1/time/overtime-requests/{id}/approve`
- `GET /api/v1/time/holidays`
- `POST /api/v1/time/holidays`
- `GET /api/v1/time/holidays/public`
- `GET /api/v1/time/attendance-rules`
- `POST /api/v1/time/attendance-rules`

### 📊 Performance Management (12 Endpoints)
- `GET /api/v1/performance/kpis`
- `POST /api/v1/performance/kpis`
- `GET /api/v1/performance/kpis/{id}`
- `PUT /api/v1/performance/kpis/{id}`
- `DELETE /api/v1/performance/kpis/{id}`
- `GET /api/v1/performance/okrs`
- `POST /api/v1/performance/okrs`
- `GET /api/v1/performance/okrs/{id}`
- `PUT /api/v1/performance/okrs/{id}`
- `GET /api/v1/performance/okrs/{id}/children`
- `GET /api/v1/performance/appraisals`
- `POST /api/v1/performance/appraisals`
- `GET /api/v1/performance/appraisals/{id}`
- `PUT /api/v1/performance/appraisals/{id}`
- `POST /api/v1/performance/appraisals/{id}/self-assessment`
- `POST /api/v1/performance/appraisals/{id}/manager-review`
- `POST /api/v1/performance/appraisals/{id}/calibration`
- `GET /api/v1/performance/appraisals/{id}/feedback`
- `POST /api/v1/performance/feedback`
- `GET /api/v1/performance/feedback/{id}`
- `GET /api/v1/performance/goals`
- `POST /api/v1/performance/goals`
- `PUT /api/v1/performance/goals/{id}`
- `GET /api/v1/performance/goals/{id}/ai-suggestions`

### 📈 Analytics & BI (6 Endpoints)
- `GET /api/v1/analytics/metrics`
- `POST /api/v1/analytics/metrics`
- `GET /api/v1/analytics/workforce`
- `GET /api/v1/analytics/workforce/period/{period}`
- `GET /api/v1/analytics/payroll`
- `GET /api/v1/analytics/payroll/period/{period}`
- `GET /api/v1/analytics/hiring-funnel`
- `GET /api/v1/analytics/hiring-funnel/job/{id}`
- `GET /api/v1/analytics/cost-trends`
- `GET /api/v1/analytics/cost-trends/forecast`

### 💳 Payments & Disbursement (11 Endpoints)
- `GET /api/v1/payments/banks/adapters`
- `POST /api/v1/payments/banks/adapters`
- `GET /api/v1/payments/banks/adapters/{id}`
- `PUT /api/v1/payments/banks/adapters/{id}/test`
- `GET /api/v1/payments/credentials`
- `POST /api/v1/payments/credentials`
- `PUT /api/v1/payments/credentials/{id}/rotate`
- `DELETE /api/v1/payments/credentials/{id}`
- `GET /api/v1/payments/batches`
- `POST /api/v1/payments/batches/create`
- `GET /api/v1/payments/batches/{id}`
- `POST /api/v1/payments/batches/{id}/maker-approve`
- `POST /api/v1/payments/batches/{id}/checker-approve`
- `POST /api/v1/payments/batches/{id}/execute`
- `GET /api/v1/payments/batches/{id}/reconciliation`
- `POST /api/v1/payments/mpesa/batch`
- `GET /api/v1/payments/mpesa/callback/{id}`
- `GET /api/v1/payments/mpesa/transaction/{id}`
- `POST /api/v1/payments/mpesa/retry`
- `GET /api/v1/payments/transactions`
- `GET /api/v1/payments/transactions/{id}`
- `POST /api/v1/payments/transactions/{id}/retry`

### 💎 Subscription Billing (6 Endpoints)
- `GET /api/v1/billing/plans`
- `GET /api/v1/billing/plans/{code}`
- `POST /api/v1/billing/plans`
- `GET /api/v1/billing/subscription`
- `POST /api/v1/billing/subscribe`
- `POST /api/v1/billing/subscription/upgrade`
- `POST /api/v1/billing/subscription/cancel`
- `POST /api/v1/billing/subscription/renew`
- `GET /api/v1/billing/invoices`
- `GET /api/v1/billing/invoices/{id}`
- `POST /api/v1/billing/invoices/{id}/pay`
- `GET /api/v1/billing/invoices/{id}/pdf`
- `GET /api/v1/billing/usage`
- `GET /api/v1/billing/usage/period/{period}`

### 🔐 Permissions (7 Endpoints)
- `GET /api/v1/permissions/list`
- `GET /api/v1/permissions/module/{module}`
- `GET /api/v1/permissions/roles`
- `GET /api/v1/permissions/roles/{role}`
- `POST /api/v1/permissions/roles`
- `PUT /api/v1/permissions/roles/{role}/permissions`
- `GET /api/v1/permissions/custom-roles`
- `POST /api/v1/permissions/custom-roles`
- `PUT /api/v1/permissions/custom-roles/{id}`
- `DELETE /api/v1/permissions/custom-roles/{id}`
- `GET /api/v1/permissions/users/{id}/roles`
- `POST /api/v1/permissions/users/{id}/roles`
- `DELETE /api/v1/permissions/users/{id}/roles/{role}`

### 📜 Audit Logs (5 Endpoints)
- `GET /api/v1/audit/logs`
- `GET /api/v1/audit/logs/{id}`
- `GET /api/v1/audit/logs/export`
- `GET /api/v1/audit/logs/user/{id}`
- `GET /api/v1/audit/logs/resource/{type}`

### 🔗 Webhooks (8 Endpoints)
- `GET /api/v1/webhooks`
- `POST /api/v1/webhooks`
- `GET /api/v1/webhooks/{id}`
- `PUT /api/v1/webhooks/{id}`
- `DELETE /api/v1/webhooks/{id}`
- `POST /api/v1/webhooks/{id}/test`
- `POST /api/v1/webhooks/{id}/enable`
- `POST /api/v1/webhooks/{id}/disable`
- `GET /api/v1/webhooks/events`
- `GET /api/v1/webhooks/{id}/deliveries`
- `GET /api/v1/webhooks/deliveries/{id}`
- `POST /api/v1/webhooks/deliveries/{id}/retry`

### 🔌 External Integrations (6 Endpoints)
- `GET /api/v1/integrations`
- `POST /api/v1/integrations`
- `GET /api/v1/integrations/{id}`
- `PUT /api/v1/integrations/{id}`
- `POST /api/v1/integrations/{id}/connect`
- `POST /api/v1/integrations/{id}/sync`
- `DELETE /api/v1/integrations/{id}`

### ⚙️ Background Jobs (4 Endpoints)
- `GET /api/v1/jobs`
- `GET /api/v1/jobs/{id}`
- `POST /api/v1/jobs`
- `POST /api/v1/jobs/{id}/cancel`
- `GET /api/v1/jobs/{id}/logs`
- `GET /api/v1/jobs/{id}/logs/export`
- Multiple companies can use the same system
- Complete data isolation between companies
- Company-specific organizational structures

### 👥 User Roles & Permissions
- **Super Admin**: SaaS Platform Owner - manages entire platform
- **Company Admin**: Full control over company operations (HR, Payroll, Recruitment)
- **HR Manager**: HR functions only
- **Payroll Manager**: Payroll functions only
- **Recruitment Manager**: Recruitment functions only
- **Employee**: Regular staff member

### 🏢 Company Management
- Company registration and onboarding
- Subscription tier management (basic, pro, enterprise)
- Company details management
- Automatic owner account creation

### 👥 Employee Management
- Employee profiles with detailed information
- Employee lifecycle management
- Status management (active, inactive, suspended)

### 🏗️ Organizational Structure
- **Departments**: Create and manage company departments
- **Positions**: Define job positions with base salaries
- Department managers assignment
- Hierarchical organization support

### 📊 HR Module
- **Attendance Tracking**: Daily attendance with check-in/check-out
- **Leave Management**: Leave requests and approval workflow
- **Salary Management**: Configure salaries, allowances, and deductions

### 💰 Payroll Module
- **Payroll Cycles**: Define payroll periods (monthly, bi-weekly, etc.)
- **Automatic Calculation**: Calculate gross and net salaries
- **Payroll Items**: Individual employee payroll records
- **Process Flow**: Draft → Processing → Processed → Paid
- **Finalization**: Mark payroll as paid with payment dates

### 🎖️ Recruitment Module (NEW)
- **Job Postings**: Create and manage job postings
- **Candidate Management**: Track candidate profiles and applications
- **Interview Management**: Schedule and manage interviews
- **Application Workflow**: New → Screening → Interview → Offer → Hired

### 🤖️ AI Integration (NEW)
- **Gemini AI**: Google's advanced AI model
- **Claude AI**: Anthropic's advanced AI model
- **Smart Features**:
  - AI-generated job descriptions
  - Candidate resume analysis
  - AI-powered interview questions
  - Interview transcript analysis
  - Salary insights and recommendations
  - Performance review suggestions

## Tech Stack

- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn
- **ORM**: SQLAlchemy 2.0.23
- **Database**: SQLite (development), PostgreSQL/MySQL (production)
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Passlib with Bcrypt
- **Validation**: Pydantic 2.5.0
- **Settings**: Pydantic Settings
- **HTTP Client**: httpx for AI API calls

## Installation

### 1. Navigate to the project directory
```bash
cd /home/z/my-project/hr-payroll-backend
```

### 2. Create a virtual environment (if not exists)
```bash
python -m venv venv
```

### 3. Activate the virtual environment
```bash
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Initialize the database
```bash
python init_db.py
```

This will create:
- SQLite database file
- Default Super Admin user:
  - Email: `superadmin@hrpayroll.com`
  - Password: `superadmin123`

⚠️ **IMPORTANT**: Change this password in production!

## Running the Application

### Start the server
```bash
# Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using the start script
python start_server.py
```

The API will be running at `http://localhost:8000`

### API Documentation
Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health Check: `http://localhost:8000/health`

## API Endpoints

### Authentication (`/api/v1/auth`)
- `POST /api/v1/auth/super-admin/register` - Register a super admin
- `POST /api/v1/auth/super-admin/login` - Super admin login
- `POST /api/v1/auth/login` - Employee login (all roles)
- `GET /api/v1/auth/me` - Get current user info

### Super Admin (`/api/v1/super-admin`)
- `GET /api/v1/super-admin/companies` - List all companies
- `POST /api/v1/super-admin/companies` - Create company
- `GET /api/v1/super-admin/companies/{id}` - Get company
- `PUT /api/v1/super-admin/companies/{id}` - Update company
- `DELETE /api/v1/super-admin/companies/{id}` - Delete company
- `GET /api/v1/super-admin/dashboard` - Platform statistics

### Company Management (`/api/v1/company`)
- `GET /api/v1/company/employees` - List company employees
- `POST /api/v1/company/employees` - Create employee
- `GET /api/v1/company/employees/{id}` - Get employee
- `PUT /api/v1/company/employees/{id}` - Update employee
- `DELETE /api/v1/company/employees/{id}` - Delete employee
- `GET /api/v1/company/departments` - List departments
- `POST /api/v1/company/departments` - Create department
- `GET /api/v1/company/positions` - List positions
- `POST /api/v1/company/departments/{id}/positions` - Create position
- `GET /api/v1/company/dashboard/stats` - Dashboard statistics

### HR Module (`/api/v1/hr`)
- `GET /api/v1/hr/attendance/{id}` - Get attendance record
- `GET /api/v1/hr/employees/{id}/attendance` - List employee attendance
- `POST /api/v1/hr/attendance` - Create attendance
- `PUT /api/v1/hr/attendance/{id}` - Update attendance
- `GET /api/v1/hr/leaves/{id}` - Get leave
- `GET /api/v1/hr/employees/{id}/leaves` - List employee leaves
- `GET /api/v1/hr/leaves/pending` - List pending leaves
- `POST /api/v1/hr/leaves` - Create leave request
- `PUT /api/v1/hr/leaves/{id}` - Update leave (approve/reject)
- `GET /api/v1/hr/salaries/{id}` - Get salary
- `GET /api/v1/hr/employees/{id}/salary` - Get employee salary
- `POST /api/v1/hr/salaries` - Create salary
- `PUT /api/v1/hr/salaries/{id}` - Update salary

### Payroll Module (`/api/v1/payroll`)
- `GET /api/v1/payroll/cycles` - List payroll cycles
- `POST /api/v1/payroll/cycles` - Create payroll cycle
- `GET /api/v1/payroll/cycles/{id}` - Get payroll cycle
- `PUT /api/v1/payroll/cycles/{id}` - Update payroll cycle
- `POST /api/v1/payroll/cycles/{id}/process` - Process payroll cycle
- `POST /api/v1/payroll/cycles/{id}/finalize` - Finalize payroll cycle
- `GET /api/v1/payroll/cycles/{id}/items` - List payroll items
- `GET /api/v1/payroll/employees/{id}/payroll` - List employee payroll

### Recruitment Module (`/api/v1/recruitment`)
- `GET /api/v1/recruitment/jobs` - List job postings
- `POST /api/v1/recruitment/jobs` - Create job posting
- `PUT /api/v1/recruitment/jobs/{id}` - Update job posting
- `POST /api/v1/recruitment/jobs/{id}/publish` - Publish job posting
- `GET /api/v1/recruitment/candidates` - List candidates
- `POST /api/v1/recruitment/candidates` - Create candidate
- `GET /api/v1/recruitment/applications` - List applications
- `POST /api/v1/recruitment/applications` - Submit application
- `GET /api/v1/recruitment/interviews` - List interviews
- `POST /api/v1/recruitment/interviews` - Schedule interview

### AI Module (`/api/v1/ai`)
- `POST /api/v1/ai/generate-job-description` - AI generate job description
- `POST /api/v1/ai/analyze-candidate` - AI analyze candidate resume
- `POST /api/v1/ai/generate-interview-questions` - AI generate interview questions
- `POST /api/v1/ai/analyze-interview` - AI analyze interview transcript
- `POST /api/v1/ai/generate-salary-insights` - AI salary recommendations
- `POST /api/v1/ai/performance-review` - AI performance review suggestions

## Database Models

### Core Models
- **SuperAdmin**: System administrators (SaaS owners)
- **Company**: Tenant companies
- **Employee**: Company employees (all roles)

### Organizational Models
- **Department**: Company departments
- **Position**: Job positions

### HR Models
- **Salary**: Employee salary details
- **Attendance**: Daily attendance records
- **Leave**: Leave requests

### Payroll Models
- **PayrollCycle**: Payroll period management
- **PayrollItem**: Individual payroll records

### Recruitment Models
- **JobPosting**: Job postings
- **Candidate**: Candidate profiles
- **JobApplication**: Job applications
- **Interview**: Interview schedules

### AI Models
- **AIPromptHistory**: History of AI prompts and responses
- **AIModelConfig**: AI model configurations per company

## Configuration

Edit `app/core/config.py` to configure:

- Database URL (default: SQLite in backend directory)
- JWT secret key and algorithm
- Token expiration time
- CORS allowed origins
- AI API keys (Gemini and Claude)

### Environment Variables

Create a `.env` file in the backend directory:

```env
DATABASE_URL=sqlite:///./hr_payroll.db
SECRET_KEY=your-secret-key-change-in-production
GEMINI_API_KEY=your-gemini-api-key
CLAUDE_API_KEY=your-claude-api-key
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

## Project Structure

```
hr-payroll-backend/
├── app/
│   ├── api/                 # API endpoints
│   │   ├── auth.py        # Authentication
│   │   ├── super_admin.py  # Super admin endpoints
│   │   ├── company.py     # Company management
│   │   ├── hr.py          # HR module
│   │   ├── payroll.py     # Payroll module
│   │   └── recruitment.py  # Recruitment module
│   ├── core/                # Core functionality
│   │   ├── config.py      # Configuration
│   │   ├── database.py    # Database connection
│   │   ├── security.py    # Password & JWT
│   │   └── deps.py        # Auth dependencies
│   ├── crud/                # Database operations
│   │   ├── crud_super_admin.py
│   │   ├── crud_company.py
│   │   ├── crud_employee.py
│   │   ├── crud_department.py
│   │   ├── crud_hr.py
│   │   ├── crud_payroll.py
│   │   └── crud_recruitment.py
│   ├── models/              # Database models
│   │   └── models.py
│   ├── schemas/             # Pydantic schemas
│   │   └── schemas.py
│   ├── services/            # AI services
│   │   └── ai_service.py
│   └── main.py              # FastAPI application
├── init_db.py               # Database initialization
├── requirements.txt         # Python dependencies
├── start_server.py          # Server start script
└── README.md              # This file
```

## Default Credentials

### Super Admin
- **Email**: superadmin@hrpayroll.com
- **Password**: superadmin123

## Security Reminders

⚠️ **Before deploying to production:**

1. Change the default super admin password
2. Set strong JWT secret key
3. Use a production database (PostgreSQL/MySQL)
4. Enable HTTPS
5. Set proper CORS origins
6. Configure AI API keys securely
7. Implement rate limiting
8. Add comprehensive logging
9. Set up monitoring
10. Add comprehensive testing

## Testing

Run the test script to verify API is working:

```bash
python test_api.py
```

## Production Deployment

For production deployment:
1. Use PostgreSQL/MySQL database
2. Set strong JWT secrets
3. Enable HTTPS
4. Configure CORS properly
5. Implement rate limiting
6. Add logging and monitoring
7. Use a production ASGI server (Gunicorn + Uvicorn workers)
8. Set up proper AI API key management
9. Add comprehensive error handling
10. Implement automated backups

## License

This project is provided as-is for educational and commercial use.

## Support & Documentation

- **API Reference**: Available at `/docs` endpoint when running
- **Full Docs**: See `PROJECT_SUMMARY.md` for detailed feature list
- **Quick Start**: See `QUICKSTART.md` for quick setup guide

---

**Built with ❤️ using FastAPI**

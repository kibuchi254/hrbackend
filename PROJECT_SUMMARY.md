# HR & Payroll SaaS API - Project Summary

## Overview
A comprehensive FastAPI backend for a multi-tenant Human Resources and Payroll management system built as a SaaS platform.

## Project Structure

```
hr-payroll-backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI application entry point
│   │
│   ├── api/                         # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py                  # Authentication endpoints
│   │   ├── admin.py                 # Admin management endpoints
│   │   ├── company.py               # Company & employee management
│   │   ├── hr.py                    # HR module (attendance, leaves, salary)
│   │   └── payroll.py               # Payroll processing
│   │
│   ├── core/                        # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py                # Configuration settings
│   │   ├── database.py              # Database connection
│   │   ├── security.py              # JWT & password hashing
│   │   └── deps.py                  # Authentication dependencies
│   │
│   ├── crud/                        # Database operations
│   │   ├── __init__.py
│   │   ├── crud_admin.py            # Admin CRUD operations
│   │   ├── crud_company.py          # Company CRUD operations
│   │   ├── crud_employee.py         # Employee CRUD operations
│   │   ├── crud_department.py       # Department & Position CRUD
│   │   ├── crud_hr.py               # Attendance, Leave, Salary CRUD
│   │   └── crud_payroll.py          # Payroll CRUD operations
│   │
│   ├── models/                      # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── models.py                # All database models
│   │
│   └── schemas/                     # Pydantic schemas
│       ├── __init__.py
│       └── schemas.py               # Request/response schemas
│
├── init_db.py                       # Database initialization with seed data
├── requirements.txt                 # Python dependencies
├── README.md                        # Full documentation
├── QUICKSTART.md                    # Quick start guide
├── .env.example                     # Environment variables template
└── .gitignore                       # Git ignore rules
```

## Key Features

### 1. Multi-Tenant SaaS Architecture
- Multiple companies can use the same system
- Complete data isolation between companies
- Company-specific organizational structures

### 2. Role-Based Access Control (RBAC)
Four distinct user roles with different permissions:

#### Admin (Super Admin)
- System-wide access
- Create and manage companies
- Manage other admins
- View all system data

#### Company Owner
- Full control over company operations
- Manage employees, departments, positions
- Process payroll
- Approve/reject leaves

#### Company Admin
- Employee management
- HR operations (attendance, leaves)
- Payroll processing
- Cannot delete company

#### Employee
- View own profile
- View own attendance
- Request and view own leaves
- View own payroll records

### 3. User Management
- Admin users (system-level)
- Company employees with different roles
- Employee profiles with detailed information
- Status management (active, inactive, suspended)

### 4. Company Management
- Company registration and onboarding
- Subscription tier management
- Company details management
- Automatic owner account creation

### 5. Organizational Structure
- **Departments**: Create and manage company departments
- **Positions**: Define job positions with base salaries
- Department managers assignment
- Hierarchical organization support

### 6. Attendance Management
- Daily attendance tracking
- Check-in/Check-out times
- Status tracking (present, absent, late, half-day, leave)
- Attendance notes
- Bulk attendance management

### 7. Leave Management
- Multiple leave types (annual, sick, maternity, paternity, etc.)
- Leave request workflow
- Approval/rejection by company admins
- Automatic leave day calculation
- Leave history tracking

### 8. Salary Management
- Base salary configuration
- Allowances (housing, transport, medical, others)
- Deductions (tax, insurance, others)
- Effective date tracking
- Employee-specific salary structures

### 9. Payroll Processing
- **Payroll Cycles**: Define payroll periods (monthly, bi-weekly, etc.)
- **Automatic Calculation**: Calculate gross and net salaries
- **Payroll Items**: Individual employee payroll records
- **Process Flow**: Draft → Processing → Processed → Paid
- **Finalization**: Mark payroll as paid with payment dates

### 10. Dashboard Statistics
- Total and active employees count
- Department count
- Payroll totals
- Pending leaves count
- Daily attendance summary

## Database Models

### Core Models
1. **Admin**: System administrators
2. **Company**: Tenant companies
3. **Employee**: Company employees (all roles)

### Organizational Models
4. **Department**: Company departments
5. **Position**: Job positions

### HR Models
6. **Salary**: Employee salary details
7. **Attendance**: Daily attendance records
8. **Leave**: Leave requests

### Payroll Models
9. **PayrollCycle**: Payroll period management
10. **PayrollItem**: Individual payroll records

## API Endpoints Summary

### Authentication (7 endpoints)
- Admin registration and login
- Employee login (all roles)
- Current user info

### Admin Management (5 endpoints)
- List, create, update, delete admins

### Company Management (15 endpoints)
- Admin endpoints for company management
- Company endpoints for employees, departments, positions
- Dashboard statistics

### HR Module (21 endpoints)
- Attendance (6 endpoints)
- Leave (7 endpoints)
- Salary (5 endpoints)
- Employee-specific endpoints (3 endpoints)

### Payroll Module (13 endpoints)
- Payroll cycle management (7 endpoints)
- Payroll item management (6 endpoints)

**Total: 61 API endpoints**

## Security Features

1. **JWT Authentication**: Secure token-based authentication
2. **Password Hashing**: Bcrypt for secure password storage
3. **Role-Based Authorization**: Endpoints protected by user roles
4. **Company Isolation**: Users can only access their company's data
5. **CORS Support**: Configurable CORS for frontend integration
6. **Token Expiration**: Configurable token lifetime

## Technology Stack

- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn
- **ORM**: SQLAlchemy 2.0.23
- **Database**: SQLite (development), PostgreSQL/MySQL (production)
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Passlib with Bcrypt
- **Validation**: Pydantic 2.5.0
- **Settings**: Pydantic Settings

## SaaS Features

1. **Multi-Tenancy**: Complete data isolation per company
2. **Subscription Tiers**: Support for different subscription levels
3. **Scalable Architecture**: Easy to add new features
4. **Admin Portal**: Super admin for managing companies
5. **Company Portal**: Full company management interface

## Installation & Quick Start

See [QUICKSTART.md](QUICKSTART.md) for step-by-step instructions.

### Basic Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Default Admin Credentials
- **Email**: admin@hrpayroll.com
- **Password**: admin123

## API Documentation

Once running, access interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Configuration

Key configuration options in `app/core/config.py`:
- Database URL
- JWT secret key and algorithm
- Token expiration time
- CORS allowed origins
- App name and version

## Next Steps for Production

1. **Change default passwords**
2. **Use production database** (PostgreSQL recommended)
3. **Set strong JWT secret**
4. **Enable HTTPS**
5. **Configure CORS properly**
6. **Add rate limiting**
7. **Implement logging**
8. **Set up monitoring**
9. **Add comprehensive testing**
10. **Deploy with proper ASGI server**

## Example Workflows

### 1. Company Onboarding
1. Admin creates company
2. System creates owner account automatically
3. Owner logs in and sets up company
4. Owner creates departments and positions
5. Owner adds employees
6. Owner configures employee salaries

### 2. Payroll Processing
1. Create payroll cycle
2. Process payroll (auto-calculates all salaries)
3. Review and adjust if needed
4. Finalize payroll (marks as paid)
5. Employees can view their payslips

### 3. Leave Management
1. Employee requests leave
2. Request appears in pending leaves
3. Manager reviews and approves/rejects
4. Employee receives notification
5. Leave history is maintained

## Scalability

The architecture supports:
- Adding new roles easily
- Extending HR features
- Adding new payroll types
- Integrating payment gateways
- Adding reporting and analytics
- Email notifications
- File uploads (documents, images)

## Extensibility Points

1. **Custom Leave Types**: Add more leave types
2. **Payment Integration**: Connect with payment gateways
3. **Notifications**: Email/SMS notifications
4. **Reports**: Custom payroll and HR reports
5. **Document Management**: Upload and store employee documents
6. **Time Tracking**: Integration with time tracking systems
7. **Benefits Management**: Additional benefits modules
8. **Performance Management**: Appraisals and reviews

## Support & Documentation

- **Full Documentation**: See [README.md](README.md)
- **Quick Start**: See [QUICKSTART.md](QUICKSTART.md)
- **API Reference**: Available at `/docs` endpoint when running

## License

This project is provided as-is for educational and commercial use.

---

**Built with ❤️ using FastAPI**

# HR & Payroll SaaS API

A comprehensive FastAPI backend for a multi-tenant Human Resources and Payroll management system.

## 🚀 Quick Start

### 1. Start the API Server

```bash
cd /home/z/my-project/hr-payroll-backend
./start.sh
```

This will:
- Check if virtual environment exists
- Initialize database if needed
- Start the API server on `http://localhost:8000`
- Display API documentation links

### 2. Stop the API Server

```bash
cd /home/z/my-project/hr-payroll-backend
./stop.sh
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔐 Default Admin Credentials

- **Email**: `admin@hrpayroll.com`
- **Password**: `admin123`

⚠️ **IMPORTANT**: Change this password in production!

## 📋 Project Structure

```
hr-payroll-backend/
├── app/
│   ├── api/              # API endpoints
│   │   ├── auth.py       # Authentication
│   │   ├── admin.py      # Admin management
│   │   ├── company.py    # Company & employee management
│   │   ├── hr.py         # HR module (attendance, leaves, salary)
│   │   └── payroll.py    # Payroll processing
│   ├── core/              # Core functionality
│   │   ├── config.py      # Configuration
│   │   ├── database.py    # Database connection
│   │   ├── security.py    # Password hashing & JWT
│   │   └── deps.py        # Auth dependencies
│   ├── crud/              # Database operations
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   └── main.py           # FastAPI app
├── venv/                   # Python virtual environment
├── hr_payroll.db          # SQLite database
├── init_db.py             # Database initialization
├── start.sh                # Start script
├── stop.sh                 # Stop script
├── requirements.txt         # Python dependencies
├── .env                    # Environment variables
└── README.md               # This file
```

## ✅ Features

### 1. Multi-Tenant SaaS Architecture
- Multiple companies with isolated data
- Company-specific organizational structures
- Subscription tier management

### 2. Role-Based Access Control (RBAC)

#### Admin (Super Admin)
- System-wide access
- Create and manage companies
- Manage other admins
- **Access**: `/api/v1/admin/*`

#### Company Owner
- Full company control
- Manage employees, departments, positions
- Process payroll
- Approve/reject leaves
- **Access**: `/api/v1/company/*`, `/api/v1/hr/*`, `/api/v1/payroll/*`

#### Company Admin
- Employee management
- HR operations (attendance, leaves)
- Payroll processing
- **Access**: `/api/v1/company/*`, `/api/v1/hr/*`, `/api/v1/payroll/*`

#### Employee
- View own profile
- View own attendance
- Request and view own leaves
- View own payroll records
- **Access**: `/api/v1/hr/leaves` (own), `/api/v1/payroll/employees/{employee_id}/payroll`

### 3. HR Modules
- **Employee Management**: Complete employee lifecycle
- **Department Management**: Organizational structure
- **Position Management**: Job definitions
- **Attendance Tracking**: Daily attendance monitoring
- **Leave Management**: Request and approval workflow
- **Salary Management**: Configure salaries, allowances, deductions

### 4. Payroll Processing
- **Payroll Cycles**: Define payroll periods
- **Automatic Calculation**: Calculate salaries for all employees
- **Processing Workflow**: Draft → Processing → Processed → Paid
- **Finalization**: Mark payroll as paid

### 5. Dashboard Statistics
- Total and active employees
- Department count
- Payroll totals
- Pending leaves
- Daily attendance summary

## 📡 API Endpoints

### Authentication (`/api/v1/auth`)
- `POST /api/v1/auth/admin/register` - Register admin
- `POST /api/v1/auth/admin/login` - Admin login
- `POST /api/v1/auth/login` - Employee login
- `GET /api/v1/auth/me` - Get current user

### Admin Management (`/api/v1/admin`)
- `GET /api/v1/admin/admins` - List admins
- `POST /api/v1/admin/admins` - Create admin
- `PUT /api/v1/admin/admins/{id}` - Update admin
- `DELETE /api/v1/admin/admins/{id}` - Delete admin
- `GET /api/v1/admin/companies` - List companies
- `POST /api/v1/admin/companies` - Create company

### Company Management (`/api/v1/company`)
- `GET /api/v1/company/employees` - List employees
- `POST /api/v1/company/employees` - Create employee
- `GET /api/v1/company/departments` - List departments
- `POST /api/v1/company/departments` - Create department
- `GET /api/v1/company/departments/{id}/positions` - List positions
- `POST /api/v1/company/departments/{id}/positions` - Create position
- `GET /api/v1/company/dashboard/stats` - Dashboard stats

### HR Module (`/api/v1/hr`)
#### Attendance
- `GET /api/v1/hr/attendance/{id}` - Get attendance
- `GET /api/v1/hr/employees/{id}/attendance` - List employee attendance
- `POST /api/v1/hr/attendance` - Create attendance

#### Leave
- `GET /api/v1/hr/leaves/{id}` - Get leave
- `GET /api/v1/hr/employees/{id}/leaves` - List employee leaves
- `GET /api/v1/hr/leaves/pending` - List pending leaves
- `POST /api/v1/hr/leaves` - Create leave request
- `PUT /api/v1/hr/leaves/{id}` - Approve/reject leave

#### Salary
- `GET /api/v1/hr/salaries/{id}` - Get salary
- `GET /api/v1/hr/employees/{id}/salary` - Get employee salary
- `POST /api/v1/hr/salaries` - Create salary
- `PUT /api/v1/hr/salaries/{id}` - Update salary

### Payroll Module (`/api/v1/payroll`)
- `GET /api/v1/payroll/cycles` - List payroll cycles
- `POST /api/v1/payroll/cycles` - Create payroll cycle
- `POST /api/v1/payroll/cycles/{id}/process` - Process payroll
- `POST /api/v1/payroll/cycles/{id}/finalize` - Finalize payroll
- `GET /api/v1/payroll/cycles/{id}/items` - List payroll items
- `GET /api/v1/payroll/employees/{id}/payroll` - List employee payroll

**Total: 50+ API endpoints**

## 🔧 Configuration

Environment variables in `.env`:

```bash
# App Configuration
APP_NAME=HR & Payroll SaaS API
APP_VERSION=1.0.0
API_V1_PREFIX=/api/v1

# Database
DATABASE_URL=sqlite:///./hr_payroll.db

# Security (CHANGE THESE IN PRODUCTION!)
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# CORS (Comma-separated list)
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000
```

## 📝 Example Usage

### 1. Login as Admin
```bash
curl -X POST "http://localhost:8000/api/v1/auth/admin/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@hrpayroll.com&password=admin123"
```

### 2. Create a Company
```bash
curl -X POST "http://localhost:8000/api/v1/admin/companies" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Corporation",
    "business_email": "contact@acme.com",
    "owner_email": "owner@acme.com",
    "owner_password": "owner123",
    "owner_full_name": "John Owner"
  }'
```

### 3. Login as Company Owner
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=owner@acme.com&password=owner123"
```

### 4. Create an Employee
```bash
curl -X POST "http://localhost:8000/api/v1/company/employees" \
  -H "Authorization: Bearer <owner_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane@acme.com",
    "password": "jane123",
    "full_name": "Jane Doe",
    "employee_id": "EMP001",
    "role": "employee",
    "hire_date": "2024-01-01"
  }'
```

### 5. Create Payroll Cycle
```bash
curl -X POST "http://localhost:8000/api/v1/payroll/cycles" \
  -H "Authorization: Bearer <owner_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "January 2024",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "payment_date": "2024-01-31"
  }'
```

### 6. Process Payroll
```bash
curl -X POST "http://localhost:8000/api/v1/payroll/cycles/{cycle_id}/process" \
  -H "Authorization: Bearer <owner_token>"
```

## 🗄️ Database Models

### Core Models
- `Admin` - System administrators
- `Company` - Tenant companies
- `Employee` - Company employees (all roles)

### Organizational Models
- `Department` - Company departments
- `Position` - Job positions

### HR Models
- `Salary` - Employee salary details
- `Attendance` - Daily attendance records
- `Leave` - Leave requests

### Payroll Models
- `PayrollCycle` - Payroll period management
- `PayrollItem` - Individual payroll records

## 🛠️ Manual Setup

If you prefer to start everything manually:

### 1. Install Dependencies (if not already done)
```bash
cd /home/z/my-project/hr-payroll-backend
python3 -m venv venv
source venv/bin/activate  # or: ./venv/bin/pip install
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
./venv/bin/python3 init_db.py
```

### 3. Start Server
```bash
./venv/bin/python3 -m uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload
```

## 📋 Logs

Server logs are saved to:
- **Production logs**: `/tmp/hr-api.log`

View logs in real-time:
```bash
tail -f /tmp/hr-api.log
```

## 🔒 Security Notes

⚠️ **Before deploying to production:**

1. **Change default passwords**
   - Admin password: `admin123`

2. **Set strong JWT secret**
   - Update `SECRET_KEY` in `.env`

3. **Use production database**
   - Switch from SQLite to PostgreSQL/MySQL
   - Update `DATABASE_URL` in `.env`

4. **Enable HTTPS**
   - Use reverse proxy (nginx/Apache)
   - Configure SSL certificates

5. **Set proper CORS origins**
   - Update `ALLOWED_ORIGINS` in `.env`

6. **Implement rate limiting**
   - Add API rate limiting middleware

7. **Add comprehensive logging**
   - Implement structured logging
   - Set up log rotation

## 🚀 Deployment

For production deployment:

1. **Use production-grade database** (PostgreSQL recommended)
2. **Use Gunicorn with Uvicorn workers**
3. **Set up reverse proxy** (nginx)
4. **Configure SSL/TLS**
5. **Set up monitoring** (Prometheus/Grafana)
6. **Implement CI/CD pipeline**
7. **Use environment variables** for secrets
8. **Set up backups** (database and logs)

Example Gunicorn command:
```bash
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile /var/log/hr-api/access.log \
  --error-logfile /var/log/hr-api/error.log
```

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port 8000 is already in use
lsof -i :8000

# Kill existing process
./stop.sh
```

### Database errors
```bash
# Recreate database
rm hr_payroll.db
./venv/bin/python3 init_db.py
```

### Import errors
```bash
# Reinstall dependencies
rm -rf venv
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

## 📚 Technology Stack

- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn
- **ORM**: SQLAlchemy 2.0.23
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Bcrypt
- **Validation**: Pydantic 2.5.0
- **Settings**: Pydantic Settings

## 📄️ License

This project is provided as-is for educational and commercial use.

## 📞 Support

For detailed API documentation, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

**Built with ❤️ using FastAPI**

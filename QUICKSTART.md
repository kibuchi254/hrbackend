# Quick Start Guide

This guide will help you get the HR & Payroll SaaS API up and running in minutes.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps

### 1. Navigate to the project directory
```bash
cd hr-payroll-backend
```

### 2. Create a virtual environment
```bash
# On Linux/Mac
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize the database
```bash
python init_db.py
```

This will create a default admin user:
- **Email**: admin@hrpayroll.com
- **Password**: admin123

⚠️ **IMPORTANT**: Change this password in production!

### 5. Start the server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be running at `http://localhost:8000`

## Test the API

### 1. Check API Documentation
Open your browser and visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 2. Test Health Endpoint
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy"
}
```

### 3. Login as Admin
```bash
curl -X POST "http://localhost:8000/api/v1/auth/admin/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@hrpayroll.com&password=admin123"
```

Copy the `access_token` from the response.

### 4. Create a Company
```bash
curl -X POST "http://localhost:8000/api/v1/admin/companies" \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Company",
    "business_email": "contact@mycompany.com",
    "owner_email": "owner@mycompany.com",
    "owner_password": "owner123",
    "owner_full_name": "John Owner"
  }'
```

### 5. Login as Company Owner
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=owner@mycompany.com&password=owner123"
```

### 6. Create an Employee
```bash
curl -X POST "http://localhost:8000/api/v1/company/employees" \
  -H "Authorization: Bearer <OWNER_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane@mycompany.com",
    "password": "jane123",
    "full_name": "Jane Doe",
    "employee_id": "EMP001",
    "role": "employee",
    "hire_date": "2024-01-01"
  }'
```

## Common Use Cases

### View Dashboard Stats
```bash
curl -X GET "http://localhost:8000/api/v1/company/dashboard/stats" \
  -H "Authorization: Bearer <OWNER_ACCESS_TOKEN>"
```

### Create a Department
```bash
curl -X POST "http://localhost:8000/api/v1/company/departments" \
  -H "Authorization: Bearer <OWNER_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Engineering",
    "description": "Software development team"
  }'
```

### Create Employee Salary
```bash
curl -X POST "http://localhost:8000/api/v1/hr/salaries" \
  -H "Authorization: Bearer <OWNER_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 1,
    "base_salary": 5000.00,
    "housing_allowance": 500.00,
    "transport_allowance": 200.00,
    "medical_allowance": 300.00,
    "tax_deduction": 500.00,
    "insurance_deduction": 100.00
  }'
```

### Create Payroll Cycle
```bash
curl -X POST "http://localhost:8000/api/v1/payroll/cycles" \
  -H "Authorization: Bearer <OWNER_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "January 2024",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "payment_date": "2024-01-31"
  }'
```

### Process Payroll
```bash
curl -X POST "http://localhost:8000/api/v1/payroll/cycles/{CYCLE_ID}/process" \
  -H "Authorization: Bearer <OWNER_ACCESS_TOKEN>"
```

## API Structure

### Authentication
- `/api/v1/auth/admin/register` - Register admin
- `/api/v1/auth/admin/login` - Admin login
- `/api/v1/auth/login` - Employee login
- `/api/v1/auth/me` - Get current user

### Admin (Super Admin Only)
- `/api/v1/admin/admins/*` - Manage admins
- `/api/v1/admin/companies/*` - Manage companies

### Company (Company Owner/Admin)
- `/api/v1/company/employees/*` - Manage employees
- `/api/v1/company/departments/*` - Manage departments
- `/api/v1/company/departments/{id}/positions` - Manage positions
- `/api/v1/company/dashboard/stats` - Dashboard statistics

### HR (All company roles)
- `/api/v1/hr/attendance/*` - Manage attendance
- `/api/v1/hr/leaves/*` - Manage leaves
- `/api/v1/hr/salaries/*` - Manage salaries

### Payroll (Company Owner/Admin)
- `/api/v1/payroll/cycles/*` - Manage payroll cycles
- `/api/v1/payroll/cycles/{id}/process` - Process payroll
- `/api/v1/payroll/cycles/{id}/finalize` - Finalize payroll
- `/api/v1/payroll/items/*` - Manage payroll items

## User Roles Explained

### Admin
- System administrator
- Can create and manage companies
- Can create and manage other admins

### Company Owner
- Highest authority in a company
- Full access to all company features
- Can manage employees, departments, payroll

### Company Admin
- Management role in a company
- Can manage employees and HR functions
- Can process payroll

### Employee
- Regular staff member
- Can view own data
- Can request leaves
- Can view own attendance and payroll

## Troubleshooting

### Database Lock Error
If you see a database lock error, stop the server and delete the database file:
```bash
rm hr_payroll.db
python init_db.py
```

### Import Errors
Make sure you're running commands from the project directory with the virtual environment activated.

### CORS Errors
Check your `ALLOWED_ORIGINS` in `.env` file matches your frontend URL.

## Next Steps

1. **Customize Configuration**: Edit `app/core/config.py` to match your needs
2. **Set Environment Variables**: Copy `.env.example` to `.env` and customize
3. **Add Features**: Extend the API with additional endpoints as needed
4. **Deploy**: Deploy to a production server with proper database and security settings

## Support

For detailed documentation, see the main `README.md` file.

## Security Reminders

⚠️ **Before deploying to production:**

1. Change the default admin password
2. Set a strong JWT secret key
3. Use a production database (PostgreSQL/MySQL)
4. Enable HTTPS
5. Set proper CORS origins
6. Implement rate limiting
7. Add comprehensive logging

Happy coding! 🚀

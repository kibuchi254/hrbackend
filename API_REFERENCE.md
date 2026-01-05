# API Endpoints Reference

Complete list of all API endpoints for the HR & Payroll SaaS system.

## Base URL
```
http://localhost:8000
```

## Table of Contents
- [Authentication](#authentication)
- [Admin Management](#admin-management)
- [Company Management](#company-management)
- [HR Module](#hr-module)
- [Payroll Module](#payroll-module)

---

## Authentication

All authentication endpoints are public (no authentication required).

### Register Admin
```http
POST /api/v1/auth/admin/register
```
**Body:**
```json
{
  "email": "admin@example.com",
  "password": "securePassword123",
  "full_name": "John Admin"
}
```

### Admin Login
```http
POST /api/v1/auth/admin/login
```
**Content-Type:** `application/x-www-form-urlencoded`  
**Body:**
```
username=admin@example.com&password=securePassword123
```

### Employee Login (All Roles)
```http
POST /api/v1/auth/login
```
**Content-Type:** `application/x-www-form-urlencoded`  
**Body:**
```
username=user@company.com&password=userPassword123
```

### Get Current User Info
```http
GET /api/v1/auth/me
```
**Headers:**
```
Authorization: Bearer <jwt_token>
```

---

## Admin Management

All admin endpoints require authentication with Admin role.

### List All Admins
```http
GET /api/v1/admin/admins?skip=0&limit=100
```

### Create Admin
```http
POST /api/v1/admin/admins
```
**Body:**
```json
{
  "email": "newadmin@example.com",
  "password": "adminPassword123",
  "full_name": "New Admin"
}
```

### Get Admin by ID
```http
GET /api/v1/admin/admins/{admin_id}
```

### Update Admin
```http
PUT /api/v1/admin/admins/{admin_id}
```
**Body:**
```json
{
  "full_name": "Updated Name",
  "is_active": true
}
```

### Delete Admin
```http
DELETE /api/v1/admin/admins/{admin_id}
```

### List All Companies
```http
GET /api/v1/admin/companies?skip=0&limit=100
```

### Create Company
```http
POST /api/v1/admin/companies
```
**Body:**
```json
{
  "name": "Company Name",
  "business_email": "contact@company.com",
  "phone": "+1234567890",
  "address": "123 Business St",
  "owner_email": "owner@company.com",
  "owner_password": "ownerPassword123",
  "owner_full_name": "Owner Name"
}
```

### Get Company by ID
```http
GET /api/v1/admin/companies/{company_id}
```

### Update Company
```http
PUT /api/v1/admin/companies/{company_id}
```
**Body:**
```json
{
  "name": "Updated Company Name",
  "phone": "+0987654321",
  "subscription_tier": "pro"
}
```

### Delete Company
```http
DELETE /api/v1/admin/companies/{company_id}
```

---

## Company Management

These endpoints require authentication with Company Owner or Company Admin role.

### Employee Management

#### List Company Employees
```http
GET /api/v1/company/employees?skip=0&limit=100
```

#### Create Employee
```http
POST /api/v1/company/employees
```
**Body:**
```json
{
  "email": "jane@company.com",
  "password": "employeePassword123",
  "full_name": "Jane Doe",
  "employee_id": "EMP001",
  "role": "employee",
  "department_id": 1,
  "position_id": 1,
  "phone": "+1234567890",
  "address": "123 Main St",
  "hire_date": "2024-01-01"
}
```
**Roles:** `admin`, `company_owner`, `company_admin`, `employee`

#### Get Employee by ID
```http
GET /api/v1/company/employees/{employee_id}
```

#### Update Employee
```http
PUT /api/v1/company/employees/{employee_id}
```
**Body:**
```json
{
  "full_name": "Jane Smith",
  "department_id": 2,
  "status": "active"
}
```

#### Delete Employee
```http
DELETE /api/v1/company/employees/{employee_id}
```

### Department Management

#### List Departments
```http
GET /api/v1/company/departments?skip=0&limit=100
```

#### Create Department
```http
POST /api/v1/company/departments
```
**Body:**
```json
{
  "name": "Engineering",
  "description": "Software Development Team",
  "manager_id": 5
}
```

#### Get Department by ID
```http
GET /api/v1/company/departments/{department_id}
```

#### Update Department
```http
PUT /api/v1/company/departments/{department_id}
```
**Body:**
```json
{
  "name": "Updated Name",
  "manager_id": 10
}
```

#### Delete Department
```http
DELETE /api/v1/company/departments/{department_id}
```

### Position Management

#### List Positions in Department
```http
GET /api/v1/company/departments/{department_id}/positions?skip=0&limit=100
```

#### Create Position
```http
POST /api/v1/company/departments/{department_id}/positions
```
**Body:**
```json
{
  "title": "Senior Developer",
  "description": "Senior software engineer position",
  "base_salary": 5000.00
}
```

#### Update Position
```http
PUT /api/v1/company/positions/{position_id}
```
**Body:**
```json
{
  "title": "Lead Developer",
  "base_salary": 6000.00
}
```

#### Delete Position
```http
DELETE /api/v1/company/positions/{position_id}
```

### Dashboard

#### Get Dashboard Statistics
```http
GET /api/v1/company/dashboard/stats
```
**Response:**
```json
{
  "total_employees": 50,
  "active_employees": 45,
  "total_departments": 5,
  "total_payroll_this_month": 250000.00,
  "pending_leaves": 3,
  "present_today": 40,
  "absent_today": 5
}
```

---

## HR Module

### Attendance Management

#### Get Attendance Record
```http
GET /api/v1/hr/attendance/{attendance_id}
```

#### List Employee Attendance
```http
GET /api/v1/hr/employees/{employee_id}/attendance?skip=0&limit=100
```

#### List Attendance by Date
```http
GET /api/v1/hr/attendance/date/{date}
```
**Date format:** `YYYY-MM-DD`

#### Create Attendance
```http
POST /api/v1/hr/attendance
```
**Body:**
```json
{
  "employee_id": 5,
  "date": "2024-01-15",
  "check_in_time": "2024-01-15T09:00:00",
  "check_out_time": "2024-01-15T18:00:00",
  "status": "present",
  "notes": "Normal working day"
}
```
**Status options:** `present`, `absent`, `late`, `half_day`, `leave`

#### Update Attendance
```http
PUT /api/v1/hr/attendance/{attendance_id}
```
**Body:**
```json
{
  "check_out_time": "2024-01-15T18:30:00",
  "status": "present"
}
```

#### Delete Attendance
```http
DELETE /api/v1/hr/attendance/{attendance_id}
```

### Leave Management

#### Get Leave Request
```http
GET /api/v1/hr/leaves/{leave_id}
```

#### List Employee Leaves
```http
GET /api/v1/hr/employees/{employee_id}/leaves?skip=0&limit=100
```

#### List Pending Leaves
```http
GET /api/v1/hr/leaves/pending?skip=0&limit=100
```

#### List Company Leaves
```http
GET /api/v1/hr/leaves?skip=0&limit=100
```

#### Create Leave Request
```http
POST /api/v1/hr/leaves
```
**Body:**
```json
{
  "leave_type": "annual",
  "start_date": "2024-02-01",
  "end_date": "2024-02-05",
  "reason": "Family vacation"
}
```
**Leave types:** `annual`, `sick`, `maternity`, `paternity`, `unpaid`, etc.

#### Update Leave (Approve/Reject)
```http
PUT /api/v1/hr/leaves/{leave_id}
```
**Body:**
```json
{
  "status": "approved",
  "rejection_reason": ""
}
```
**Status options:** `pending`, `approved`, `rejected`, `cancelled`

#### Delete Leave
```http
DELETE /api/v1/hr/leaves/{leave_id}
```

### Salary Management

#### Get Salary Record
```http
GET /api/v1/hr/salaries/{salary_id}
```

#### Get Employee Salary
```http
GET /api/v1/hr/employees/{employee_id}/salary
```

#### Create Salary
```http
POST /api/v1/hr/salaries
```
**Body:**
```json
{
  "employee_id": 5,
  "base_salary": 5000.00,
  "housing_allowance": 500.00,
  "transport_allowance": 200.00,
  "medical_allowance": 300.00,
  "other_allowances": 0.00,
  "tax_deduction": 500.00,
  "insurance_deduction": 100.00,
  "other_deductions": 0.00,
  "effective_date": "2024-01-01"
}
```

#### Update Salary
```http
PUT /api/v1/hr/salaries/{salary_id}
```
**Body:**
```json
{
  "base_salary": 5500.00,
  "housing_allowance": 600.00
}
```

#### Delete Salary
```http
DELETE /api/v1/hr/salaries/{salary_id}
```

---

## Payroll Module

### Payroll Cycle Management

#### List Payroll Cycles
```http
GET /api/v1/payroll/cycles?skip=0&limit=100
```

#### Create Payroll Cycle
```http
POST /api/v1/payroll/cycles
```
**Body:**
```json
{
  "name": "January 2024",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "payment_date": "2024-01-31"
}
```

#### Get Payroll Cycle
```http
GET /api/v1/payroll/cycles/{cycle_id}
```

#### Update Payroll Cycle
```http
PUT /api/v1/payroll/cycles/{cycle_id}
```
**Body:**
```json
{
  "name": "January 2024 (Revised)",
  "payment_date": "2024-02-01"
}
```

#### Delete Payroll Cycle
```http
DELETE /api/v1/payroll/cycles/{cycle_id}
```

#### Process Payroll Cycle
```http
POST /api/v1/payroll/cycles/{cycle_id}/process
```
**Description:** Automatically calculates salaries for all active employees based on their salary configurations.

#### Finalize Payroll Cycle
```http
POST /api/v1/payroll/cycles/{cycle_id}/finalize
```
**Description:** Marks the payroll cycle as paid and updates payment dates.

### Payroll Item Management

#### List Payroll Items in Cycle
```http
GET /api/v1/payroll/cycles/{cycle_id}/items?skip=0&limit=100
```

#### List Employee Payroll
```http
GET /api/v1/payroll/employees/{employee_id}/payroll?skip=0&limit=100
```

#### Get Payroll Item
```http
GET /api/v1/payroll/items/{item_id}
```

#### Create Payroll Item
```http
POST /api/v1/payroll/cycles/{cycle_id}/items
```
**Body:**
```json
{
  "employee_id": 5,
  "base_salary": 5000.00,
  "gross_salary": 6000.00,
  "total_deductions": 600.00,
  "net_salary": 5400.00,
  "payment_method": "bank_transfer",
  "payment_reference": "TXN123456"
}
```

#### Update Payroll Item
```http
PUT /api/v1/payroll/items/{item_id}
```
**Body:**
```json
{
  "net_salary": 5500.00,
  "payment_reference": "TXN789012"
}
```

#### Delete Payroll Item
```http
DELETE /api/v1/payroll/items/{item_id}
```

---

## Common Response Formats

### Success Response
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Error Response
```json
{
  "detail": "Error message describing what went wrong"
}
```

### Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Authentication Headers

All protected endpoints require:

```
Authorization: Bearer <your_jwt_token>
```

Replace `<your_jwt_token>` with the token received from login endpoint.

---

## Pagination

List endpoints support pagination:

```
?skip=0&limit=100
```

- `skip`: Number of items to skip (default: 0)
- `limit`: Number of items to return (default: 100)

---

## Payroll Status Flow

Payroll cycles follow this status flow:

```
draft → processing → processed → paid
```

- **draft**: Initial state, can be edited
- **processing**: Currently being processed
- **processed**: Calculations complete, ready for review
- **paid**: Finalized and payments recorded

---

## Leave Status Flow

Leave requests follow this status flow:

```
pending → approved
         → rejected
         → cancelled
```

---

## Common HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or failed
- `403 Forbidden`: User doesn't have permission
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error

---

## Notes

1. All dates should be in `YYYY-MM-DD` format
2. All date-time should be in ISO 8601 format: `YYYY-MM-DDTHH:MM:SS`
3. All monetary values should be decimal numbers with 2 decimal places
4. All email addresses must be unique per role
5. Employee IDs must be unique within a company

---

For more detailed examples and workflows, see:
- [README.md](README.md) - Full documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Project overview

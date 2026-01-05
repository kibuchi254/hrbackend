from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.core.database import get_db
from app.core.deps import get_current_user, verify_company_access, get_current_company_admin, get_current_employee
from app.crud.crud_hr import (
    get_attendance, create_attendance, update_attendance, delete_attendance,
    get_attendance_by_employee_and_date, get_attendance_by_company_and_date, get_attendance_by_employee,
    get_leave, create_leave, update_leave, delete_leave, get_leaves_by_employee,
    get_leaves_by_company, get_pending_leaves_by_company
)
from app.crud.crud_hr import (
    get_salary, create_salary, update_salary, delete_salary, get_salary_by_employee
)
from app.schemas.schemas import (
    AttendanceCreate, AttendanceUpdate, AttendanceResponse,
    LeaveCreate, LeaveUpdate, LeaveResponse,
    SalaryCreate, SalaryUpdate, SalaryResponse
)

router = APIRouter()


# ========== Attendance Management ==========
@router.get("/attendance/{attendance_id}", response_model=AttendanceResponse)
async def get_attendance_endpoint(
    attendance_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get attendance by ID"""
    attendance = get_attendance(db, attendance_id)
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )

    # Verify access
    from app.crud.crud_employee import get_employee
    employee = get_employee(db, attendance.employee_id)
    if current_user["role"] != "admin" and employee.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return attendance


@router.get("/employees/{employee_id}/attendance", response_model=List[AttendanceResponse])
async def list_employee_attendance(
    employee_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List attendance for an employee"""
    from app.crud.crud_employee import get_employee

    employee = get_employee(db, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    # Verify access
    if current_user["role"] == "employee" and current_user["user"].id != employee_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    if current_user["role"] in ["company_owner", "company_admin"] and employee.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return get_attendance_by_employee(db, employee_id=employee_id, skip=skip, limit=limit)


@router.get("/attendance/date/{date}", response_model=List[AttendanceResponse])
async def list_attendance_by_date(
    date: date,
    current_user: dict = Depends(verify_company_access),
    db: Session = Depends(get_db)
):
    """List all attendance records for a specific date"""
    company_id = current_user["company_id"]
    return get_attendance_by_company_and_date(db, company_id=company_id, date=date)


@router.post("/attendance", response_model=AttendanceResponse)
async def create_new_attendance(
    attendance: AttendanceCreate,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Create attendance record (company admin only)"""
    # Validate employee belongs to company
    from app.crud.crud_employee import get_employee
    employee = get_employee(db, attendance.employee_id)
    if not employee or employee.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid employee"
        )

    # Check if attendance already exists
    existing = get_attendance_by_employee_and_date(db, attendance.employee_id, attendance.date)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance record already exists for this date"
        )

    return create_attendance(db=db, attendance=attendance)


@router.put("/attendance/{attendance_id}", response_model=AttendanceResponse)
async def update_attendance_endpoint(
    attendance_id: int,
    attendance: AttendanceUpdate,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Update attendance record"""
    db_attendance = get_attendance(db, attendance_id)
    if not db_attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )

    # Verify employee belongs to company
    from app.crud.crud_employee import get_employee
    employee = get_employee(db, db_attendance.employee_id)
    if employee.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    updated_attendance = update_attendance(db, attendance_id, attendance)
    return updated_attendance


@router.delete("/attendance/{attendance_id}")
async def delete_attendance_endpoint(
    attendance_id: int,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Delete attendance record"""
    db_attendance = get_attendance(db, attendance_id)
    if not db_attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )

    # Verify employee belongs to company
    from app.crud.crud_employee import get_employee
    employee = get_employee(db, db_attendance.employee_id)
    if employee.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    success = delete_attendance(db, attendance_id)
    return {"message": "Attendance record deleted successfully"}


# ========== Leave Management ==========
@router.get("/leaves/{leave_id}", response_model=LeaveResponse)
async def get_leave_endpoint(
    leave_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get leave by ID"""
    leave = get_leave(db, leave_id)
    if not leave:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave not found"
        )

    # Verify access
    from app.crud.crud_employee import get_employee
    employee = get_employee(db, leave.employee_id)
    if current_user["role"] != "admin" and employee.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return leave


@router.get("/employees/{employee_id}/leaves", response_model=List[LeaveResponse])
async def list_employee_leaves(
    employee_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List leaves for an employee"""
    from app.crud.crud_employee import get_employee

    employee = get_employee(db, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    # Verify access
    if current_user["role"] == "employee" and current_user["user"].id != employee_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    if current_user["role"] in ["company_owner", "company_admin"] and employee.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return get_leaves_by_employee(db, employee_id=employee_id, skip=skip, limit=limit)


@router.get("/leaves/pending", response_model=List[LeaveResponse])
async def list_pending_leaves(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(verify_company_access),
    db: Session = Depends(get_db)
):
    """List all pending leaves in the company"""
    company_id = current_user["company_id"]
    return get_pending_leaves_by_company(db, company_id)


@router.get("/leaves", response_model=List[LeaveResponse])
async def list_company_leaves(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(verify_company_access),
    db: Session = Depends(get_db)
):
    """List all leaves in the company"""
    company_id = current_user["company_id"]
    return get_leaves_by_company(db, company_id, skip=skip, limit=limit)


@router.post("/leaves", response_model=LeaveResponse)
async def create_new_leave(
    leave: LeaveCreate,
    current_user: dict = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Create leave request"""
    employee_id = leave.employee_id or current_user["user"].id

    # Validate employee
    from app.crud.crud_employee import get_employee
    employee = get_employee(db, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    # Employees can only create leave for themselves
    if current_user["role"] == "employee" and current_user["user"].id != employee_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return create_leave(db=db, leave=leave, employee_id=employee_id)


@router.put("/leaves/{leave_id}", response_model=LeaveResponse)
async def update_leave_endpoint(
    leave_id: int,
    leave: LeaveUpdate,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Update leave (approve/reject)"""
    db_leave = get_leave(db, leave_id)
    if not db_leave:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave not found"
        )

    # Verify employee belongs to company
    from app.crud.crud_employee import get_employee
    employee = get_employee(db, db_leave.employee_id)
    if employee.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    updated_leave = update_leave(db, leave_id, leave, approved_by=current_user["user"].id)
    return updated_leave


@router.delete("/leaves/{leave_id}")
async def delete_leave_endpoint(
    leave_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete leave"""
    db_leave = get_leave(db, leave_id)
    if not db_leave:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave not found"
        )

    # Verify access
    from app.crud.crud_employee import get_employee
    employee = get_employee(db, db_leave.employee_id)
    if current_user["role"] == "employee" and current_user["user"].id != db_leave.employee_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    if current_user["role"] in ["company_owner", "company_admin"] and employee.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    success = delete_leave(db, leave_id)
    return {"message": "Leave deleted successfully"}


# ========== Salary Management ==========
@router.get("/salaries/{salary_id}", response_model=SalaryResponse)
async def get_salary_endpoint(
    salary_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get salary by ID"""
    salary = get_salary(db, salary_id)
    if not salary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salary not found"
        )

    # Verify access
    from app.crud.crud_employee import get_employee
    employee = get_employee(db, salary.employee_id)
    if current_user["role"] == "employee" and current_user["user"].id != salary.employee_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    if current_user["role"] in ["company_owner", "company_admin"] and employee.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return salary


@router.get("/employees/{employee_id}/salary", response_model=SalaryResponse)
async def get_employee_salary(
    employee_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get salary for an employee"""
    from app.crud.crud_employee import get_employee

    employee = get_employee(db, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    # Verify access
    if current_user["role"] == "employee" and current_user["user"].id != employee_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    if current_user["role"] in ["company_owner", "company_admin"] and employee.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    salary = get_salary_by_employee(db, employee_id)
    if not salary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salary not found"
        )

    return salary


@router.post("/salaries", response_model=SalaryResponse)
async def create_new_salary(
    salary: SalaryCreate,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Create salary record"""
    # Validate employee belongs to company
    from app.crud.crud_employee import get_employee
    employee = get_employee(db, salary.employee_id)
    if not employee or employee.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid employee"
        )

    # Check if salary already exists
    existing = get_salary_by_employee(db, salary.employee_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Salary already exists for this employee"
        )

    return create_salary(db=db, salary=salary)


@router.put("/salaries/{salary_id}", response_model=SalaryResponse)
async def update_salary_endpoint(
    salary_id: int,
    salary: SalaryUpdate,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Update salary record"""
    db_salary = get_salary(db, salary_id)
    if not db_salary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salary not found"
        )

    # Verify employee belongs to company
    from app.crud.crud_employee import get_employee
    employee = get_employee(db, db_salary.employee_id)
    if employee.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    updated_salary = update_salary(db, salary_id, salary)
    return updated_salary


@router.delete("/salaries/{salary_id}")
async def delete_salary_endpoint(
    salary_id: int,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Delete salary record"""
    db_salary = get_salary(db, salary_id)
    if not db_salary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salary not found"
        )

    # Verify employee belongs to company
    from app.crud.crud_employee import get_employee
    employee = get_employee(db, db_salary.employee_id)
    if employee.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    success = delete_salary(db, salary_id)
    return {"message": "Salary deleted successfully"}

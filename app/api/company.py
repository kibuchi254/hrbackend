from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.deps import get_current_user, verify_company_access, get_current_company_admin
from app.crud.crud_employee import (
    get_employees_by_company, create_employee, update_employee, delete_employee,
    get_employee as get_employee_crud, get_employee_by_email
)
from app.crud.crud_department import (
    get_departments_by_company, create_department, update_department, delete_department,
    get_department as get_department_crud
)
from app.crud.crud_department import (
    get_positions_by_department, create_position, update_position, delete_position,
    get_position as get_position_crud
)
from app.schemas.schemas import (
    EmployeeCreate, EmployeeUpdate, EmployeeResponse,
    DepartmentCreate, DepartmentUpdate, DepartmentResponse,
    PositionCreate, PositionUpdate, PositionResponse, DashboardStats
)

router = APIRouter()


# ========== Employee Management ==========
@router.get("/employees", response_model=List[EmployeeResponse])
async def list_employees(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(verify_company_access),
    db: Session = Depends(get_db)
):
    """List all employees in the company"""
    company_id = current_user["company_id"]
    return get_employees_by_company(db, company_id=company_id, skip=skip, limit=limit)


@router.post("/employees", response_model=EmployeeResponse)
async def create_new_employee(
    employee: EmployeeCreate,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Create a new employee (company owner/admin only)"""
    company_id = current_user["company_id"]

    # Check if email already exists
    db_employee = get_employee_by_email(db, email=employee.email)
    if db_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Validate department and position belong to the company
    if employee.department_id:
        dept = get_department_crud(db, employee.department_id)
        if not dept or dept.company_id != company_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid department"
            )

    return create_employee(db=db, employee=employee, company_id=company_id)


@router.get("/employees/{employee_id}", response_model=EmployeeResponse)
async def get_employee_endpoint(
    employee_id: int,
    current_user: dict = Depends(verify_company_access),
    db: Session = Depends(get_db)
):
    """Get employee by ID"""
    employee = get_employee_crud(db, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    # Verify employee belongs to the same company
    if current_user["role"] != "admin" and employee.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return employee


@router.put("/employees/{employee_id}", response_model=EmployeeResponse)
async def update_employee_endpoint(
    employee_id: int,
    employee: EmployeeUpdate,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Update employee"""
    db_employee = get_employee_crud(db, employee_id)
    if not db_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    if db_employee.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    updated_employee = update_employee(db, employee_id, employee)
    return updated_employee


@router.delete("/employees/{employee_id}")
async def delete_employee_endpoint(
    employee_id: int,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Delete employee"""
    db_employee = get_employee_crud(db, employee_id)
    if not db_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    if db_employee.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    success = delete_employee(db, employee_id)
    return {"message": "Employee deleted successfully"}


# ========== Department Management ==========
@router.get("/departments", response_model=List[DepartmentResponse])
async def list_departments(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(verify_company_access),
    db: Session = Depends(get_db)
):
    """List all departments in the company"""
    company_id = current_user["company_id"]
    return get_departments_by_company(db, company_id=company_id, skip=skip, limit=limit)


@router.post("/departments", response_model=DepartmentResponse)
async def create_new_department(
    department: DepartmentCreate,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Create a new department"""
    company_id = current_user["company_id"]

    # Validate manager if provided
    if department.manager_id:
        from app.crud.crud_employee import get_employee
        manager = get_employee(db, department.manager_id)
        if not manager or manager.company_id != company_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid manager"
            )

    return create_department(db=db, department=department, company_id=company_id)


@router.get("/departments/{department_id}", response_model=DepartmentResponse)
async def get_department_endpoint(
    department_id: int,
    current_user: dict = Depends(verify_company_access),
    db: Session = Depends(get_db)
):
    """Get department by ID"""
    department = get_department_crud(db, department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )

    if current_user["role"] != "admin" and department.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return department


@router.put("/departments/{department_id}", response_model=DepartmentResponse)
async def update_department_endpoint(
    department_id: int,
    department: DepartmentUpdate,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Update department"""
    db_department = get_department_crud(db, department_id)
    if not db_department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )

    if db_department.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    updated_department = update_department(db, department_id, department)
    return updated_department


@router.delete("/departments/{department_id}")
async def delete_department_endpoint(
    department_id: int,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Delete department"""
    db_department = get_department_crud(db, department_id)
    if not db_department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )

    if db_department.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    success = delete_department(db, department_id)
    return {"message": "Department deleted successfully"}


# ========== Position Management ==========
@router.get("/departments/{department_id}/positions", response_model=List[PositionResponse])
async def list_positions(
    department_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(verify_company_access),
    db: Session = Depends(get_db)
):
    """List all positions in a department"""
    return get_positions_by_department(db, department_id=department_id, skip=skip, limit=limit)


@router.post("/departments/{department_id}/positions", response_model=PositionResponse)
async def create_new_position(
    department_id: int,
    position: PositionCreate,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Create a new position"""
    # Validate department belongs to company
    department = get_department_crud(db, department_id)
    if not department or department.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid department"
        )

    return create_position(db=db, position=position, department_id=department_id)


@router.put("/positions/{position_id}", response_model=PositionResponse)
async def update_position_endpoint(
    position_id: int,
    position: PositionUpdate,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Update position"""
    db_position = get_position_crud(db, position_id)
    if not db_position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found"
        )

    # Verify position's department belongs to the company
    from app.crud.crud_department import get_department
    department = get_department(db, db_position.department_id)
    if department.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    updated_position = update_position(db, position_id, position)
    return updated_position


@router.delete("/positions/{position_id}")
async def delete_position_endpoint(
    position_id: int,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Delete position"""
    db_position = get_position_crud(db, position_id)
    if not db_position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found"
        )

    # Verify position's department belongs to the company
    from app.crud.crud_department import get_department
    department = get_department(db, db_position.department_id)
    if department.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    success = delete_position(db, position_id)
    return {"message": "Position deleted successfully"}


# ========== Dashboard Stats ==========
@router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: dict = Depends(verify_company_access),
    db: Session = Depends(get_db)
):
    """Get company dashboard statistics"""
    from app.models.models import Employee, Department, Leave, Attendance, PayrollCycle
    from sqlalchemy import func
    from datetime import date

    company_id = current_user["company_id"]

    # Count employees
    total_employees = db.query(Employee).filter(Employee.company_id == company_id).count()
    active_employees = db.query(Employee).filter(
        Employee.company_id == company_id, Employee.status == "active"
    ).count()

    # Count departments
    total_departments = db.query(Department).filter(Department.company_id == company_id).count()

    # Get current month payroll
    current_month = date.today().replace(day=1)
    payroll_cycle = db.query(PayrollCycle).filter(
        PayrollCycle.company_id == company_id,
        PayrollCycle.start_date >= current_month,
        PayrollCycle.status == "paid"
    ).first()

    total_payroll_this_month = payroll_cycle.total_amount if payroll_cycle else None

    # Count pending leaves
    pending_leaves = db.query(Leave).join(Employee).filter(
        Employee.company_id == company_id,
        Leave.status == "pending"
    ).count()

    # Get today's attendance
    today = date.today()
    present_today = db.query(Attendance).join(Employee).filter(
        Employee.company_id == company_id,
        Attendance.date == today,
        Attendance.status == "present"
    ).count()

    absent_today = db.query(Attendance).join(Employee).filter(
        Employee.company_id == company_id,
        Attendance.date == today,
        Attendance.status == "absent"
    ).count()

    return DashboardStats(
        total_employees=total_employees,
        active_employees=active_employees,
        total_departments=total_departments,
        total_payroll_this_month=total_payroll_this_month,
        pending_leaves=pending_leaves,
        present_today=present_today,
        absent_today=absent_today
    )

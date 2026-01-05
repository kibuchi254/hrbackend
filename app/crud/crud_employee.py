from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.models import Employee
from app.schemas.schemas import EmployeeCreate, EmployeeUpdate
from app.core.security import get_password_hash, verify_password


def get_employee(db: Session, employee_id: int) -> Optional[Employee]:
    return db.query(Employee).filter(Employee.id == employee_id).first()


def get_employee_by_email(db: Session, email: str) -> Optional[Employee]:
    return db.query(Employee).filter(Employee.email == email).first()


def get_employees_by_company(db: Session, company_id: int, skip: int = 0, limit: int = 100) -> List[Employee]:
    return db.query(Employee).filter(Employee.company_id == company_id).offset(skip).limit(limit).all()


def get_employees(db: Session, skip: int = 0, limit: int = 100) -> List[Employee]:
    return db.query(Employee).offset(skip).limit(limit).all()


def create_employee(db: Session, employee: EmployeeCreate, company_id: int) -> Employee:
    hashed_password = get_password_hash(employee.password)
    db_employee = Employee(
        email=employee.email,
        password_hash=hashed_password,
        full_name=employee.full_name,
        employee_id=employee.employee_id,
        role=employee.role,
        company_id=company_id,
        department_id=employee.department_id,
        position_id=employee.position_id,
        phone=employee.phone,
        address=employee.address,
        date_of_birth=employee.date_of_birth,
        hire_date=employee.hire_date
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def update_employee(db: Session, employee_id: int, employee: EmployeeUpdate) -> Optional[Employee]:
    db_employee = get_employee(db, employee_id)
    if db_employee:
        update_data = employee.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_employee, key, value)
        db.commit()
        db.refresh(db_employee)
    return db_employee


def delete_employee(db: Session, employee_id: int) -> bool:
    db_employee = get_employee(db, employee_id)
    if db_employee:
        db.delete(db_employee)
        db.commit()
        return True
    return False


def authenticate_employee(db: Session, email: str, password: str) -> Optional[Employee]:
    employee = get_employee_by_email(db, email)
    if not employee:
        return None
    if not verify_password(password, employee.password_hash):
        return None
    return employee

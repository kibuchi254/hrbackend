from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from datetime import date
from app.models.models import Salary, Attendance, Leave
from app.schemas.schemas import SalaryCreate, SalaryUpdate, AttendanceCreate, AttendanceUpdate, LeaveCreate, LeaveUpdate


# ========== Salary CRUD ==========
def get_salary(db: Session, salary_id: int) -> Optional[Salary]:
    return db.query(Salary).filter(Salary.id == salary_id).first()


def get_salary_by_employee(db: Session, employee_id: int) -> Optional[Salary]:
    return db.query(Salary).filter(Salary.employee_id == employee_id).first()


def create_salary(db: Session, salary: SalaryCreate) -> Salary:
    db_salary = Salary(
        employee_id=salary.employee_id,
        base_salary=salary.base_salary,
        housing_allowance=salary.housing_allowance,
        transport_allowance=salary.transport_allowance,
        medical_allowance=salary.medical_allowance,
        other_allowances=salary.other_allowances,
        tax_deduction=salary.tax_deduction,
        insurance_deduction=salary.insurance_deduction,
        other_deductions=salary.other_deductions,
        effective_date=salary.effective_date
    )
    db.add(db_salary)
    db.commit()
    db.refresh(db_salary)
    return db_salary


def update_salary(db: Session, salary_id: int, salary: SalaryUpdate) -> Optional[Salary]:
    db_salary = get_salary(db, salary_id)
    if db_salary:
        update_data = salary.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_salary, key, value)
        db.commit()
        db.refresh(db_salary)
    return db_salary


def delete_salary(db: Session, salary_id: int) -> bool:
    db_salary = get_salary(db, salary_id)
    if db_salary:
        db.delete(db_salary)
        db.commit()
        return True
    return False


# ========== Attendance CRUD ==========
def get_attendance(db: Session, attendance_id: int) -> Optional[Attendance]:
    return db.query(Attendance).filter(Attendance.id == attendance_id).first()


def get_attendance_by_employee_and_date(db: Session, employee_id: int, date: date) -> Optional[Attendance]:
    return db.query(Attendance).filter(
        and_(Attendance.employee_id == employee_id, Attendance.date == date)
    ).first()


def get_attendance_by_employee(db: Session, employee_id: int, skip: int = 0, limit: int = 100) -> List[Attendance]:
    return db.query(Attendance).filter(Attendance.employee_id == employee_id).offset(skip).limit(limit).all()


def get_attendance_by_company_and_date(db: Session, company_id: int, date: date) -> List[Attendance]:
    from app.models.models import Employee
    return db.query(Attendance).join(Employee).filter(
        and_(Employee.company_id == company_id, Attendance.date == date)
    ).all()


def create_attendance(db: Session, attendance: AttendanceCreate) -> Attendance:
    db_attendance = Attendance(
        employee_id=attendance.employee_id,
        date=attendance.date,
        check_in_time=attendance.check_in_time,
        check_out_time=attendance.check_out_time,
        status=attendance.status,
        notes=attendance.notes
    )
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance


def update_attendance(db: Session, attendance_id: int, attendance: AttendanceUpdate) -> Optional[Attendance]:
    db_attendance = get_attendance(db, attendance_id)
    if db_attendance:
        update_data = attendance.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_attendance, key, value)
        db.commit()
        db.refresh(db_attendance)
    return db_attendance


def delete_attendance(db: Session, attendance_id: int) -> bool:
    db_attendance = get_attendance(db, attendance_id)
    if db_attendance:
        db.delete(db_attendance)
        db.commit()
        return True
    return False


# ========== Leave CRUD ==========
def get_leave(db: Session, leave_id: int) -> Optional[Leave]:
    return db.query(Leave).filter(Leave.id == leave_id).first()


def get_leaves_by_employee(db: Session, employee_id: int, skip: int = 0, limit: int = 100) -> List[Leave]:
    return db.query(Leave).filter(Leave.employee_id == employee_id).offset(skip).limit(limit).all()


def get_leaves_by_company(db: Session, company_id: int, skip: int = 0, limit: int = 100) -> List[Leave]:
    from app.models.models import Employee
    return db.query(Leave).join(Employee).filter(Employee.company_id == company_id).offset(skip).limit(limit).all()


def get_pending_leaves_by_company(db: Session, company_id: int) -> List[Leave]:
    from app.models.models import Employee
    return db.query(Leave).join(Employee).filter(
        and_(Employee.company_id == company_id, Leave.status == "pending")
    ).all()


def create_leave(db: Session, leave: LeaveCreate, employee_id: int) -> Leave:
    from datetime import timedelta
    total_days = (leave.end_date - leave.start_date).days + 1

    db_leave = Leave(
        employee_id=employee_id,
        leave_type=leave.leave_type,
        start_date=leave.start_date,
        end_date=leave.end_date,
        total_days=total_days,
        reason=leave.reason,
        status="pending"
    )
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave


def update_leave(db: Session, leave_id: int, leave: LeaveUpdate, approved_by: Optional[int] = None) -> Optional[Leave]:
    from datetime import datetime
    db_leave = get_leave(db, leave_id)
    if db_leave:
        update_data = leave.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_leave, key, value)
        if approved_by and leave.status in ["approved", "rejected"]:
            db_leave.approved_by = approved_by
            db_leave.approved_at = datetime.utcnow()
        db.commit()
        db.refresh(db_leave)
    return db_leave


def delete_leave(db: Session, leave_id: int) -> bool:
    db_leave = get_leave(db, leave_id)
    if db_leave:
        db.delete(db_leave)
        db.commit()
        return True
    return False

from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from datetime import date
from decimal import Decimal
from app.models.models import PayrollCycle, PayrollItem, Employee, Salary
from app.schemas.schemas import PayrollCycleCreate, PayrollCycleUpdate, PayrollItemCreate, PayrollItemUpdate


# ========== Payroll Cycle CRUD ==========
def get_payroll_cycle(db: Session, cycle_id: int) -> Optional[PayrollCycle]:
    return db.query(PayrollCycle).filter(PayrollCycle.id == cycle_id).first()


def get_payroll_cycles_by_company(db: Session, company_id: int, skip: int = 0, limit: int = 100) -> List[PayrollCycle]:
    return db.query(PayrollCycle).filter(PayrollCycle.company_id == company_id).offset(skip).limit(limit).all()


def create_payroll_cycle(db: Session, payroll_cycle: PayrollCycleCreate, company_id: int) -> PayrollCycle:
    db_cycle = PayrollCycle(
        company_id=company_id,
        name=payroll_cycle.name,
        start_date=payroll_cycle.start_date,
        end_date=payroll_cycle.end_date,
        payment_date=payroll_cycle.payment_date,
        status="draft"
    )
    db.add(db_cycle)
    db.commit()
    db.refresh(db_cycle)
    return db_cycle


def update_payroll_cycle(db: Session, cycle_id: int, payroll_cycle: PayrollCycleUpdate) -> Optional[PayrollCycle]:
    db_cycle = get_payroll_cycle(db, cycle_id)
    if db_cycle:
        update_data = payroll_cycle.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_cycle, key, value)
        db.commit()
        db.refresh(db_cycle)
    return db_cycle


def delete_payroll_cycle(db: Session, cycle_id: int) -> bool:
    db_cycle = get_payroll_cycle(db, cycle_id)
    if db_cycle:
        db.delete(db_cycle)
        db.commit()
        return True
    return False


# ========== Payroll Item CRUD ==========
def get_payroll_item(db: Session, item_id: int) -> Optional[PayrollItem]:
    return db.query(PayrollItem).filter(PayrollItem.id == item_id).first()


def get_payroll_items_by_cycle(db: Session, cycle_id: int, skip: int = 0, limit: int = 100) -> List[PayrollItem]:
    return db.query(PayrollItem).filter(PayrollItem.payroll_cycle_id == cycle_id).offset(skip).limit(limit).all()


def get_payroll_items_by_employee(db: Session, employee_id: int, skip: int = 0, limit: int = 100) -> List[PayrollItem]:
    return db.query(PayrollItem).filter(PayrollItem.employee_id == employee_id).offset(skip).limit(limit).all()


def create_payroll_item(db: Session, payroll_item: PayrollItemCreate, cycle_id: int) -> PayrollItem:
    db_item = PayrollItem(
        payroll_cycle_id=cycle_id,
        employee_id=payroll_item.employee_id,
        base_salary=payroll_item.base_salary,
        gross_salary=payroll_item.gross_salary,
        total_deductions=payroll_item.total_deductions,
        net_salary=payroll_item.net_salary,
        payment_method=payroll_item.payment_method,
        payment_reference=payroll_item.payment_reference
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_payroll_item(db: Session, item_id: int, payroll_item: PayrollItemUpdate) -> Optional[PayrollItem]:
    db_item = get_payroll_item(db, item_id)
    if db_item:
        update_data = payroll_item.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item


def delete_payroll_item(db: Session, item_id: int) -> bool:
    db_item = get_payroll_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False


# ========== Payroll Processing Functions ==========
def process_payroll_cycle(db: Session, cycle_id: int) -> Optional[PayrollCycle]:
    """Process payroll for all active employees in the company"""
    from datetime import datetime

    cycle = get_payroll_cycle(db, cycle_id)
    if not cycle or cycle.status != "draft":
        return None

    cycle.status = "processing"
    db.commit()

    # Get all active employees in the company
    employees = db.query(Employee).filter(
        and_(Employee.company_id == cycle.company_id, Employee.status == "active")
    ).all()

    total_amount = Decimal("0")

    for employee in employees:
        # Get employee salary details
        salary = db.query(Salary).filter(Salary.employee_id == employee.id).first()

        if salary:
            base = salary.base_salary
            allowances = (salary.housing_allowance + salary.transport_allowance +
                         salary.medical_allowance + salary.other_allowances)
            deductions = (salary.tax_deduction + salary.insurance_deduction +
                         salary.other_deductions)
            gross = base + allowances
            net = gross - deductions
        else:
            base = Decimal("0")
            allowances = Decimal("0")
            deductions = Decimal("0")
            gross = Decimal("0")
            net = Decimal("0")

        # Check if payroll item already exists
        existing_item = db.query(PayrollItem).filter(
            and_(
                PayrollItem.payroll_cycle_id == cycle_id,
                PayrollItem.employee_id == employee.id
            )
        ).first()

        if existing_item:
            existing_item.base_salary = base
            existing_item.gross_salary = gross
            existing_item.total_deductions = deductions
            existing_item.net_salary = net
        else:
            payroll_item = PayrollItem(
                payroll_cycle_id=cycle_id,
                employee_id=employee.id,
                base_salary=base,
                gross_salary=gross,
                total_deductions=deductions,
                net_salary=net
            )
            db.add(payroll_item)

        total_amount += net

    cycle.total_amount = total_amount
    cycle.status = "processed"
    db.commit()
    db.refresh(cycle)

    return cycle


def finalize_payroll_cycle(db: Session, cycle_id: int) -> Optional[PayrollCycle]:
    """Mark payroll cycle as paid"""
    from datetime import datetime

    cycle = get_payroll_cycle(db, cycle_id)
    if not cycle or cycle.status != "processed":
        return None

    cycle.status = "paid"
    cycle.payment_date = datetime.utcnow().date()

    # Update payment dates for all payroll items
    db.query(PayrollItem).filter(PayrollItem.payroll_cycle_id == cycle_id).update(
        {"payment_date": datetime.utcnow()}
    )

    db.commit()
    db.refresh(cycle)

    return cycle

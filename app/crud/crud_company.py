from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.models import Company, Employee
from app.schemas.schemas import CompanyCreate, CompanyUpdate
from app.core.security import get_password_hash
from datetime import datetime, timedelta


def get_company(db: Session, company_id: int) -> Optional[Company]:
    return db.query(Company).filter(Company.id == company_id).first()


def get_company_by_email(db: Session, email: str) -> Optional[Company]:
    return db.query(Company).filter(Company.business_email == email).first()


def get_companies(db: Session, skip: int = 0, limit: int = 100) -> List[Company]:
    return db.query(Company).offset(skip).limit(limit).all()


def create_company(db: Session, company: CompanyCreate, created_by: int) -> Company:
    # Create the company
    db_company = Company(
        name=company.name,
        business_email=company.business_email,
        phone=company.phone,
        address=company.address,
        created_by=created_by,
        subscription_expires_at=datetime.utcnow() + timedelta(days=30)  # 30 days trial
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    # Create the owner as an employee with company_owner role
    owner = Employee(
        email=company.owner_email,
        password_hash=get_password_hash(company.owner_password),
        full_name=company.owner_full_name,
        employee_id="OWNER001",
        role="company_owner",
        company_id=db_company.id,
        hire_date=datetime.utcnow().date()
    )
    db.add(owner)
    db.commit()

    return db_company


def update_company(db: Session, company_id: int, company: CompanyUpdate) -> Optional[Company]:
    db_company = get_company(db, company_id)
    if db_company:
        update_data = company.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_company, key, value)
        db.commit()
        db.refresh(db_company)
    return db_company


def delete_company(db: Session, company_id: int) -> bool:
    db_company = get_company(db, company_id)
    if db_company:
        db.delete(db_company)
        db.commit()
        return True
    return False

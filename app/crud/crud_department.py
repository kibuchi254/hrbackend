from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.models import Department, Position
from app.schemas.schemas import DepartmentCreate, DepartmentUpdate, PositionCreate, PositionUpdate


# ========== Department CRUD ==========
def get_department(db: Session, department_id: int) -> Optional[Department]:
    return db.query(Department).filter(Department.id == department_id).first()


def get_departments_by_company(db: Session, company_id: int, skip: int = 0, limit: int = 100) -> List[Department]:
    return db.query(Department).filter(Department.company_id == company_id).offset(skip).limit(limit).all()


def create_department(db: Session, department: DepartmentCreate, company_id: int) -> Department:
    db_department = Department(
        name=department.name,
        description=department.description,
        company_id=company_id,
        manager_id=department.manager_id
    )
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


def update_department(db: Session, department_id: int, department: DepartmentUpdate) -> Optional[Department]:
    db_department = get_department(db, department_id)
    if db_department:
        update_data = department.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_department, key, value)
        db.commit()
        db.refresh(db_department)
    return db_department


def delete_department(db: Session, department_id: int) -> bool:
    db_department = get_department(db, department_id)
    if db_department:
        db.delete(db_department)
        db.commit()
        return True
    return False


# ========== Position CRUD ==========
def get_position(db: Session, position_id: int) -> Optional[Position]:
    return db.query(Position).filter(Position.id == position_id).first()


def get_positions_by_department(db: Session, department_id: int, skip: int = 0, limit: int = 100) -> List[Position]:
    return db.query(Position).filter(Position.department_id == department_id).offset(skip).limit(limit).all()


def create_position(db: Session, position: PositionCreate, department_id: int) -> Position:
    db_position = Position(
        title=position.title,
        description=position.description,
        department_id=department_id,
        base_salary=position.base_salary
    )
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position


def update_position(db: Session, position_id: int, position: PositionUpdate) -> Optional[Position]:
    db_position = get_position(db, position_id)
    if db_position:
        update_data = position.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_position, key, value)
        db.commit()
        db.refresh(db_position)
    return db_position


def delete_position(db: Session, position_id: int) -> bool:
    db_position = get_position(db, position_id)
    if db_position:
        db.delete(db_position)
        db.commit()
        return True
    return False

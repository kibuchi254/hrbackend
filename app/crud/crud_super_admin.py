from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.models import SuperAdmin
from app.schemas.schemas import SuperAdminCreate, SuperAdminUpdate
from app.core.security import get_password_hash, verify_password


def get_super_admin(db: Session, super_admin_id: int) -> Optional[SuperAdmin]:
    return db.query(SuperAdmin).filter(SuperAdmin.id == super_admin_id).first()


def get_super_admin_by_email(db: Session, email: str) -> Optional[SuperAdmin]:
    return db.query(SuperAdmin).filter(SuperAdmin.email == email).first()


def get_super_admins(db: Session, skip: int = 0, limit: int = 100) -> List[SuperAdmin]:
    return db.query(SuperAdmin).offset(skip).limit(limit).all()


def create_super_admin(db: Session, super_admin: SuperAdminCreate) -> SuperAdmin:
    hashed_password = get_password_hash(super_admin.password)
    db_super_admin = SuperAdmin(
        email=super_admin.email,
        full_name=super_admin.full_name,
        password_hash=hashed_password
    )
    db.add(db_super_admin)
    db.commit()
    db.refresh(db_super_admin)
    return db_super_admin


def update_super_admin(db: Session, super_admin_id: int, super_admin: SuperAdminUpdate) -> Optional[SuperAdmin]:
    db_super_admin = get_super_admin(db, super_admin_id)
    if db_super_admin:
        update_data = super_admin.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_super_admin, key, value)
        db.commit()
        db.refresh(db_super_admin)
    return db_super_admin


def delete_super_admin(db: Session, super_admin_id: int) -> bool:
    db_super_admin = get_super_admin(db, super_admin_id)
    if db_super_admin:
        db.delete(db_super_admin)
        db.commit()
        return True
    return False


def authenticate_super_admin(db: Session, email: str, password: str) -> Optional[SuperAdmin]:
    super_admin = get_super_admin_by_email(db, email)
    if not super_admin or not super_admin.is_active:
        return None
    if not verify_password(password, super_admin.password_hash):
        return None
    return super_admin

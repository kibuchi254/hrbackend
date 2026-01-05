from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.database import get_db
from app.core.security import create_access_token
from app.core.config import settings
from app.crud.crud_super_admin import authenticate_super_admin, create_super_admin
from app.crud.crud_employee import authenticate_employee
from app.schemas.schemas import SuperAdminCreate, SuperAdminLogin, Token, EmployeeResponse, SuperAdminResponse

# Import get_current_user to avoid circular dependency
from app.core.deps import get_current_user

router = APIRouter()


@router.post("/super-admin/register", response_model=SuperAdminResponse)
async def register_super_admin(super_admin: SuperAdminCreate, db: Session = Depends(get_db)):
    """Register a new super admin"""
    from app.crud.crud_super_admin import get_super_admin_by_email

    db_super_admin = get_super_admin_by_email(db, email=super_admin.email)
    if db_super_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    return create_super_admin(db=db, super_admin=super_admin)


@router.post("/super-admin/login", response_model=Token)
async def login_super_admin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login for super admin users"""
    super_admin = authenticate_super_admin(db, form_data.username, form_data.password)
    if not super_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": super_admin.id, "email": super_admin.email, "role": "super_admin"},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login_employee(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login for company employees (all roles)"""
    employee = authenticate_employee(db, form_data.username, form_data.password)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": employee.id,
            "email": employee.email,
            "role": employee.role,
            "company_id": employee.company_id
        },
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=dict)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    user = current_user["user"]
    role = current_user["role"]

    if role == "super_admin":
        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": role,
            "is_active": user.is_active
        }
    else:
        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": role,
            "company_id": user.company_id,
            "employee_id": user.employee_id,
            "status": user.status
        }

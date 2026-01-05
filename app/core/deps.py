from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.models import SuperAdmin, Employee
from app.crud.crud_super_admin import get_super_admin as get_super_admin_crud
from app.crud.crud_employee import get_employee as get_employee_crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id: Optional[int] = payload.get("sub")
    role: Optional[str] = payload.get("role")
    company_id: Optional[int] = payload.get("company_id")

    if user_id is None or role is None:
        raise credentials_exception

    if role == "super_admin":
        user = get_super_admin_crud(db, user_id)
    elif role in ["company_admin", "hr_manager", "payroll_manager", "recruitment_manager", "employee"]:
        user = get_employee_crud(db, user_id)
    else:
        raise credentials_exception

    if user is None:
        raise credentials_exception

    return {"user": user, "role": role, "company_id": company_id}


async def get_current_super_admin(
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can access this resource"
        )
    return current_user


async def get_current_company_admin(
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] not in ["company_admin", "hr_manager", "payroll_manager", "recruitment_manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only company admins can access this resource"
        )
    return current_user


async def get_current_employee(
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "employee":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employees can access this resource"
        )
    return current_user


async def verify_company_access(
    current_user: dict = Depends(get_current_user),
    company_id: int = None
):
    """Verify that the current user has access to the specified company"""
    if current_user["role"] == "super_admin":
        return current_user

    if current_user["company_id"] != company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this company's data"
        )

    return current_user

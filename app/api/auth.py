# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
import logging
from pydantic import BaseModel, EmailStr

from app.core.database import get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.core.config import settings
from app.crud.crud_super_admin import authenticate_super_admin, create_super_admin
from app.crud.crud_employee import authenticate_employee
from app.schemas.schemas import SuperAdminCreate, SuperAdminResponse, Token, EmployeeResponse
from app.core.deps import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()


# ========== JSON Login Request Schema ==========
class LoginRequest(BaseModel):
    """JSON login request body"""
    username: EmailStr
    password: str


# ========== Super Admin Routes ==========

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
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login for super admin users
    
    Request body (JSON):
    {
        "username": "superadmin@hrpayroll.com",
        "password": "superadmin123"
    }
    """
    logger.info(f"Super admin login attempt for: {credentials.username}")
    
    super_admin = authenticate_super_admin(db, credentials.username, credentials.password)
    if not super_admin:
        logger.warning(f"Failed login attempt for super admin: {credentials.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info(f"Successful super admin login: {credentials.username}")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": super_admin.id,
            "email": super_admin.email,
            "role": "super_admin"
        },
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


# ========== Employee Routes ==========

@router.post("/login", response_model=Token)
async def login_employee(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login for company employees (all roles)
    
    Request body (JSON):
    {
        "username": "employee@company.com",
        "password": "employee_password"
    }
    """
    logger.info(f"Employee login attempt for: {credentials.username}")
    
    employee = authenticate_employee(db, credentials.username, credentials.password)
    if not employee:
        logger.warning(f"Failed login attempt for employee: {credentials.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info(f"Successful employee login: {credentials.username}")
    
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


# ========== User Info Route ==========

class CurrentUserResponse(BaseModel):
    """Response schema for /me endpoint"""
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool = None
    company_id: int = None
    employee_id: str = None
    status: str = None

    class Config:
        from_attributes = True


@router.get("/me", response_model=CurrentUserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current authenticated user information
    
    Headers required:
    Authorization: Bearer <access_token>
    """
    try:
        logger.info(f"Getting current user info - Data structure: {current_user.keys()}")
        
        # Extract user object and role from dependency
        user = current_user.get("user")
        role = current_user.get("role")
        company_id = current_user.get("company_id")
        
        # Validate user exists
        if user is None:
            logger.error("User is None in current_user dependency")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Validate role exists
        if role is None:
            logger.error("Role is None in current_user dependency")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Role not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        logger.info(f"Current user - ID: {user.id}, Email: {user.email}, Role: {role}")
        
        # Return different response based on role
        if role == "super_admin":
            return {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role": role,
                "is_active": user.is_active,
                "company_id": None,
                "employee_id": None,
                "status": None
            }
        else:
            # For employees
            return {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role": role,
                "is_active": None,
                "company_id": user.company_id,
                "employee_id": user.employee_id,
                "status": user.status
            }
            
    except HTTPException:
        raise
    except AttributeError as e:
        logger.error(f"AttributeError in /me endpoint: {str(e)}")
        logger.error(f"User object type: {type(user)}, User object: {user}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"User object structure error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error in /me endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """
    Logout endpoint (token invalidation on client side)
    Just verify token is valid and return success
    """
    logger.info(f"User logout: {current_user.get('user').email}")
    return {"message": "Successfully logged out. Please discard the access token."}


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}
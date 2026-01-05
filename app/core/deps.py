import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.security import decode_access_token

# Configure logging
logger = logging.getLogger(__name__)

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

    # Log authentication attempt
    if len(token) > 30:
        token_preview = token[:20] + "..." + token[-10:]
    else:
        token_preview = token
    logger.info(f"Authentication attempt - Token: {token_preview}")

    # Decode token
    payload = decode_access_token(token)
    if payload is None:
        logger.error("Token decode failed - payload is None")
        raise credentials_exception

    # Extract payload fields
    user_id = payload.get("sub")
    role = payload.get("role")
    company_id = payload.get("company_id")
    email = payload.get("email")

    # Log payload extraction
    logger.info(f"Payload extracted - User ID: {user_id}, Role: {role}, Company ID: {company_id}, Email: {email}")

    if user_id is None or role is None:
        logger.error(f"Missing required fields - User ID: {user_id}, Role: {role}")
        raise credentials_exception

    # Lazy import to avoid circular dependency
    from app.crud.crud_super_admin import get_super_admin as get_super_admin_crud
    from app.crud.crud_employee import get_employee as get_employee_crud

    # Look up user in database
    logger.info(f"Looking up user in database - Role: {role}, User ID: {user_id}")

    try:
        if role == "super_admin":
            from app.models.models import SuperAdmin
            user = get_super_admin_crud(db, user_id)
        elif role in ["company_admin", "hr_manager", "payroll_manager", "recruitment_manager", "employee"]:
            user = get_employee_crud(db, user_id)
        else:
            logger.error(f"Invalid role: {role}")
            raise credentials_exception

        if user is None:
            logger.error(f"User not found in database - User ID: {user_id}, Role: {role}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found in database",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logger.info(f"User found successfully - User ID: {user.id}, Role: {role}, Email: {user.email}")

        return {"user": user, "role": role, "company_id": company_id}

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error in get_current_user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_super_admin(
    current_user: dict = Depends(get_current_user)
):
    role = current_user.get("role")
    if role != "super_admin":
        logger.error(f"Unauthorized access attempt - Role: {role}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can access this resource"
        )
    return current_user


async def get_current_company_admin(
    current_user: dict = Depends(get_current_user)
):
    role = current_user.get("role")
    if role not in ["company_admin", "hr_manager", "payroll_manager", "recruitment_manager"]:
        logger.error(f"Unauthorized company admin access attempt - Role: {role}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only company admins can access this resource"
        )
    return current_user


async def get_current_employee(
    current_user: dict = Depends(get_current_user)
):
    role = current_user.get("role")
    if role != "employee":
        logger.error(f"Unauthorized employee access attempt - Role: {role}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employees can access this resource"
        )
    return current_user


async def verify_company_access(
    current_user: dict = Depends(get_current_user),
    company_id: int = None
):
    """Verify that current user has access to the specified company"""
    role = current_user.get("role")
    current_company_id = current_user.get("company_id")
    
    logger.info(f"Company access verification - Role: {role}, User Company ID: {current_company_id}, Requested Company ID: {company_id}")
    
    if role == "super_admin":
        logger.info("Super admin access granted (no company restriction)")
        return current_user

    if current_company_id != company_id:
        logger.error(f"Company access denied - User Company ID: {current_company_id}, Requested Company ID: {company_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this company's data"
        )

    return current_user

# app/core/deps.py
import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_access_token

logger = logging.getLogger(__name__)

# Fixed token URL to match your auth routes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/super-admin/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Dependency to get current authenticated user
    Returns: {"user": user_object, "role": role_string, "company_id": company_id_or_none}
    """
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

    logger.info(f"Token decoded - User ID: {user_id}, Role: {role}, Company ID: {company_id}, Email: {email}")

    # Validate required fields
    if user_id is None or role is None:
        logger.error(f"Missing required token fields - User ID: {user_id}, Role: {role}")
        raise credentials_exception

    # Lazy import to avoid circular dependency
    from app.crud.crud_super_admin import get_super_admin
    from app.crud.crud_employee import get_employee

    try:
        # Look up user in database based on role
        logger.info(f"Looking up user - Role: {role}, User ID: {user_id}")

        if role == "super_admin":
            user = get_super_admin(db, user_id)
            if user is None:
                logger.error(f"Super admin not found - User ID: {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Super admin not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        elif role in ["company_admin", "hr_manager", "payroll_manager", "recruitment_manager", "employee"]:
            user = get_employee(db, user_id)
            if user is None:
                logger.error(f"Employee not found - User ID: {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Employee not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        else:
            logger.error(f"Invalid role in token: {role}")
            raise credentials_exception

        logger.info(f"User found successfully - ID: {user.id}, Email: {user.email}, Role: {role}")

        # Return user dictionary for use in routes
        return {
            "user": user,
            "role": role,
            "company_id": company_id
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_current_user: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during authentication",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_super_admin(
    current_user: dict = Depends(get_current_user)
):
    """
    Dependency to ensure current user is a super admin
    """
    role = current_user.get("role")
    if role != "super_admin":
        logger.error(f"Unauthorized access attempt - Required: super_admin, Got: {role}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can access this resource"
        )
    return current_user


async def get_current_company_admin(
    current_user: dict = Depends(get_current_user)
):
    """
    Dependency to ensure current user is a company admin or manager
    """
    role = current_user.get("role")
    allowed_roles = ["company_admin", "hr_manager", "payroll_manager", "recruitment_manager"]
    
    if role not in allowed_roles:
        logger.error(f"Unauthorized company admin access - Required: {allowed_roles}, Got: {role}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only company admins can access this resource"
        )
    return current_user


async def get_current_employee(
    current_user: dict = Depends(get_current_user)
):
    """
    Dependency to ensure current user is an employee
    """
    role = current_user.get("role")
    if role != "employee":
        logger.error(f"Unauthorized employee access - Required: employee, Got: {role}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employees can access this resource"
        )
    return current_user


async def verify_company_access(
    current_user: dict = Depends(get_current_user),
    company_id: int = None
):
    """
    Verify that current user has access to the specified company
    Super admins have access to all companies
    """
    role = current_user.get("role")
    user_company_id = current_user.get("company_id")
    
    logger.info(f"Company access verification - Role: {role}, User Company: {user_company_id}, Requested: {company_id}")
    
    if role == "super_admin":
        logger.info("Super admin - access granted to all companies")
        return current_user

    if user_company_id != company_id:
        logger.error(f"Company access denied - User Company: {user_company_id}, Requested: {company_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this company's data"
        )

    return current_user
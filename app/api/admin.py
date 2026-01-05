from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_super_admin
from app.crud.crud_super_admin import get_super_admins, create_super_admin, update_super_admin, delete_super_admin, get_super_admin as get_super_admin_crud
from app.crud.crud_company import get_companies, create_company, update_company, delete_company, get_company as get_company_crud
from app.schemas.schemas import (
    SuperAdminCreate, SuperAdminUpdate, SuperAdminResponse,
    CompanyCreate, CompanyUpdate, CompanyResponse
)

router = APIRouter()


# ========== Super Admin Management ==========
@router.get("/super-admins", response_model=List[SuperAdminResponse])
async def list_super_admins(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_super_admin),
    db: Session = Depends(get_db)
):
    """List all super admins"""
    return get_super_admins(db, skip=skip, limit=limit)


@router.post("/super-admins", response_model=SuperAdminResponse)
async def create_new_super_admin(
    super_admin: SuperAdminCreate,
    current_user: dict = Depends(get_current_super_admin),
    db: Session = Depends(get_db)
):
    """Create a new super admin"""
    from app.crud.crud_super_admin import get_super_admin_by_email

    db_super_admin = get_super_admin_by_email(db, email=super_admin.email)
    if db_super_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    return create_super_admin(db=db, super_admin=super_admin)


@router.get("/super-admins/{admin_id}", response_model=SuperAdminResponse)
async def get_super_admin(
    admin_id: int,
    current_user: dict = Depends(get_current_super_admin),
    db: Session = Depends(get_db)
):
    """Get super admin by ID"""
    admin = get_super_admin_crud(db, admin_id)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Super Admin not found"
        )
    return admin


@router.put("/super-admins/{admin_id}", response_model=SuperAdminResponse)
async def update_super_admin_endpoint(
    admin_id: int,
    super_admin: SuperAdminUpdate,
    current_user: dict = Depends(get_current_super_admin),
    db: Session = Depends(get_db)
):
    """Update super admin"""
    updated_admin = update_super_admin(db, admin_id, super_admin)
    if not updated_admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Super Admin not found"
        )
    return updated_admin


@router.delete("/super-admins/{admin_id}")
async def delete_super_admin_endpoint(
    admin_id: int,
    current_user: dict = Depends(get_current_super_admin),
    db: Session = Depends(get_db)
):
    """Delete super admin"""
    success = delete_super_admin(db, admin_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Super Admin not found"
        )
    return {"message": "Super Admin deleted successfully"}


# ========== Company Management ==========
@router.get("/companies", response_model=List[CompanyResponse])
async def list_companies(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_super_admin),
    db: Session = Depends(get_db)
):
    """List all companies"""
    return get_companies(db, skip=skip, limit=limit)


@router.post("/companies", response_model=CompanyResponse)
async def create_new_company(
    company: CompanyCreate,
    current_user: dict = Depends(get_current_super_admin),
    db: Session = Depends(get_db)
):
    """Create a new company and its owner"""
    from app.crud.crud_company import get_company_by_email

    db_company = get_company_by_email(db, email=company.business_email)
    if db_company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company email already registered"
        )

    return create_company(db=db, company=company, created_by=current_user["user"].id)


@router.get("/companies/{company_id}", response_model=CompanyResponse)
async def get_company_endpoint(
    company_id: int,
    current_user: dict = Depends(get_current_super_admin),
    db: Session = Depends(get_db)
):
    """Get company by ID"""
    company = get_company_crud(db, company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    return company


@router.put("/companies/{company_id}", response_model=CompanyResponse)
async def update_company_endpoint(
    company_id: int,
    company: CompanyUpdate,
    current_user: dict = Depends(get_current_super_admin),
    db: Session = Depends(get_db)
):
    """Update company"""
    updated_company = update_company(db, company_id, company)
    if not updated_company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    return updated_company


@router.delete("/companies/{company_id}")
async def delete_company_endpoint(
    company_id: int,
    current_user: dict = Depends(get_current_super_admin),
    db: Session = Depends(get_db)
):
    """Delete company"""
    success = delete_company(db, company_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    return {"message": "Company deleted successfully"}

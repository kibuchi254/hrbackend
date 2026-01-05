from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_user, verify_company_access, get_current_company_admin, get_current_employee
from app.crud.crud_payroll import (
    get_payroll_cycle, create_payroll_cycle, update_payroll_cycle, delete_payroll_cycle,
    get_payroll_cycles_by_company,
    get_payroll_item, create_payroll_item, update_payroll_item, delete_payroll_item,
    get_payroll_items_by_cycle, get_payroll_items_by_employee,
    process_payroll_cycle, finalize_payroll_cycle
)
from app.schemas.schemas import (
    PayrollCycleCreate, PayrollCycleUpdate, PayrollCycleResponse,
    PayrollItemCreate, PayrollItemUpdate, PayrollItemResponse
)

router = APIRouter()


# ========== Payroll Cycle Management ==========
@router.get("/cycles", response_model=List[PayrollCycleResponse])
async def list_payroll_cycles(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(verify_company_access),
    db: Session = Depends(get_db)
):
    """List all payroll cycles for the company"""
    company_id = current_user["company_id"]
    return get_payroll_cycles_by_company(db, company_id=company_id, skip=skip, limit=limit)


@router.post("/cycles", response_model=PayrollCycleResponse)
async def create_new_payroll_cycle(
    cycle: PayrollCycleCreate,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Create a new payroll cycle"""
    company_id = current_user["company_id"]
    return create_payroll_cycle(db=db, payroll_cycle=cycle, company_id=company_id)


@router.get("/cycles/{cycle_id}", response_model=PayrollCycleResponse)
async def get_payroll_cycle_endpoint(
    cycle_id: int,
    current_user: dict = Depends(verify_company_access),
    db: Session = Depends(get_db)
):
    """Get payroll cycle by ID"""
    cycle = get_payroll_cycle(db, cycle_id)
    if not cycle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll cycle not found"
        )

    # Verify cycle belongs to company
    if cycle.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return cycle


@router.put("/cycles/{cycle_id}", response_model=PayrollCycleResponse)
async def update_payroll_cycle_endpoint(
    cycle_id: int,
    cycle: PayrollCycleUpdate,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Update payroll cycle"""
    db_cycle = get_payroll_cycle(db, cycle_id)
    if not db_cycle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll cycle not found"
        )

    if db_cycle.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    updated_cycle = update_payroll_cycle(db, cycle_id, cycle)
    return updated_cycle


@router.delete("/cycles/{cycle_id}")
async def delete_payroll_cycle_endpoint(
    cycle_id: int,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Delete payroll cycle"""
    db_cycle = get_payroll_cycle(db, cycle_id)
    if not db_cycle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll cycle not found"
        )

    if db_cycle.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    success = delete_payroll_cycle(db, cycle_id)
    return {"message": "Payroll cycle deleted successfully"}


@router.post("/cycles/{cycle_id}/process", response_model=PayrollCycleResponse)
async def process_payroll_cycle_endpoint(
    cycle_id: int,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Process payroll cycle - calculate salaries for all employees"""
    db_cycle = get_payroll_cycle(db, cycle_id)
    if not db_cycle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll cycle not found"
        )

    if db_cycle.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    processed_cycle = process_payroll_cycle(db, cycle_id)
    if not processed_cycle:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot process payroll cycle. It must be in draft status."
        )

    return processed_cycle


@router.post("/cycles/{cycle_id}/finalize", response_model=PayrollCycleResponse)
async def finalize_payroll_cycle_endpoint(
    cycle_id: int,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Finalize payroll cycle - mark as paid"""
    db_cycle = get_payroll_cycle(db, cycle_id)
    if not db_cycle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll cycle not found"
        )

    if db_cycle.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    finalized_cycle = finalize_payroll_cycle(db, cycle_id)
    if not finalized_cycle:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot finalize payroll cycle. It must be in processed status."
        )

    return finalized_cycle


# ========== Payroll Item Management ==========
@router.get("/cycles/{cycle_id}/items", response_model=List[PayrollItemResponse])
async def list_payroll_items_by_cycle(
    cycle_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(verify_company_access),
    db: Session = Depends(get_db)
):
    """List all payroll items in a cycle"""
    # Verify cycle belongs to company
    cycle = get_payroll_cycle(db, cycle_id)
    if not cycle or cycle.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll cycle not found"
        )

    return get_payroll_items_by_cycle(db, cycle_id=cycle_id, skip=skip, limit=limit)


@router.get("/employees/{employee_id}/payroll", response_model=List[PayrollItemResponse])
async def list_employee_payroll(
    employee_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List payroll items for an employee"""
    from app.crud.crud_employee import get_employee

    employee = get_employee(db, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    # Verify access
    if current_user["role"] == "employee" and current_user["user"].id != employee_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    if current_user["role"] in ["company_owner", "company_admin"] and employee.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return get_payroll_items_by_employee(db, employee_id=employee_id, skip=skip, limit=limit)


@router.get("/items/{item_id}", response_model=PayrollItemResponse)
async def get_payroll_item_endpoint(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get payroll item by ID"""
    item = get_payroll_item(db, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll item not found"
        )

    # Verify access
    from app.crud.crud_employee import get_employee
    from app.crud.crud_payroll import get_payroll_cycle
    cycle = get_payroll_cycle(db, item.payroll_cycle_id)

    if current_user["role"] == "employee" and current_user["user"].id != item.employee_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    if current_user["role"] in ["company_owner", "company_admin"] and cycle.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return item


@router.post("/cycles/{cycle_id}/items", response_model=PayrollItemResponse)
async def create_new_payroll_item(
    cycle_id: int,
    item: PayrollItemCreate,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Add a payroll item to a cycle"""
    # Verify cycle belongs to company
    cycle = get_payroll_cycle(db, cycle_id)
    if not cycle or cycle.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll cycle not found"
        )

    # Validate employee belongs to company
    from app.crud.crud_employee import get_employee
    employee = get_employee(db, item.employee_id)
    if not employee or employee.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid employee"
        )

    return create_payroll_item(db=db, payroll_item=item, cycle_id=cycle_id)


@router.put("/items/{item_id}", response_model=PayrollItemResponse)
async def update_payroll_item_endpoint(
    item_id: int,
    item: PayrollItemUpdate,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Update payroll item"""
    db_item = get_payroll_item(db, item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll item not found"
        )

    # Verify cycle belongs to company
    from app.crud.crud_payroll import get_payroll_cycle
    cycle = get_payroll_cycle(db, db_item.payroll_cycle_id)
    if cycle.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    updated_item = update_payroll_item(db, item_id, item)
    return updated_item


@router.delete("/items/{item_id}")
async def delete_payroll_item_endpoint(
    item_id: int,
    current_user: dict = Depends(get_current_company_admin),
    db: Session = Depends(get_db)
):
    """Delete payroll item"""
    db_item = get_payroll_item(db, item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll item not found"
        )

    # Verify cycle belongs to company
    from app.crud.crud_payroll import get_payroll_cycle
    cycle = get_payroll_cycle(db, db_item.payroll_cycle_id)
    if cycle.company_id != current_user["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    success = delete_payroll_item(db, item_id)
    return {"message": "Payroll item deleted successfully"}

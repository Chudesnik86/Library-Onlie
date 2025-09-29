from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from services import CustomerService
from dto import (
    CustomerCreateDTO, CustomerUpdateDTO, CustomerResponseDTO, 
    CustomerSearchDTO
)
from database import get_db
from auth import verify_token

router = APIRouter(prefix="/customers", tags=["customers"])


def get_customer_service(db: Session = Depends(get_db)) -> CustomerService:
    """Получить сервис клиентов"""
    return CustomerService(db)


@router.get("", response_model=List[CustomerResponseDTO])
async def get_customers(
    customer_id: Optional[int] = Query(None),
    name: Optional[str] = Query(None),
    customer_service: CustomerService = Depends(get_customer_service),
    current_user: str = Depends(verify_token)
):
    """Получить список клиентов с поиском (требует аутентификации)"""
    search_params = CustomerSearchDTO(
        customer_id=customer_id,
        name=name
    )
    
    return customer_service.get_customers(search_params)


@router.get("/{customer_id}", response_model=CustomerResponseDTO)
async def get_customer(
    customer_id: int,
    customer_service: CustomerService = Depends(get_customer_service),
    current_user: str = Depends(verify_token)
):
    """Получить клиента по ID (требует аутентификации)"""
    customer = customer_service.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.post("", response_model=CustomerResponseDTO)
async def create_customer(
    customer: CustomerCreateDTO,
    customer_service: CustomerService = Depends(get_customer_service),
    current_user: str = Depends(verify_token)
):
    """Создать нового клиента (требует аутентификации)"""
    return customer_service.create_customer(customer)


@router.put("/{customer_id}", response_model=CustomerResponseDTO)
async def update_customer(
    customer_id: int,
    customer: CustomerUpdateDTO,
    customer_service: CustomerService = Depends(get_customer_service),
    current_user: str = Depends(verify_token)
):
    """Обновить клиента (требует аутентификации)"""
    updated_customer = customer_service.update_customer(customer_id, customer)
    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated_customer





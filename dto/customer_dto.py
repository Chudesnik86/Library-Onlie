from pydantic import BaseModel
from typing import List, Optional
from .base import BaseDTO, SearchDTO


class CustomerBaseDTO(BaseModel):
    """Базовый DTO для клиента"""
    name: str
    address: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class CustomerCreateDTO(CustomerBaseDTO):
    """DTO для создания клиента"""
    pass


class CustomerUpdateDTO(CustomerBaseDTO):
    """DTO для обновления клиента"""
    pass


class CustomerResponseDTO(CustomerBaseDTO):
    """DTO для ответа с клиентом"""
    id: int
    issues: List[dict] = []  # Используем dict вместо IssueResponseDTO для избежания циклических импортов


class CustomerSearchDTO(SearchDTO):
    """DTO для поиска клиентов"""
    customer_id: Optional[int] = None
    name: Optional[str] = None


class CustomerListResponseDTO(BaseModel):
    """DTO для списка клиентов"""
    items: List[CustomerResponseDTO]
    total: int
    page: int
    limit: int
    total_pages: int


# Update forward references
CustomerResponseDTO.model_rebuild()

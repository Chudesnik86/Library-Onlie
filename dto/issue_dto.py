from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from .base import BaseDTO


class IssueBaseDTO(BaseModel):
    """Базовый DTO для выдачи"""
    book_key: int
    customer_id: int
    date_of_issue: date
    return_until: date
    renewed: bool = False


class IssueCreateDTO(BaseModel):
    """DTO для создания выдачи"""
    book_key: int
    customer_id: int


class IssueResponseDTO(IssueBaseDTO):
    """DTO для ответа с выдачей"""
    id: int
    return_date: Optional[date] = None
    created_at: datetime
    book: dict  # Используем dict вместо BookResponseDTO для избежания циклических импортов
    customer: dict  # Используем dict вместо CustomerResponseDTO для избежания циклических импортов


class IssueWithBookDTO(BaseModel):
    """DTO для выдачи с информацией о книге"""
    id: int
    book: dict  # Book info
    date_of_issue: date
    return_until: date
    return_date: Optional[date] = None
    renewed: bool
    is_overdue: bool = False
    was_overdue: bool = False


class IssueWithCustomerDTO(BaseModel):
    """DTO для выдачи с информацией о клиенте"""
    id: int
    customer: dict  # Customer info
    date_of_issue: date
    return_until: date
    return_date: Optional[date] = None
    renewed: bool


class IssueReturnDTO(BaseModel):
    """DTO для возврата книги"""
    issue_id: int


class IssueRenewDTO(BaseModel):
    """DTO для продления выдачи"""
    issue_id: int


class IssueRenewResponseDTO(BaseModel):
    """DTO для ответа при продлении выдачи"""
    message: str
    new_return_date: date


class IssueReturnResponseDTO(BaseModel):
    """DTO для ответа при возврате книги"""
    message: str


# Forward references больше не нужны, так как используем dict


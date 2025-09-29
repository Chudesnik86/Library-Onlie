from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class BaseDTO(BaseModel):
    """Базовый DTO класс"""
    class Config:
        from_attributes = True


class PaginationDTO(BaseModel):
    """DTO для пагинации"""
    page: int = 1
    limit: int = 50
    total: Optional[int] = None
    total_pages: Optional[int] = None


class SearchDTO(BaseModel):
    """Базовый DTO для поиска"""
    skip: int = 0
    limit: int = 50





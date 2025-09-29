from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional
from .base import BaseDTO, SearchDTO


class BookBaseDTO(BaseModel):
    """Базовый DTO для книги"""
    title: str
    subtitle: Optional[str] = None
    first_publish_date: Optional[date] = None
    description: Optional[str] = None


class BookCreateDTO(BookBaseDTO):
    """DTO для создания книги"""
    authors_keys: Optional[List[int]] = None
    subjects: Optional[List[str]] = None


class BookUpdateDTO(BookCreateDTO):
    """DTO для обновления книги"""
    pass


class BookResponseDTO(BookBaseDTO):
    """DTO для ответа с книгой"""
    key: int
    authors: List["AuthorResponseDTO"] = Field(default_factory=list)
    subjects: List["BookSubjectResponseDTO"] = Field(default_factory=list)
    covers: List["BookCoverResponseDTO"] = Field(default_factory=list)
    is_available: bool = True


class BookSearchDTO(SearchDTO):
    """DTO для поиска книг"""
    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None


class BookListResponseDTO(BaseModel):
    """DTO для списка книг с пагинацией"""
    items: List[BookResponseDTO]
    total: int
    page: int
    limit: int
    total_pages: int


# Author DTOs
class AuthorBaseDTO(BaseModel):
    """Базовый DTO для автора"""
    name: str
    biography: Optional[str] = None
    birth_date: Optional[date] = None
    death_date: Optional[date] = None
    wikipedia: Optional[str] = None


class AuthorCreateDTO(AuthorBaseDTO):
    """DTO для создания автора"""
    pass


class AuthorResponseDTO(AuthorBaseDTO):
    """DTO для ответа с автором"""
    key: int


# Book Cover DTOs
class BookCoverBaseDTO(BaseModel):
    """Базовый DTO для обложки книги"""
    cover_file: str


class BookCoverCreateDTO(BookCoverBaseDTO):
    """DTO для создания обложки книги"""
    book_key: int


class BookCoverResponseDTO(BookCoverBaseDTO):
    """DTO для ответа с обложкой книги"""
    id: int
    book_key: int


# Book Subject DTOs
class BookSubjectBaseDTO(BaseModel):
    """Базовый DTO для темы книги"""
    subject: str


class BookSubjectCreateDTO(BookSubjectBaseDTO):
    """DTO для создания темы книги"""
    book_key: int


class BookSubjectResponseDTO(BookSubjectBaseDTO):
    """DTO для ответа с темой книги"""
    id: int
    book_key: int


# Update forward references
BookResponseDTO.model_rebuild()





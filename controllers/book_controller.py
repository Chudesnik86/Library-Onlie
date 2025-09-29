from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from services import BookService
from dto import (
    BookCreateDTO, BookUpdateDTO, BookResponseDTO, BookSearchDTO, 
    BookListResponseDTO, TokenDTO
)
from database import get_db
from auth import verify_token

router = APIRouter(prefix="/books", tags=["books"])


def get_book_service(db: Session = Depends(get_db)) -> BookService:
    """Получить сервис книг"""
    return BookService(db)


@router.get("", response_model=BookListResponseDTO)
async def get_books(
    title: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    subject: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    book_service: BookService = Depends(get_book_service)
):
    """Получить список книг с поиском и пагинацией"""
    search_params = BookSearchDTO(
        title=title,
        author=author,
        subject=subject,
        skip=(page - 1) * limit,
        limit=limit
    )
    
    return book_service.get_books(search_params)


@router.get("/{book_key}", response_model=BookResponseDTO)
async def get_book(
    book_key: int,
    book_service: BookService = Depends(get_book_service)
):
    """Получить книгу по ключу"""
    book = book_service.get_book(book_key)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("", response_model=BookResponseDTO)
async def create_book(
    book: BookCreateDTO,
    book_service: BookService = Depends(get_book_service),
    current_user: str = Depends(verify_token)
):
    """Создать новую книгу (требует аутентификации)"""
    return book_service.create_book(book)


@router.put("/{book_key}", response_model=BookResponseDTO)
async def update_book(
    book_key: int,
    book: BookUpdateDTO,
    book_service: BookService = Depends(get_book_service),
    current_user: str = Depends(verify_token)
):
    """Обновить книгу (требует аутентификации)"""
    updated_book = book_service.update_book(book_key, book)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


@router.delete("/{book_key}")
async def delete_book(
    book_key: int,
    book_service: BookService = Depends(get_book_service),
    current_user: str = Depends(verify_token)
):
    """Удалить книгу (требует аутентификации)"""
    success = book_service.delete_book(book_key)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted"}


@router.get("/{book_key}/availability")
async def check_book_availability(
    book_key: int,
    book_service: BookService = Depends(get_book_service)
):
    """Проверить доступность книги"""
    book = book_service.get_book(book_key)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    available = book_service.check_book_availability(book_key)
    return {
        "book_key": book_key,
        "title": book.title,
        "is_available": available
    }





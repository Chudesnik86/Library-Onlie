from sqlalchemy.orm import Session
from typing import List, Optional
from repositories import BookRepository, AuthorRepository
from dto import BookCreateDTO, BookUpdateDTO, BookResponseDTO, BookSearchDTO, BookListResponseDTO
from models import Book


class BookService:
    """Сервис для работы с книгами"""
    
    def __init__(self, db: Session):
        self.db = db
        self.book_repo = BookRepository(db)
        self.author_repo = AuthorRepository(db)
    
    def get_books(self, search_params: BookSearchDTO) -> BookListResponseDTO:
        """Получить список книг с поиском и пагинацией"""
        books = self.book_repo.search_books(
            title=search_params.title,
            author=search_params.author,
            subject=search_params.subject,
            skip=search_params.skip,
            limit=search_params.limit
        )
        
        total = self.book_repo.get_books_count(
            title=search_params.title,
            author=search_params.author,
            subject=search_params.subject
        )
        
        # Преобразовать в DTO
        book_dtos = []
        for book in books:
            book_dto = self._convert_to_response_dto(book)
            book_dtos.append(book_dto)
        
        total_pages = (total + search_params.limit - 1) // search_params.limit
        
        return BookListResponseDTO(
            items=book_dtos,
            total=total,
            page=search_params.skip // search_params.limit + 1,
            limit=search_params.limit,
            total_pages=total_pages
        )
    
    def get_book(self, book_key: int) -> Optional[BookResponseDTO]:
        """Получить книгу по ключу"""
        book = self.book_repo.get_by_key(book_key)
        if not book:
            return None
        
        return self._convert_to_response_dto(book)
    
    def create_book(self, book_data: BookCreateDTO) -> BookResponseDTO:
        """Создать новую книгу"""
        book_dict = book_data.dict(exclude={'authors_keys', 'subjects'})
        
        book = self.book_repo.create_with_relations(
            book_dict,
            authors_keys=book_data.authors_keys,
            subjects=book_data.subjects
        )
        
        return self._convert_to_response_dto(book)
    
    def update_book(self, book_key: int, book_data: BookUpdateDTO) -> Optional[BookResponseDTO]:
        """Обновить книгу"""
        book_dict = book_data.dict(exclude={'authors_keys', 'subjects'})
        
        book = self.book_repo.update_with_relations(
            book_key,
            book_dict,
            authors_keys=book_data.authors_keys,
            subjects=book_data.subjects
        )
        
        if not book:
            return None
        
        return self._convert_to_response_dto(book)
    
    def delete_book(self, book_key: int) -> bool:
        """Удалить книгу"""
        return self.book_repo.delete_with_relations(book_key)
    
    def check_book_availability(self, book_key: int) -> bool:
        """Проверить доступность книги"""
        return self.book_repo.is_book_available(book_key)
    
    def get_book_history(self, book_key: int) -> List[dict]:
        """Получить историю выдачи книги"""
        issues = self.book_repo.db.query(self.book_repo.db.query().filter(
            self.book_repo.db.query().filter().book_key == book_key
        ).order_by(self.book_repo.db.query().filter().date_of_issue.desc()).all())
        
        # Это нужно будет переписать с правильным запросом
        return []
    
    def _convert_to_response_dto(self, book: Book) -> BookResponseDTO:
        """Преобразовать модель книги в DTO ответа"""
        return BookResponseDTO(
            key=book.key,
            title=book.title,
            subtitle=book.subtitle,
            first_publish_date=book.first_publish_date,
            description=book.description,
            authors=[{
                "key": author.key,
                "name": author.name,
                "biography": author.biography,
                "birth_date": author.birth_date,
                "death_date": author.death_date,
                "wikipedia": author.wikipedia
            } for author in book.authors],
            subjects=[{
                "id": subject.id,
                "subject": subject.subject,
                "book_key": subject.book_key
            } for subject in book.subjects],
            covers=[{
                "id": cover.id,
                "cover_file": cover.cover_file,
                "book_key": cover.book_key
            } for cover in book.covers],
            is_available=self.book_repo.is_book_available(book.key)
        )





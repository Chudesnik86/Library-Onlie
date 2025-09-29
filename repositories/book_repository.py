from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional
from models import Book, Author, BookSubject, BookCover, Issue
from .base_repository import BaseRepository


class BookRepository(BaseRepository[Book]):
    """Репозиторий для работы с книгами"""
    
    def __init__(self, db: Session):
        super().__init__(db, Book)
    
    def search_books(self, title: Optional[str] = None, author: Optional[str] = None, 
                    subject: Optional[str] = None, skip: int = 0, limit: int = 50) -> List[Book]:
        """Поиск книг по различным критериям"""
        query = self.db.query(Book)
        
        if title:
            query = query.filter(Book.title.contains(title))
        
        if author:
            query = query.join(Book.authors).filter(Author.name.contains(author))
        
        if subject:
            query = query.join(Book.subjects).filter(BookSubject.subject.contains(subject))
        
        return query.offset(skip).limit(limit).all()
    
    def get_books_count(self, title: Optional[str] = None, author: Optional[str] = None, 
                       subject: Optional[str] = None) -> int:
        """Получить количество книг по критериям поиска"""
        query = self.db.query(Book)
        
        if title:
            query = query.filter(Book.title.contains(title))
        
        if author:
            query = query.join(Book.authors).filter(Author.name.contains(author))
        
        if subject:
            query = query.join(Book.subjects).filter(BookSubject.subject.contains(subject))
        
        return query.count()
    
    def is_book_available(self, book_key: int) -> bool:
        """Проверить доступность книги"""
        active_issue = self.db.query(Issue).filter(
            and_(
                Issue.book_key == book_key,
                Issue.return_date.is_(None)
            )
        ).first()
        return active_issue is None
    
    def get_authors_by_book(self, book_key: int) -> List[Author]:
        """Получить авторов книги"""
        return self.db.query(Author).join(Author.books).filter(Book.key == book_key).all()
    
    def create_with_relations(self, book_data: dict, authors_keys: List[int] = None, 
                            subjects: List[str] = None) -> Book:
        """Создать книгу с авторами и темами"""
        # Определить следующий ключ
        max_key = self.db.query(func.max(Book.key)).scalar() or 0
        new_key = max_key + 1
        
        book_data['key'] = new_key
        db_book = Book(**book_data)
        self.db.add(db_book)
        self.db.flush()
        
        # Добавить авторов
        if authors_keys:
            authors = self.db.query(Author).filter(Author.key.in_(authors_keys)).all()
            for author in authors:
                if author not in db_book.authors:
                    db_book.authors.append(author)
        
        # Добавить темы
        if subjects:
            for subject_text in subjects:
                self.db.add(BookSubject(subject=subject_text, book_key=db_book.key))
        
        self.db.commit()
        self.db.refresh(db_book)
        return db_book
    
    def update_with_relations(self, book_key: int, book_data: dict, 
                            authors_keys: List[int] = None, subjects: List[str] = None) -> Optional[Book]:
        """Обновить книгу с авторами и темами"""
        db_book = self.get_by_key(book_key)
        if not db_book:
            return None
        
        # Обновить основные поля
        for field, value in book_data.items():
            if field not in ['authors_keys', 'subjects']:
                setattr(db_book, field, value)
        
        # Обновить авторов
        if authors_keys is not None:
            db_book.authors.clear()
            if authors_keys:
                authors = self.db.query(Author).filter(Author.key.in_(authors_keys)).all()
                for author in authors:
                    db_book.authors.append(author)
        
        # Обновить темы
        if subjects is not None:
            self.db.query(BookSubject).filter(BookSubject.book_key == book_key).delete()
            for subject_text in subjects:
                self.db.add(BookSubject(subject=subject_text, book_key=book_key))
        
        self.db.commit()
        self.db.refresh(db_book)
        return db_book
    
    def delete_with_relations(self, book_key: int) -> bool:
        """Удалить книгу со всеми связанными данными"""
        db_book = self.get_by_key(book_key)
        if not db_book:
            return False
        
        # Удалить связанные записи
        self.db.query(BookSubject).filter(BookSubject.book_key == book_key).delete()
        self.db.query(BookCover).filter(BookCover.book_key == book_key).delete()
        
        # Очистить связи many-to-many
        db_book.authors.clear()
        
        # Удалить книгу
        self.db.delete(db_book)
        self.db.commit()
        return True





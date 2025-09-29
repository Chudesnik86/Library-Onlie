from sqlalchemy.orm import Session
from typing import List, Optional
from models import Author, Book
from .base_repository import BaseRepository


class AuthorRepository(BaseRepository[Author]):
    """Репозиторий для работы с авторами"""
    
    def __init__(self, db: Session):
        super().__init__(db, Author)
    
    def get_authors_by_book(self, book_key: int) -> List[Author]:
        """Получить авторов книги"""
        return self.db.query(Author).join(Author.books).filter(Book.key == book_key).all()
    
    def search_authors(self, name: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[Author]:
        """Поиск авторов по имени"""
        query = self.db.query(Author)
        
        if name:
            query = query.filter(Author.name.contains(name))
        
        return query.offset(skip).limit(limit).all()
    
    def get_authors_count(self, name: Optional[str] = None) -> int:
        """Получить количество авторов"""
        query = self.db.query(Author)
        
        if name:
            query = query.filter(Author.name.contains(name))
        
        return query.count()





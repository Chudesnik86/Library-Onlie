from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import date, timedelta
from typing import List, Optional
from models import Issue, Book, Customer
from .base_repository import BaseRepository


class IssueRepository(BaseRepository[Issue]):
    """Репозиторий для работы с выдачами книг"""
    
    def __init__(self, db: Session):
        super().__init__(db, Issue)
    
    def get_current_issues_by_customer(self, customer_id: int) -> List[Issue]:
        """Получить текущие выдачи клиента"""
        return self.db.query(Issue).filter(
            and_(
                Issue.customer_id == customer_id,
                Issue.return_date.is_(None)
            )
        ).order_by(Issue.return_until.asc()).all()
    
    def get_issue_history_by_customer(self, customer_id: int) -> List[Issue]:
        """Получить историю выдач клиента"""
        return self.db.query(Issue).filter(
            and_(
                Issue.customer_id == customer_id,
                Issue.return_date.isnot(None)
            )
        ).order_by(Issue.return_date.desc()).all()
    
    def get_book_history(self, book_key: int) -> List[Issue]:
        """Получить историю выдачи книги"""
        return self.db.query(Issue).filter(Issue.book_key == book_key).order_by(Issue.date_of_issue.desc()).all()
    
    def get_overdue_issues(self) -> List[Issue]:
        """Получить просроченные выдачи"""
        today = date.today()
        return self.db.query(Issue).filter(
            and_(
                Issue.return_date.is_(None),
                Issue.return_until < today
            )
        ).order_by(Issue.return_until.asc()).all()
    
    def is_book_available(self, book_key: int) -> bool:
        """Проверить доступность книги"""
        active_issue = self.db.query(Issue).filter(
            and_(
                Issue.book_key == book_key,
                Issue.return_date.is_(None)
            )
        ).first()
        return active_issue is None
    
    def can_customer_borrow(self, customer_id: int) -> bool:
        """Проверить, может ли клиент взять книгу (лимит 5 книг)"""
        active_issues = self.get_current_issues_by_customer(customer_id)
        return len(active_issues) < 5
    
    def create_issue(self, book_key: int, customer_id: int) -> Issue:
        """Создать новую выдачу книги"""
        # Проверить лимит клиента
        if not self.can_customer_borrow(customer_id):
            raise ValueError("Customer has reached the maximum limit of 5 active issues")
        
        # Проверить доступность книги
        if not self.is_book_available(book_key):
            raise ValueError("Book is already checked out")
        
        today = date.today()
        return_date = today + timedelta(days=21)
        
        issue_data = {
            'book_key': book_key,
            'customer_id': customer_id,
            'date_of_issue': today,
            'return_until': return_date,
            'renewed': False
        }
        
        return self.create(issue_data)
    
    def return_book(self, issue_id: int) -> Optional[Issue]:
        """Вернуть книгу"""
        issue = self.get_by_id(issue_id)
        if issue:
            issue.return_date = date.today()
            self.db.commit()
            self.db.refresh(issue)
        return issue
    
    def renew_issue(self, issue_id: int) -> Optional[Issue]:
        """Продлить выдачу книги"""
        issue = self.get_by_id(issue_id)
        if not issue:
            raise ValueError("Issue not found")
        
        if issue.renewed:
            raise ValueError("Book has already been renewed once")
        
        issue.return_until = issue.return_until + timedelta(days=7)
        issue.renewed = True
        self.db.commit()
        self.db.refresh(issue)
        return issue
    
    def get_issue_with_details(self, issue_id: int) -> Optional[Issue]:
        """Получить выдачу с деталями книги и клиента"""
        return self.db.query(Issue).filter(Issue.id == issue_id).first()





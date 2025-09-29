from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional
from repositories import IssueRepository, BookRepository, CustomerRepository
from dto import (
    IssueCreateDTO, IssueResponseDTO, IssueWithBookDTO, IssueWithCustomerDTO,
    IssueRenewResponseDTO, IssueReturnResponseDTO
)
from models import Issue


class IssueService:
    """Сервис для работы с выдачами книг"""
    
    def __init__(self, db: Session):
        self.db = db
        self.issue_repo = IssueRepository(db)
        self.book_repo = BookRepository(db)
        self.customer_repo = CustomerRepository(db)
    
    def get_current_issues_by_customer(self, customer_id: int) -> List[IssueWithBookDTO]:
        """Получить текущие выдачи клиента"""
        issues = self.issue_repo.get_current_issues_by_customer(customer_id)
        
        return [self._convert_to_issue_with_book_dto(issue) for issue in issues]
    
    def get_issue_history_by_customer(self, customer_id: int) -> List[IssueWithBookDTO]:
        """Получить историю выдач клиента"""
        issues = self.issue_repo.get_issue_history_by_customer(customer_id)
        
        return [self._convert_to_issue_with_book_dto(issue) for issue in issues]
    
    def get_book_history(self, book_key: int) -> List[IssueWithCustomerDTO]:
        """Получить историю выдачи книги"""
        issues = self.issue_repo.get_book_history(book_key)
        
        return [self._convert_to_issue_with_customer_dto(issue) for issue in issues]
    
    def get_overdue_issues(self) -> List[IssueWithCustomerDTO]:
        """Получить просроченные выдачи"""
        issues = self.issue_repo.get_overdue_issues()
        
        return [self._convert_to_issue_with_customer_dto(issue) for issue in issues]
    
    def create_issue(self, issue_data: IssueCreateDTO) -> IssueResponseDTO:
        """Создать новую выдачу"""
        issue = self.issue_repo.create_issue(
            book_key=issue_data.book_key,
            customer_id=issue_data.customer_id
        )
        
        return self._convert_to_response_dto(issue)
    
    def return_book(self, issue_id: int) -> IssueReturnResponseDTO:
        """Вернуть книгу"""
        issue = self.issue_repo.return_book(issue_id)
        if not issue:
            raise ValueError("Issue not found")
        
        return IssueReturnResponseDTO(message="Book returned successfully")
    
    def renew_issue(self, issue_id: int) -> IssueRenewResponseDTO:
        """Продлить выдачу"""
        issue = self.issue_repo.renew_issue(issue_id)
        
        return IssueRenewResponseDTO(
            message="Book renewed successfully",
            new_return_date=issue.return_until
        )
    
    def check_book_availability(self, book_key: int) -> bool:
        """Проверить доступность книги"""
        return self.issue_repo.is_book_available(book_key)
    
    def can_customer_borrow(self, customer_id: int) -> bool:
        """Проверить, может ли клиент взять книгу"""
        return self.issue_repo.can_customer_borrow(customer_id)
    
    def _convert_to_response_dto(self, issue: Issue) -> IssueResponseDTO:
        """Преобразовать модель выдачи в DTO ответа"""
        return IssueResponseDTO(
            id=issue.id,
            book_key=issue.book_key,
            customer_id=issue.customer_id,
            date_of_issue=issue.date_of_issue,
            return_until=issue.return_until,
            return_date=issue.return_date,
            renewed=issue.renewed,
            created_at=issue.created_at,
            book={
                "key": issue.book.key,
                "title": issue.book.title,
                "subtitle": issue.book.subtitle
            },
            customer={
                "id": issue.customer.id,
                "name": issue.customer.name
            }
        )
    
    def _convert_to_issue_with_book_dto(self, issue: Issue) -> IssueWithBookDTO:
        """Преобразовать выдачу в DTO с информацией о книге"""
        today = date.today()
        is_overdue = issue.return_until < today and issue.return_date is None
        was_overdue = issue.return_date and issue.return_date > issue.return_until
        
        return IssueWithBookDTO(
            id=issue.id,
            book={
                "key": issue.book.key,
                "title": issue.book.title
            },
            date_of_issue=issue.date_of_issue,
            return_until=issue.return_until,
            return_date=issue.return_date,
            renewed=issue.renewed,
            is_overdue=is_overdue,
            was_overdue=was_overdue
        )
    
    def _convert_to_issue_with_customer_dto(self, issue: Issue) -> IssueWithCustomerDTO:
        """Преобразовать выдачу в DTO с информацией о клиенте"""
        return IssueWithCustomerDTO(
            id=issue.id,
            customer={
                "id": issue.customer.id,
                "name": issue.customer.name
            },
            date_of_issue=issue.date_of_issue,
            return_until=issue.return_until,
            return_date=issue.return_date,
            renewed=issue.renewed
        )





from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from services import IssueService
from dto import (
    IssueCreateDTO, IssueWithBookDTO, IssueWithCustomerDTO,
    IssueRenewResponseDTO, IssueReturnResponseDTO
)
from database import get_db
from auth import verify_token

router = APIRouter(prefix="/issues", tags=["circulation"])


def get_issue_service(db: Session = Depends(get_db)) -> IssueService:
    """Получить сервис выдач"""
    return IssueService(db)


@router.get("/customers/{customer_id}/current", response_model=List[IssueWithBookDTO])
async def get_current_issues(
    customer_id: int,
    issue_service: IssueService = Depends(get_issue_service),
    current_user: str = Depends(verify_token)
):
    """Получить текущие выдачи клиента (требует аутентификации)"""
    return issue_service.get_current_issues_by_customer(customer_id)


@router.get("/customers/{customer_id}/history", response_model=List[IssueWithBookDTO])
async def get_issue_history(
    customer_id: int,
    issue_service: IssueService = Depends(get_issue_service),
    current_user: str = Depends(verify_token)
):
    """Получить историю выдач клиента (требует аутентификации)"""
    return issue_service.get_issue_history_by_customer(customer_id)


@router.get("/books/{book_key}/history", response_model=List[IssueWithCustomerDTO])
async def get_book_history(
    book_key: int,
    issue_service: IssueService = Depends(get_issue_service),
    current_user: str = Depends(verify_token)
):
    """Получить историю выдачи книги (требует аутентификации)"""
    return issue_service.get_book_history(book_key)


@router.get("/overdue", response_model=List[IssueWithCustomerDTO])
async def get_overdue_issues(
    issue_service: IssueService = Depends(get_issue_service),
    current_user: str = Depends(verify_token)
):
    """Получить просроченные выдачи (требует аутентификации)"""
    return issue_service.get_overdue_issues()


@router.post("", response_model=dict)
async def create_issue(
    issue: IssueCreateDTO,
    issue_service: IssueService = Depends(get_issue_service),
    current_user: str = Depends(verify_token)
):
    """Создать новую выдачу (требует аутентификации)"""
    try:
        created_issue = issue_service.create_issue(issue)
        return {"message": "Book issued successfully", "issue_id": created_issue.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{issue_id}/return", response_model=IssueReturnResponseDTO)
async def return_book(
    issue_id: int,
    issue_service: IssueService = Depends(get_issue_service),
    current_user: str = Depends(verify_token)
):
    """Вернуть книгу (требует аутентификации)"""
    try:
        return issue_service.return_book(issue_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{issue_id}/renew", response_model=IssueRenewResponseDTO)
async def renew_issue(
    issue_id: int,
    issue_service: IssueService = Depends(get_issue_service),
    current_user: str = Depends(verify_token)
):
    """Продлить выдачу (требует аутентификации)"""
    try:
        return issue_service.renew_issue(issue_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))





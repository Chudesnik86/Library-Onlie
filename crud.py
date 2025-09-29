from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import date, datetime, timedelta
from typing import List, Optional
from models import Book, Author, BookSubject, BookCover, Customer, Issue
from schemas import BookCreate, AuthorCreate, CustomerCreate, IssueCreate

# Book CRUD operations
def get_books(db: Session, skip: int = 0, limit: int = 50):
    return db.query(Book).offset(skip).limit(limit).all()

def get_book(db: Session, book_key: int):
    return db.query(Book).filter(Book.key == book_key).first()

def create_book(db: Session, payload: BookCreate) -> Book:
    # Determine next key if not provided (for simplicity use max+1)
    max_key = db.query(func.max(Book.key)).scalar() or 0
    new_key = max_key + 1
    db_book = Book(
        key=new_key,
        title=payload.title,
        subtitle=payload.subtitle,
        first_publish_date=payload.first_publish_date,
        description=payload.description,
    )
    db.add(db_book)
    db.flush()

    # Authors
    if payload.authors_keys:
        authors = db.query(Author).filter(Author.key.in_(payload.authors_keys)).all()
        for a in authors:
            if a not in db_book.authors:
                db_book.authors.append(a)

    # Subjects
    if payload.subjects:
        for subject_text in payload.subjects:
            db.add(BookSubject(subject=subject_text, book_key=db_book.key))

    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_key: int, payload: BookCreate) -> Optional[Book]:
    db_book = db.query(Book).filter(Book.key == book_key).first()
    if not db_book:
        return None
    db_book.title = payload.title
    db_book.subtitle = payload.subtitle
    db_book.first_publish_date = payload.first_publish_date
    db_book.description = payload.description

    # Replace authors
    if payload.authors_keys is not None:
        db_book.authors.clear()
        if payload.authors_keys:
            authors = db.query(Author).filter(Author.key.in_(payload.authors_keys)).all()
            for a in authors:
                db_book.authors.append(a)

    # Replace subjects
    if payload.subjects is not None:
        db.query(BookSubject).filter(BookSubject.book_key == db_book.key).delete()
        for subject_text in payload.subjects:
            db.add(BookSubject(subject=subject_text, book_key=db_book.key))

    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_key: int) -> bool:
    db_book = db.query(Book).filter(Book.key == book_key).first()
    if not db_book:
        return False
    # Cascade delete simple related rows (subjects, covers handled by FK if set; do manually for safety)
    db.query(BookSubject).filter(BookSubject.book_key == book_key).delete()
    db.query(BookCover).filter(BookCover.book_key == book_key).delete()
    # Clear m2m
    db_book.authors.clear()
    db.delete(db_book)
    db.commit()
    return True

def search_books(db: Session, title: Optional[str] = None, author: Optional[str] = None, 
                 subject: Optional[str] = None, skip: int = 0, limit: int = 50):
    query = db.query(Book)
    
    if title:
        query = query.filter(Book.title.contains(title))
    
    if author:
        query = query.join(Book.authors).filter(Author.name.contains(author))
    
    if subject:
        query = query.join(Book.subjects).filter(BookSubject.subject.contains(subject))
    
    return query.offset(skip).limit(limit).all()

def get_books_count(db: Session, title: Optional[str] = None, author: Optional[str] = None, 
                   subject: Optional[str] = None):
    query = db.query(Book)
    
    if title:
        query = query.filter(Book.title.contains(title))
    
    if author:
        query = query.join(Book.authors).filter(Author.name.contains(author))
    
    if subject:
        query = query.join(Book.subjects).filter(BookSubject.subject.contains(subject))
    
    return query.count()

# Author CRUD operations
def get_author(db: Session, author_key: int):
    return db.query(Author).filter(Author.key == author_key).first()

def get_authors_by_book(db: Session, book_key: int):
    return db.query(Author).join(Author.books).filter(Book.key == book_key).all()

# Customer CRUD operations
def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer).offset(skip).limit(limit).all()

def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()

def search_customers(db: Session, customer_id: Optional[int] = None, name: Optional[str] = None):
    query = db.query(Customer)
    
    if customer_id:
        query = query.filter(Customer.id == customer_id)
    
    if name:
        query = query.filter(Customer.name.contains(name))
    
    return query.all()

def create_customer(db: Session, customer: CustomerCreate):
    # Generate customer ID starting from C1000
    last_customer = db.query(Customer).order_by(Customer.id.desc()).first()
    new_id = 1000 if not last_customer else last_customer.id + 1
    
    db_customer = Customer(
        id=new_id,
        name=customer.name,
        address=customer.address,
        zip_code=customer.zip_code,
        city=customer.city,
        phone=customer.phone,
        email=customer.email
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: int, customer: CustomerCreate):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if db_customer:
        for key, value in customer.dict().items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer

# Issue CRUD operations
def get_issue(db: Session, issue_id: int):
    return db.query(Issue).filter(Issue.id == issue_id).first()

def get_current_issues_by_customer(db: Session, customer_id: int):
    return db.query(Issue).filter(
        and_(
            Issue.customer_id == customer_id,
            Issue.return_date.is_(None)
        )
    ).order_by(Issue.return_until.asc()).all()

def get_issue_history_by_customer(db: Session, customer_id: int):
    return db.query(Issue).filter(
        and_(
            Issue.customer_id == customer_id,
            Issue.return_date.isnot(None)
        )
    ).order_by(Issue.return_date.desc()).all()

def get_book_history(db: Session, book_key: int):
    return db.query(Issue).filter(Issue.book_key == book_key).order_by(Issue.date_of_issue.desc()).all()

def get_overdue_issues(db: Session):
    today = date.today()
    return db.query(Issue).filter(
        and_(
            Issue.return_date.is_(None),
            Issue.return_until < today
        )
    ).order_by(Issue.return_until.asc()).all()

def create_issue(db: Session, issue: IssueCreate):
    # Check if customer has more than 5 active issues
    active_issues = get_current_issues_by_customer(db, issue.customer_id)
    if len(active_issues) >= 5:
        raise ValueError("Customer has reached the maximum limit of 5 active issues")
    
    # Check if book is available
    book_issues = db.query(Issue).filter(
        and_(
            Issue.book_key == issue.book_key,
            Issue.return_date.is_(None)
        )
    ).first()
    
    if book_issues:
        raise ValueError("Book is already checked out")
    
    today = date.today()
    return_date = today + timedelta(days=21)
    
    db_issue = Issue(
        book_key=issue.book_key,
        customer_id=issue.customer_id,
        date_of_issue=today,
        return_until=return_date,
        renewed=False
    )
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue

def return_book(db: Session, issue_id: int):
    db_issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if db_issue:
        db_issue.return_date = date.today()
        db.commit()
        db.refresh(db_issue)
    return db_issue

def renew_issue(db: Session, issue_id: int):
    db_issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not db_issue:
        raise ValueError("Issue not found")
    
    if db_issue.renewed:
        raise ValueError("Book has already been renewed once")
    
    db_issue.return_until = db_issue.return_until + timedelta(days=7)
    db_issue.renewed = True
    db.commit()
    db.refresh(db_issue)
    return db_issue

def is_book_available(db: Session, book_key: int):
    active_issue = db.query(Issue).filter(
        and_(
            Issue.book_key == book_key,
            Issue.return_date.is_(None)
        )
    ).first()
    return active_issue is None


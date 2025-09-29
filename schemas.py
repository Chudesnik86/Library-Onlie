from __future__ import annotations
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import List, Optional

# Book schemas
class BookBase(BaseModel):
    title: str
    subtitle: Optional[str] = None
    first_publish_date: Optional[date] = None
    description: Optional[str] = None

class BookCreate(BookBase):
    authors_keys: Optional[List[int]] = None
    subjects: Optional[List[str]] = None

class Book(BookBase):
    key: int
    authors: List["Author"] = Field(default_factory=list)
    subjects: List["BookSubject"] = Field(default_factory=list)
    covers: List["BookCover"] = Field(default_factory=list)
    
    class Config:
        from_attributes = True

class BookWithStatus(Book):
    is_available: bool = True

# Author schemas
class AuthorBase(BaseModel):
    name: str
    biography: Optional[str] = None
    birth_date: Optional[date] = None
    death_date: Optional[date] = None
    wikipedia: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    key: int
    
    class Config:
        from_attributes = True

# Book Cover schemas
class BookCoverBase(BaseModel):
    cover_file: str

class BookCoverCreate(BookCoverBase):
    book_key: int

class BookCover(BookCoverBase):
    id: int
    book_key: int
    
    class Config:
        from_attributes = True

# Book Subject schemas
class BookSubjectBase(BaseModel):
    subject: str

class BookSubjectCreate(BookSubjectBase):
    book_key: int

class BookSubject(BookSubjectBase):
    id: int
    book_key: int
    
    class Config:
        from_attributes = True

# Customer schemas
class CustomerBase(BaseModel):
    name: str
    address: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    issues: List["Issue"] = Field(default_factory=list)
    
    class Config:
        from_attributes = True

# Issue schemas
class IssueBase(BaseModel):
    book_key: int
    customer_id: int
    date_of_issue: date
    return_until: date
    renewed: bool = False

class IssueCreate(BaseModel):
    book_key: int
    customer_id: int

class IssueReturn(BaseModel):
    issue_id: int

class Issue(IssueBase):
    id: int
    return_date: Optional[date] = None
    created_at: datetime
    book: Book
    customer: Customer
    
    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

# Search schemas
class BookSearch(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None
    page: int = 1
    limit: int = 50

class CustomerSearch(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

# Pagination schema
class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    limit: int
    total_pages: int

# Update the forward references
Book.model_rebuild()
Author.model_rebuild()
Customer.model_rebuild()
Issue.model_rebuild()


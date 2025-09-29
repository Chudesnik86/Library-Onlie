from sqlalchemy import Column, Integer, String, DateTime, Date, Text, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# Association table for many-to-many relationship between books and authors
book_authors = Table(
    'book_authors',
    Base.metadata,
    Column('book_key', Integer, ForeignKey('books.key'), primary_key=True),
    Column('author_key', Integer, ForeignKey('authors.key'), primary_key=True)
)

class Book(Base):
    __tablename__ = "books"
    
    key = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    subtitle = Column(String(255))
    first_publish_date = Column(Date)
    description = Column(Text)
    
    # Relationships
    authors = relationship("Author", secondary=book_authors, back_populates="books")
    covers = relationship("BookCover", back_populates="book")
    subjects = relationship("BookSubject", back_populates="book")
    issues = relationship("Issue", back_populates="book")

class BookCover(Base):
    __tablename__ = "book_covers"
    
    id = Column(Integer, primary_key=True, index=True)
    cover_file = Column(String(255), nullable=False)
    book_key = Column(Integer, ForeignKey("books.key"))
    
    # Relationship
    book = relationship("Book", back_populates="covers")

class BookSubject(Base):
    __tablename__ = "book_subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(255), nullable=False)
    book_key = Column(Integer, ForeignKey("books.key"))
    
    # Relationship
    book = relationship("Book", back_populates="subjects")

class Author(Base):
    __tablename__ = "authors"
    
    key = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    biography = Column(Text)
    birth_date = Column(Date)
    death_date = Column(Date)
    wikipedia = Column(String(500))
    
    # Relationships
    books = relationship("Book", secondary=book_authors, back_populates="authors")

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String(500))
    zip_code = Column(String(20))
    city = Column(String(100))
    phone = Column(String(50))
    email = Column(String(255))
    
    # Relationships
    issues = relationship("Issue", back_populates="customer")

class Issue(Base):
    __tablename__ = "issues"
    
    id = Column(Integer, primary_key=True, index=True)
    book_key = Column(Integer, ForeignKey("books.key"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    date_of_issue = Column(Date, nullable=False)
    return_until = Column(Date, nullable=False)
    return_date = Column(Date)
    renewed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    book = relationship("Book", back_populates="issues")
    customer = relationship("Customer", back_populates="issues")


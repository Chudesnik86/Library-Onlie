from sqlalchemy.orm import Session
from datetime import date
from database import SessionLocal, engine
from models import Base, Book, Author, BookSubject, BookCover, Customer, Issue

# Create tables
Base.metadata.create_all(bind=engine)

def create_sample_data():
    db = SessionLocal()
    
    try:
        # Create authors (with additional authors)
        authors_data = [
            {"key": 1, "name": "F. Scott Fitzgerald", "birth_date": date(1896, 9, 24), "death_date": date(1940, 12, 21), "biography": "American novelist and short story writer"},
            {"key": 2, "name": "Harper Lee", "birth_date": date(1926, 4, 28), "death_date": date(2016, 2, 19), "biography": "American novelist"},
            {"key": 3, "name": "George Orwell", "birth_date": date(1903, 6, 25), "death_date": date(1950, 1, 21), "biography": "English novelist, essayist, journalist, and critic"},
            {"key": 4, "name": "Jane Austen", "birth_date": date(1775, 12, 16), "death_date": date(1817, 7, 18), "biography": "English novelist"},
            {"key": 5, "name": "J.D. Salinger", "birth_date": date(1919, 1, 1), "death_date": date(2010, 1, 27), "biography": "American writer"},
            {"key": 6, "name": "J.R.R. Tolkien", "birth_date": date(1892, 1, 3), "death_date": date(1973, 9, 2), "biography": "English writer, poet, philologist"},
            {"key": 7, "name": "J.K. Rowling", "birth_date": date(1965, 7, 31), "biography": "British author and philanthropist"},
            {"key": 8, "name": "Fyodor Dostoevsky", "birth_date": date(1821, 11, 11), "death_date": date(1881, 2, 9), "biography": "Russian novelist and philosopher"},
            {"key": 9, "name": "Leo Tolstoy", "birth_date": date(1828, 9, 9), "death_date": date(1910, 11, 20), "biography": "Russian writer"},
        ]

        for author_data in authors_data:
            if not db.query(Author).filter(Author.key == author_data["key"]).first():
                db.add(Author(**author_data))

        # Create books (with additional books)
        books_data = [
            {"key": 1, "title": "The Great Gatsby", "subtitle": "A Novel", "first_publish_date": date(1925, 4, 10), "description": "The story of the fabulously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan."},
            {"key": 2, "title": "To Kill a Mockingbird", "subtitle": "", "first_publish_date": date(1960, 7, 11), "description": "The story of young Scout Finch, whose father defends a Black man falsely accused of rape."},
            {"key": 3, "title": "1984", "subtitle": "A Novel", "first_publish_date": date(1949, 6, 8), "description": "A dystopian social science fiction novel about totalitarian control and surveillance."},
            {"key": 4, "title": "Pride and Prejudice", "subtitle": "", "first_publish_date": date(1813, 1, 28), "description": "The story follows the character development of Elizabeth Bennet."},
            {"key": 5, "title": "The Catcher in the Rye", "subtitle": "", "first_publish_date": date(1951, 7, 16), "description": "A story about teenage rebellion and alienation."},
            {"key": 6, "title": "The Hobbit", "subtitle": "There and Back Again", "first_publish_date": date(1937, 9, 21), "description": "Bilbo Baggins embarks on a quest to win a share of the treasure guarded by Smaug the dragon."},
            {"key": 7, "title": "Harry Potter and the Philosopher's Stone", "subtitle": "", "first_publish_date": date(1997, 6, 26), "description": "Harry discovers he is a wizard on his 11th birthday."},
            {"key": 8, "title": "Crime and Punishment", "subtitle": "", "first_publish_date": date(1866, 1, 1), "description": "Raskolnikov wrestles with guilt after committing a crime."},
            {"key": 9, "title": "War and Peace", "subtitle": "", "first_publish_date": date(1869, 1, 1), "description": "A chronicle of Napoleon's invasion of Russia and its impact."},
        ]

        for book_data in books_data:
            if not db.query(Book).filter(Book.key == book_data["key"]).first():
                db.add(Book(**book_data))

        # Create book subjects
        subjects_data = [
            {"id": 1, "subject": "Fiction", "book_key": 1},
            {"id": 2, "subject": "American Literature", "book_key": 1},
            {"id": 3, "subject": "Fiction", "book_key": 2},
            {"id": 4, "subject": "American Literature", "book_key": 2},
            {"id": 5, "subject": "Dystopian Fiction", "book_key": 3},
            {"id": 6, "subject": "Science Fiction", "book_key": 3},
            {"id": 7, "subject": "Romance", "book_key": 4},
            {"id": 8, "subject": "British Literature", "book_key": 4},
            {"id": 9, "subject": "Coming of Age", "book_key": 5},
            {"id": 10, "subject": "American Literature", "book_key": 5},
            {"id": 11, "subject": "Fantasy", "book_key": 6},
            {"id": 12, "subject": "Adventure", "book_key": 6},
            {"id": 13, "subject": "Fantasy", "book_key": 7},
            {"id": 14, "subject": "Young Adult", "book_key": 7},
            {"id": 15, "subject": "Classic", "book_key": 8},
            {"id": 16, "subject": "Philosophical Fiction", "book_key": 8},
            {"id": 17, "subject": "Historical", "book_key": 9},
            {"id": 18, "subject": "Classic", "book_key": 9},
        ]

        for subject_data in subjects_data:
            if not db.query(BookSubject).filter(BookSubject.id == subject_data["id"]).first():
                db.add(BookSubject(**subject_data))

        # Create book covers
        covers_data = [
            {"id": 1, "cover_file": "great_gatsby_1", "book_key": 1},
            {"id": 2, "cover_file": "mockingbird_1", "book_key": 2},
            {"id": 3, "cover_file": "1984_1", "book_key": 3},
            {"id": 4, "cover_file": "pride_prejudice_1", "book_key": 4},
            {"id": 5, "cover_file": "catcher_rye_1", "book_key": 5},
            {"id": 6, "cover_file": "hobbit_1", "book_key": 6},
            {"id": 7, "cover_file": "hp_philosopher_stone_1", "book_key": 7},
            {"id": 8, "cover_file": "crime_punishment_1", "book_key": 8},
            {"id": 9, "cover_file": "war_and_peace_1", "book_key": 9},
        ]

        for cover_data in covers_data:
            if not db.query(BookCover).filter(BookCover.id == cover_data["id"]).first():
                db.add(BookCover(**cover_data))
        
        # Create customers
        customers_data = [
            {
                "id": 1001,
                "name": "John Smith",
                "address": "123 Main St",
                "zip_code": "12345",
                "city": "New York",
                "phone": "555-0123",
                "email": "john.smith@email.com"
            },
            {
                "id": 1002,
                "name": "Sarah Johnson",
                "address": "456 Oak Ave",
                "zip_code": "67890",
                "city": "Boston",
                "phone": "555-0456",
                "email": "sarah.johnson@email.com"
            },
            {
                "id": 1003,
                "name": "Michael Brown",
                "address": "789 Pine St",
                "zip_code": "11111",
                "city": "Chicago",
                "phone": "555-0789",
                "email": "michael.brown@email.com"
            },
        ]
        
        for customer_data in customers_data:
            if not db.query(Customer).filter(Customer.id == customer_data["id"]).first():
                db.add(Customer(**customer_data))
        
        # Create some sample issues
        from datetime import timedelta
        issues_data = [
            {
                "id": 1,
                "book_key": 2,
                "customer_id": 1001,
                "date_of_issue": date.today() - timedelta(days=10),
                "return_until": date.today() + timedelta(days=11),
                "renewed": False
            },
            {
                "id": 2,
                "book_key": 5,
                "customer_id": 1002,
                "date_of_issue": date.today() - timedelta(days=25),
                "return_until": date.today() - timedelta(days=4),  # Overdue
                "renewed": False
            },
            {
                "id": 3,
                "book_key": 1,
                "customer_id": 1001,
                "date_of_issue": date.today() - timedelta(days=30),
                "return_date": date.today() - timedelta(days=9),
                "return_until": date.today() - timedelta(days=9),
                "renewed": False
            },
        ]
        
        for issue_data in issues_data:
            if not db.query(Issue).filter(Issue.id == issue_data["id"]).first():
                db.add(Issue(**issue_data))
        
        # Create book-author associations
        book_authors_data = [
            {"book_key": 1, "author_key": 1},  # The Great Gatsby - F. Scott Fitzgerald
            {"book_key": 2, "author_key": 2},  # To Kill a Mockingbird - Harper Lee
            {"book_key": 3, "author_key": 3},  # 1984 - George Orwell
            {"book_key": 4, "author_key": 4},  # Pride and Prejudice - Jane Austen
            {"book_key": 5, "author_key": 5},  # The Catcher in the Rye - J.D. Salinger
            {"book_key": 6, "author_key": 6},  # The Hobbit - J.R.R. Tolkien
            {"book_key": 7, "author_key": 7},  # HP1 - J.K. Rowling
            {"book_key": 8, "author_key": 8},  # Crime and Punishment - Dostoevsky
            {"book_key": 9, "author_key": 9},  # War and Peace - Tolstoy
        ]
        
        for ba_data in book_authors_data:
            # Add the association using the many-to-many relationship
            book = db.query(Book).filter(Book.key == ba_data["book_key"]).first()
            author = db.query(Author).filter(Author.key == ba_data["author_key"]).first()
            if book and author:
                if author not in book.authors:
                    book.authors.append(author)
        
        db.commit()
        print("Sample data created successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error creating sample data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()


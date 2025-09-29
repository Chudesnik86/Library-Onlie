#!/usr/bin/env python3
"""
Database initialization script for Bookmaster3000
This script creates the database tables and can be run independently
"""
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from models import Base
from config import DATABASE_URL

def create_database():
    """Create database tables"""
    try:
        print("🔄 Creating database tables...")
        
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        print("✅ Database tables created successfully!")
        return True
        
    except OperationalError as e:
        print(f"❌ Database connection failed: {e}")
        print("\n💡 Make sure MySQL is running and the database exists.")
        print("   You can create the database with:")
        print("   mysql -u root -p -e 'CREATE DATABASE bookmaster3000;'")
        return False
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def main():
    """Main function"""
    print("🗄️  Bookmaster3000 Database Initialization")
    print("=" * 50)
    
    if create_database():
        print("\n🎉 Database initialization completed!")
        print("\n📋 Next steps:")
        print("1. Run 'python seed_data.py' to add sample data")
        print("2. Start the server with 'python run.py'")
    else:
        print("\n❌ Database initialization failed!")
        print("Please check your MySQL connection and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()









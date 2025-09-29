from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from models import Customer
from .base_repository import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    """Репозиторий для работы с клиентами"""
    
    def __init__(self, db: Session):
        super().__init__(db, Customer)
    
    def search_customers(self, customer_id: Optional[int] = None, name: Optional[str] = None) -> List[Customer]:
        """Поиск клиентов по ID или имени"""
        query = self.db.query(Customer)
        
        if customer_id:
            query = query.filter(Customer.id == customer_id)
        
        if name:
            query = query.filter(Customer.name.contains(name))
        
        return query.all()
    
    def create_customer(self, customer_data: dict) -> Customer:
        """Создать нового клиента с автоматической генерацией ID"""
        # Генерировать ID клиента начиная с C1000
        last_customer = self.db.query(Customer).order_by(Customer.id.desc()).first()
        new_id = 1000 if not last_customer else last_customer.id + 1
        
        customer_data['id'] = new_id
        return self.create(customer_data)
    
    def get_customers_with_pagination(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        """Получить клиентов с пагинацией"""
        return self.get_all(skip, limit)





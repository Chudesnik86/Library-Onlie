from sqlalchemy.orm import Session
from typing import List, Optional
from repositories import CustomerRepository
from dto import CustomerCreateDTO, CustomerUpdateDTO, CustomerResponseDTO, CustomerSearchDTO, CustomerListResponseDTO
from models import Customer


class CustomerService:
    """Сервис для работы с клиентами"""
    
    def __init__(self, db: Session):
        self.db = db
        self.customer_repo = CustomerRepository(db)
    
    def get_customers(self, search_params: CustomerSearchDTO) -> List[CustomerResponseDTO]:
        """Получить список клиентов с поиском"""
        customers = self.customer_repo.search_customers(
            customer_id=search_params.customer_id,
            name=search_params.name
        )
        
        return [self._convert_to_response_dto(customer) for customer in customers]
    
    def get_customer(self, customer_id: int) -> Optional[CustomerResponseDTO]:
        """Получить клиента по ID"""
        customer = self.customer_repo.get_by_id(customer_id)
        if not customer:
            return None
        
        return self._convert_to_response_dto(customer)
    
    def create_customer(self, customer_data: CustomerCreateDTO) -> CustomerResponseDTO:
        """Создать нового клиента"""
        customer_dict = customer_data.dict()
        customer = self.customer_repo.create_customer(customer_dict)
        
        return self._convert_to_response_dto(customer)
    
    def update_customer(self, customer_id: int, customer_data: CustomerUpdateDTO) -> Optional[CustomerResponseDTO]:
        """Обновить клиента"""
        customer = self.customer_repo.get_by_id(customer_id)
        if not customer:
            return None
        
        customer_dict = customer_data.dict()
        updated_customer = self.customer_repo.update(customer, customer_dict)
        
        return self._convert_to_response_dto(updated_customer)
    
    def delete_customer(self, customer_id: int) -> bool:
        """Удалить клиента"""
        return self.customer_repo.delete(customer_id)
    
    def _convert_to_response_dto(self, customer: Customer) -> CustomerResponseDTO:
        """Преобразовать модель клиента в DTO ответа"""
        return CustomerResponseDTO(
            id=customer.id,
            name=customer.name,
            address=customer.address,
            zip_code=customer.zip_code,
            city=customer.city,
            phone=customer.phone,
            email=customer.email,
            issues=[]  # Пока не загружаем выдачи для простоты
        )





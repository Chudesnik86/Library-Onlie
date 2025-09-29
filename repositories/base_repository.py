from sqlalchemy.orm import Session
from typing import TypeVar, Generic, Type, Optional, List, Any
from sqlalchemy import func

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """Базовый репозиторий для работы с базой данных"""
    
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model
    
    def get_by_id(self, id: Any) -> Optional[T]:
        """Получить объект по ID"""
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_by_key(self, key: Any) -> Optional[T]:
        """Получить объект по ключу (для моделей с key полем)"""
        return self.db.query(self.model).filter(self.model.key == key).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Получить все объекты с пагинацией"""
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def count(self) -> int:
        """Получить общее количество объектов"""
        return self.db.query(self.model).count()
    
    def create(self, obj_in: dict) -> T:
        """Создать новый объект"""
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update(self, db_obj: T, obj_in: dict) -> T:
        """Обновить существующий объект"""
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, id: Any) -> bool:
        """Удалить объект по ID"""
        obj = self.get_by_id(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False
    
    def delete_by_key(self, key: Any) -> bool:
        """Удалить объект по ключу"""
        obj = self.get_by_key(key)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False





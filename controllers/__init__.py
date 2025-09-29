# Controllers package
from .auth_controller import router as auth_router
from .book_controller import router as book_router
from .customer_controller import router as customer_router
from .issue_controller import router as issue_router

__all__ = [
    "auth_router",
    "book_router", 
    "customer_router",
    "issue_router"
]

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import Base
from controllers import auth_router, book_router, customer_router, issue_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bookmaster3000 API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(book_router)
app.include_router(customer_router)
app.include_router(issue_router)

@app.get("/")
async def root():
    """Корневой endpoint"""
    return {"message": "Bookmaster3000 API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Проверка здоровья API"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

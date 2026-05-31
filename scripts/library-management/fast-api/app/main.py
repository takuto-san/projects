from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
from schema import BookResponse, BorrowingRequest, BorrowingResponse
from service import borrow_books, return_books
from cruds import get_user_by_id, get_book_by_id, get_borrowing_by_id, get_borrowings_by_user
from db import SQLALCHEMY_DATABASE_URL, engine, SessionLocal, get_db
from seed import seed_data
from models import User, Book, Borrowing

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()

    yield
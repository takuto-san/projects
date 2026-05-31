from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from models import Base, User, Book, Borrowing
from schema import BookResponse, BorrowingRequest, BorrowingResponse
from cruds import get_user_by_id, get_book_by_id, get_borrowing_by_id, get_borrowings_by_user
from db import SQLALCHEMY_DATABASE_URL, engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends

# service（ロジック）

# 貸出処理
def borrow_books(db: Session, user_id: int, book_ids: List[int]):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    created_borrowings = []
    
    for book_id in book_ids:
        book = get_book_by_id(db, book_id)
        if not book:
            raise HTTPException(status_code=404, detail=f"Book ID:{book_id} not found")
        
        if book.available_copies <= 0:
            raise HTTPException(status_code=400, detail=f"『{book.title}』is not available for borrowing")

        book.available_copies -= 1

        new_borrowing = Borrowing(user_id=user_id, book_id=book_id)
        
        db.add(new_borrowing)
        created_borrowings.append(new_borrowing)

    db.commit()

    for borrowing in created_borrowings:
        db.refresh(borrowing)

    return created_borrowings


# 返却処理
def return_books(db: Session, borrowing_id: int):
    borrowing = get_borrowing_by_id(db, borrowing_id)
    if not borrowing:
        raise HTTPException(status_code=404, detail="Borrowing record not found")
    
    if borrowing.return_date is not None:
        raise HTTPException(status_code=400, detail="This book has already been returned")

    borrowing.return_date = datetime.now()

    if borrowing.book:
        borrowing.book.available_copies += 1

    db.commit()
    db.refresh(borrowing)

    return borrowing
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

# dto（スキーマ）

# # 会員
# class UserResponse(BaseModel):
#     id: int
#     name: str

# 本（在庫）
class BookResponse(BaseModel):
    id: int
    isbn: Optional[str]
    title: str
    total_copies: int
    available_copies: int

# class BookUpdateRequest(BaseModel):
#     total_copies: int
#     available_copies: int

# class BookUpdateResponse(BaseModel):
#     id: int
#     isbn: Optional[str]
#     title: str
#     total_copies: int
#     available_copies: int

# 貸出
class BorrowingRequest(BaseModel):
    book_ids: List[str]

class BorrowingResponse(BaseModel):
    id: int
    user_id: int
    borrow_date: datetime
    return_date: Optional[datetime]
    book: BookResponse
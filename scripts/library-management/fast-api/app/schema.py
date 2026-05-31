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

# 本
class BookResponse(BaseModel):
    id: int
    isbn: Optional[str]
    title: str

    class Config:
            from_attributes = True
# 在庫
class ItemResponse(BaseModel):
    id: int
    book_id: int
    book: BookResponse

    class Config:
        from_attributes = True

# 貸出
class BorrowingRequest(BaseModel):
    item_ids: List[str]

class BorrowingResponse(BaseModel):
    id: int
    user_id: int
    borrow_date: datetime
    return_date: Optional[datetime]
    item: ItemResponse

# class BookUpdateRequest(BaseModel):
#     total_copies: int
#     available_copies: int

# class BookUpdateResponse(BaseModel):
#     id: int
#     isbn: Optional[str]
#     title: str
#     total_copies: int
#     available_copies: int
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine,Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""""""""""""""
   controller
"""""""""""""""
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


# controller（API）

# # ユーザー登録情報（取得）
# @app.get("/users/{user_id}", response_model=UserResponse)
# def get_user(user_id: int):
#     return {"id": user_id, "name": "テストユーザー"}

# # ユーザー貸出情報（取得）
# @app.get("/users/{user_id}/borrowings", response_model=List[BorrowingResponse])
# def get_user_borrowings(user_id: int):
#     return [
#         {
#           "id": 1001,
#           "user_id": user_id,
#           "borrow_date": datetime.now(),
#           "return_date": None,
#           "book": {
#             "id": 1,
#             "isbn": "978-4-7741-9717-8",
#             "title": "ワンピース 1話",
#             "total_copies": 3,
#             "available_copies": 2
#           }
#         }
#     ]

# 貸出処理（登録）
@app.post("/users/{user_id}/borrowing")
def create_borrowing(user_id: str, request: BorrowingRequest):
    print(f"ユーザーID: {user_id}")
    print(f"受け取った本のIDリスト: {request.book_ids}")

    return {
        "message": "登録完了しました！",
        "user_id": user_id,
        "registered_books": request.book_ids
    }

# # 返却処理
# @app.patch("/borrowings/{borrowing_id}", response_model=BorrowingResponse)
# def return_book(borrowing_id: int):
#     return {
#         "id": borrowing_id,
#         "user_id": 1,
#         "borrow_date": datetime.now(),
#         "return_date": datetime.now(),
#         "book": {
#             "id": 1,
#             "isbn": "978-4-7741-9717-8",
#             "title": "ワンピース 1話",
#             "total_copies": 3,
#             "available_copies": 2 
#         }
#     }


# # 在庫（取得）
# @app.get("/books/{book_id}", response_model=BookResponse)
# def get_book(book_id: int):
#     return {
#         "id": book_id,
#         "isbn": "978-4-7741-9717-9",
#         "title": "ワンピース 1話",
#         "total_copies": 3,
#         "available_copies": 2
#     }

# # 在庫（更新）
# @app.patch("/books/{book_id}", response_model=BookUpdateResponse)
# def patch_book(book_id: int, request: BookUpdateRequest):
#     return {
#         "id": book_id,
#         "isbn": "978-4-7741-9717-9",
#         "title": "ワンピース 1話",
#         "total_copies": request.total_copies,
#         "available_copies": request.available_copies
#     }


# """""""""""""""
#     service
# """""""""""""""
# # service（ロジック）

# # 貸出処理
# def borrow_books(db: Session, user_id: int, book_ids: List[int]):
#     user = get_user_by_id(db, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     created_borrowings = []
    
#     for book_id in book_ids:
#         book = get_book_by_id(db, book_id)
#         if not book:
#             raise HTTPException(status_code=404, detail=f"Book ID:{book_id} not found")
        
#         if book.available_copies <= 0:
#             raise HTTPException(status_code=400, detail=f"『{book.title}』is not available for borrowing")

#         book.available_copies -= 1

#         new_borrowing = Borrowing(user_id=user_id, book_id=book_id)
        
#         db.add(new_borrowing)
#         created_borrowings.append(new_borrowing)

#     db.commit()

#     for borrowing in created_borrowings:
#         db.refresh(borrowing)

#     return created_borrowings


# # 返却処理
# def return_books(db: Session, borrowing_id: int):
#     borrowing = get_borrowing_by_id(db, borrowing_id)
#     if not borrowing:
#         raise HTTPException(status_code=404, detail="Borrowing record not found")
    
#     if borrowing.return_date is not None:
#         raise HTTPException(status_code=400, detail="This book has already been returned")

#     borrowing.return_date = datetime.now()

#     if borrowing.book:
#         borrowing.book.available_copies += 1

#     db.commit()
#     db.refresh(borrowing)

#     return borrowing


# # repository（SQL）
# def get_user_by_id(db: Session, user_id: int):
#     return db.query(User).filter(User.id == user_id).first()

# def get_book_by_id(db: Session, book_id: int):
#     return db.query(Book).filter(Book.id == book_id).first()

# def get_borrowing_by_id(db: Session, borrowing_id: int):
#     return db.query(Borrowing).filter(Borrowing.id == borrowing_id).first()

# def get_borrowings_by_user(db: Session, user_id: int):
#     return db.query(Borrowing).filter(Borrowing.user_id == user_id).all()

# アプリ起動時のイベント
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    
    # 【テスト用】もし本が1冊もなければ、初期データを自動投入する
    db = SessionLocal()
    if db.query(Book).count() == 0:
        test_user = User(id=1, name="テストユーザー")
        test_book1 = Book(id=1, isbn="978-4-7741-9717-8", title="ワンピース 1話", total_copies=3, available_copies=3)
        test_book2 = Book(id=2, isbn="978-4-7741-9717-9", title="ワンピース 2話", total_copies=3, available_copies=0) # 在庫0のテスト用
        db.add(test_user)
        db.add(test_book1)
        db.add(test_book2)
        db.commit()
    db.close()

SQLALCHEMY_DATABASE_URL = "sqlite:///./local.db"

engine = create_engine(
    # SQLite特有の設定：複数のスレッドからアクセスできるようにする
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# APIがデータベースを利用するための「クッション」となる関数
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
        
"""""""""""""""
     model
"""""""""""""""
# model（DB）
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    borrowings = relationship("Borrowing", back_populates="user")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String, unique=True, index=True, nullable=True)
    title = Column(String, nullable=False)
    
    borrowings = relationship("Borrowing", back_populates="book")

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    total_copies = Column(Integer, default=1, nullable=False)
    available_copies = Column(Integer, default=1, nullable=False)

    book = relationship("Book", back_populates="items")

class Borrowing(Base):
    __tablename__ = "borrowings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    
    borrow_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    return_date = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="borrowings")
    book = relationship("Book", back_populates="borrowings")
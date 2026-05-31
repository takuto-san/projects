from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine,Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# ==========================================
# 1. SQLite データベースの接続設定 (追加)
# ==========================================
SQLALCHEMY_DATABASE_URL = "sqlite:///./local.db"  # フォルダ内に local.db というファイルが作られます

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
    
    total_copies = Column(Integer, default=1, nullable=False)
    available_copies = Column(Integer, default=1, nullable=False)

    borrowings = relationship("Borrowing", back_populates="book")

class Borrowing(Base):
    __tablename__ = "borrowings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    
    # 修正：レコードが作成された時に、自動で現在時刻が入るように default を追加
    borrow_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    return_date = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="borrowings")
    book = relationship("Book", back_populates="borrowings")

app = FastAPI()

"""""""""""""""
   controller
"""""""""""""""
# dto（スキーマ）

# 会員
class UserResponse(BaseModel):
    id: int
    name: str

# 本（在庫）
class BookResponse(BaseModel):
    id: int
    isbn: Optional[str]
    title: str
    total_copies: int
    available_copies: int

class BookUpdateRequest(BaseModel):
    total_copies: int
    available_copies: int

class BookUpdateResponse(BaseModel):
    id: int
    isbn: Optional[str]
    title: str
    total_copies: int
    available_copies: int

# 貸出
class BorrowingRequest(BaseModel):
    book_ids: List[int]

class BorrowingResponse(BaseModel):
    id: int
    user_id: int
    borrow_date: datetime
    return_date: Optional[datetime]
    book: BookResponse


# controller（API）

# ユーザー登録情報（取得）
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return user

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
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ユーザー貸出情報（登録）
# @app.post("/users/{user_id}/borrowings", response_model=List[BorrowingResponse])
# def create_user_borrowings(user_id: int, request: BorrowingRequest):
#     return [
#         {
#             "id": 1000 + b_id,
#             "user_id": user_id,
#             "borrow_date": datetime.now(),
#             "return_date": None,
#             "book": {
#                 "id": b_id,
#                 "isbn": f"978-4-7741-9717-{b_id}",
#                 "title": f"ワンピース {b_id}話",
#                 "total_copies": 3,
#                 "available_copies": 1 
#             }
#         } for b_id in request.book_ids
#     ]
# ユーザー貸出情報（登録） ★本物の貸出処理に修正
@app.post("/users/{user_id}/borrowings", response_model=List[BorrowingResponse])
def create_user_borrowings(user_id: int, request: BorrowingRequest, db: Session = Depends(get_db)):
    # 以前作った Service 層の borrow_books ロジックをここで呼び出す！
    return borrow_books(db=db, user_id=user_id, book_ids=request.book_ids)


# 返却処理
@app.patch("/borrowings/{borrowing_id}", response_model=BorrowingResponse)
def return_book(borrowing_id: int):
    return {
        "id": borrowing_id,
        "user_id": 1,
        "borrow_date": datetime.now(),
        "return_date": datetime.now(),
        "book": {
            "id": 1,
            "isbn": "978-4-7741-9717-8",
            "title": "ワンピース 1話",
            "total_copies": 3,
            "available_copies": 2 
        }
    }


# 在庫（取得）
@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    return {
        "id": book_id,
        "isbn": "978-4-7741-9717-9",
        "title": "ワンピース 1話",
        "total_copies": 3,
        "available_copies": 2
    }

# 在庫（更新）
@app.patch("/books/{book_id}", response_model=BookUpdateResponse)
def patch_book(book_id: int, request: BookUpdateRequest):
    return {
        "id": book_id,
        "isbn": "978-4-7741-9717-9",
        "title": "ワンピース 1話",
        "total_copies": request.total_copies,
        "available_copies": request.available_copies
    }

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


"""""""""""""""
    service
"""""""""""""""
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


# repository（SQL）
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_book_by_id(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def get_borrowing_by_id(db: Session, borrowing_id: int):
    return db.query(Borrowing).filter(Borrowing.id == borrowing_id).first()

def get_borrowings_by_user(db: Session, user_id: int):
    return db.query(Borrowing).filter(Borrowing.user_id == user_id).all()



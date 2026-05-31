from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from db import engine, SessionLocal
from models import Base
from seed import seed_data
from db import get_db
from schema import BorrowingRequest, BorrowingResponse
import service

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# controller（APIエンドポイント）
@app.post("/users/{email}/borrowings", response_model=list[BorrowingResponse])
def borrow_books(email: str, request: BorrowingRequest, db: Session = Depends(get_db)):
    borrowings = service.borrow_books(db, email, request.item_ids)
    return borrowings


@app.patch("/borrowings/{borrowing_id}", response_model=BorrowingResponse)
def return_book(borrowing_id: int, db: Session = Depends(get_db)):
    borrowing = service.process_return_book(db, borrowing_id)
    return borrowing


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
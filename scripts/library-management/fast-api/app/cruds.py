from sqlalchemy.orm import Session
from models import User, Book, Borrowing

# repository（SQL）
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_book_by_id(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def get_borrowing_by_id(db: Session, borrowing_id: int):
    return db.query(Borrowing).filter(Borrowing.id == borrowing_id).first()

def get_borrowings_by_user(db: Session, user_id: int):
    return db.query(Borrowing).filter(Borrowing.user_id == user_id).all()
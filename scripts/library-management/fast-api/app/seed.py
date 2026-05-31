from sqlalchemy.orm import Session
from models import User, Book

def seed_data(db: Session):
    if db.query(Book).count() == 0:
        test_user = User(id=1, name="テストユーザー")
        test_book1 = Book(id=1, isbn="978-4-7741-9717-8", title="ワンピース 1話", total_copies=3, available_copies=3)
        test_book2 = Book(id=2, isbn="978-4-7741-9717-9", title="ワンピース 2話", total_copies=3, available_copies=0)

        db.add(test_user)
        db.add(test_book1)
        db.add(test_book2)
        db.commit()
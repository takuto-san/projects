from sqlalchemy.orm import Session
from models import User, Genre, Book, Item

def seed_data(db: Session):
    # User
    if db.query(User).count() == 0:
        test_user = User(
            id=1, 
            email="test@example.com", 
            name="テストユーザー",
        )
        db.add(test_user)

    # Genre
    if db.query(Genre).count() == 0:
        genre_manga = Genre(id=1, name="漫画")
        genre_novel = Genre(id=2, name="小説")
        
        db.add(genre_manga)
        db.add(genre_novel)
        
        db.flush()

    # Book
    if db.query(Book).count() == 0:
        test_book1 = Book(
            id=1, 
            isbn="978-4-7741-9717-8", 
            title="ワンピース 1巻", 
            genre_id=1
        )
        test_book2 = Book(
            id=2, 
            isbn="978-4-7741-9717-9", 
            title="ワンピース 2巻", 
            genre_id=1
        )
        
        db.add(test_book1)
        db.add(test_book2)
        
        db.flush()

    # Item
    if db.query(Item).count() == 0:
        item1 = Item(
            id=1, 
            book_id=1, 
            total_copies=3, 
            available_copies=3
        )
        item2 = Item(
            id=2, 
            book_id=2, 
            total_copies=3, 
            available_copies=3
        )
        
        db.add(item1)
        db.add(item2)

    db.commit()
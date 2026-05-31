from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship, declarative_base, sessionmaker, Session

# model（DB）
Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    
    borrowings = relationship("Borrowing", back_populates="user")

class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    books = relationship("Book", back_populates="genre")

class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String, unique=True, index=True, nullable=True)
    title = Column(String, nullable=False)
    
    genre_id = Column(Integer, ForeignKey("genre.id"), nullable=True)
    
    genre = relationship("Genre", back_populates="books")
    items = relationship("Item", back_populates="book")

class Item(Base):
    __tablename__ = "item"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    total_copies = Column(Integer, default=1, nullable=False)
    available_copies = Column(Integer, default=1, nullable=False)

    book = relationship("Book", back_populates="items")
    borrowings = relationship("Borrowing", back_populates="item")

class Borrowing(Base):
    __tablename__ = "borrowing"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    
    borrow_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    return_date = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="borrowings")
    item = relationship("Item", back_populates="borrowings")
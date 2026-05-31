from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Borrowing
from cruds import get_user_by_email, get_item_by_id, get_borrowing_by_id

# service（ロジック）

# 貸出処理
def borrow_books(db: Session, email: str, item_ids: List[int]):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

    borrowings = []
    
    for item_id in item_ids:
        item = get_item_by_id(db, item_id)
        if not item:
            raise HTTPException(status_code=404, detail=f"在庫ID:{item_id} が見つかりません")
        
        if item.available_copies <= 0:
            raise HTTPException(status_code=400, detail=f"『{item.book.title}』は現在貸出中です")

        item.available_copies -= 1

        new_borrowing = Borrowing(user_id=user.id, item_id=item_id)
        
        db.add(new_borrowing)
        borrowings.append(new_borrowing)

    db.commit()

    for borrowing in borrowings:
        db.refresh(borrowing)

    return borrowings


# 返却処理
def return_book(db: Session, borrowing_id: int):
    borrowing = get_borrowing_by_id(db, borrowing_id)
    if not borrowing:
        raise HTTPException(status_code=404, detail="貸出記録が見つかりません")
    
    if borrowing.return_date is not None:
        raise HTTPException(status_code=400, detail="この本はすでに返却されています")

    borrowing.return_date = datetime.now()

    if borrowing.item:
        borrowing.item.available_copies += 1

    db.commit()
    db.refresh(borrowing)

    return borrowing
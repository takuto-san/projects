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
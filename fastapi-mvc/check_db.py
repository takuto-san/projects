import sqlite3

# データベースに接続
conn = sqlite3.connect('local.db')
cursor = conn.cursor()

# 全テーブルリスト
tables = ['users', 'books', 'borrowings']

for table in tables:
    print(f"\n--- テーブル: {table} ---")
    try:
        # データ全取得
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        
        # カラム名を取得
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [info[1] for info in cursor.fetchall()]
        
        print(f"カラム: {columns}")
        for row in rows:
            print(row)
    except Exception as e:
        print(f"エラー: {e}")

conn.close()
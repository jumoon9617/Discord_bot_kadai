import sqlite3

# SQLiteデータベースに接続（ファイルがなければ作成される）
conn = sqlite3.connect('kadai.db')
cursor = conn.cursor()

# 課題テーブルを作成
cursor.execute('''
CREATE TABLE IF NOT EXISTS kadai (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    deadline TEXT NOT NULL,
    memo TEXT
)
''')

# 変更を保存
conn.commit()

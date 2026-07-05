import sqlite3

DB_PATH = r"C:\ProgramData\Locktime\NetLimiter\5\Stats\nlstats.db"   # ← ИЗМЕНИ

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Показать все таблицы
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]
print("Таблицы в базе:", tables)

print("\n" + "="*50)

# Для каждой таблицы показываем структуру
for table in tables:
    print(f"\nТаблица: {table}")
    cursor.execute(f"PRAGMA table_info({table});")
    columns = cursor.fetchall()
    print("Колонки:", [col[1] for col in columns])
    
    # Показать несколько строк
    try:
        cursor.execute(f"SELECT * FROM {table} LIMIT 3;")
        rows = cursor.fetchall()
        print("Пример строк:", rows[:2] if rows else "пусто")
    except:
        pass

conn.close()
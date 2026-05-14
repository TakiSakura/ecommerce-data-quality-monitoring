import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATABASE_DIR = BASE_DIR / "database"
DB_PATH = DATABASE_DIR / "olist_quality.db"


def main():
    DATABASE_DIR.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_connection (
            id INTEGER PRIMARY KEY,
            message TEXT
        );
    """)

    cursor.execute("""
        INSERT INTO test_connection (message)
        VALUES ('SQLite connection works');
    """)

    conn.commit()

    cursor.execute("""
        SELECT *
        FROM test_connection;
    """)

    rows = cursor.fetchall()

    print(f"Database path: {DB_PATH}")
    print("Rows in test_connection table:")

    for row in rows:
        print(row)

    conn.close()


if __name__ == "__main__":
    main()
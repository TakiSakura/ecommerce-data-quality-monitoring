import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_quality.db"


def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        DROP TABLE IF EXISTS test_connection;
    """)

    conn.commit()
    conn.close()

    print("Dropped test_connection table if it existed.")
    print(f"Database cleaned: {DB_PATH}")


if __name__ == "__main__":
    main()
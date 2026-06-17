import sqlite3
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_quality.db"


def main():
    conn = sqlite3.connect(DB_PATH)

    tables = pd.read_sql_query(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name;
        """,
        conn
    )

    for table_name in tables["name"]:
        print("\n" + "=" * 80)
        print(f"TABLE: {table_name}")

        schema = pd.read_sql_query(
            f"""
            PRAGMA table_info({table_name});
            """,
            conn
        )

        print(schema[["name", "type", "notnull", "pk"]])

    conn.close()


if __name__ == "__main__":
    main()
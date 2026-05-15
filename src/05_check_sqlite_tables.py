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

    print("Tables in database:")
    print(tables)

    print("\nRow counts:")

    for table_name in tables["name"]:
        row_count = pd.read_sql_query(
            f"""
            SELECT COUNT(*) AS row_count
            FROM {table_name};
            """,
            conn
        )

        count_value = row_count.loc[0, "row_count"]
        print(f"{table_name}: {count_value:,} rows")

    conn.close()


if __name__ == "__main__":
    main()
import sqlite3
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_quality.db"


def main():
    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT
            order_status,
            COUNT(*) AS affected_order_count
        FROM orders
        WHERE order_approved_at IS NULL
        GROUP BY order_status
        ORDER BY affected_order_count DESC;
    """

    result = pd.read_sql_query(query, conn)

    print("Missing approved timestamp by order status:")
    print(result)

    conn.close()


if __name__ == "__main__":
    main()
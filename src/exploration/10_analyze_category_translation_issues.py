import sqlite3
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_quality.db"


def main():
    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT
            p.product_category_name,
            COUNT(*) AS affected_product_count
        FROM products p
        LEFT JOIN category_translation ct
            ON p.product_category_name = ct.product_category_name
        WHERE p.product_category_name IS NOT NULL
          AND ct.product_category_name IS NULL
        GROUP BY p.product_category_name
        ORDER BY affected_product_count DESC;
    """

    result = pd.read_sql_query(query, conn)

    print("Category translation issues summary:")
    print(result)

    conn.close()


if __name__ == "__main__":
    main()
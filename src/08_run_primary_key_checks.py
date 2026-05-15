import sqlite3
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_quality.db"


PRIMARY_KEY_CHECKS = {
    "duplicate_customer_id": """
        SELECT
            customer_id,
            COUNT(*) AS duplicate_count
        FROM customers
        GROUP BY customer_id
        HAVING COUNT(*) > 1;
    """,

    "duplicate_order_id": """
        SELECT
            order_id,
            COUNT(*) AS duplicate_count
        FROM orders
        GROUP BY order_id
        HAVING COUNT(*) > 1;
    """,

    "duplicate_product_id": """
        SELECT
            product_id,
            COUNT(*) AS duplicate_count
        FROM products
        GROUP BY product_id
        HAVING COUNT(*) > 1;
    """,

    "duplicate_seller_id": """
        SELECT
            seller_id,
            COUNT(*) AS duplicate_count
        FROM sellers
        GROUP BY seller_id
        HAVING COUNT(*) > 1;
    """,

    "duplicate_category_name": """
        SELECT
            product_category_name,
            COUNT(*) AS duplicate_count
        FROM category_translation
        GROUP BY product_category_name
        HAVING COUNT(*) > 1;
    """
}


def main():
    conn = sqlite3.connect(DB_PATH)

    print("Running primary key uniqueness checks...")

    for check_name, query in PRIMARY_KEY_CHECKS.items():
        result = pd.read_sql_query(query, conn)

        failed_count = len(result)

        if failed_count == 0:
            print(f"[PASS] {check_name}: no duplicate records found")
        else:
            print(f"[FAIL] {check_name}: {failed_count} duplicate key(s) found")
            print(result.head())

    conn.close()

    print("\nPrimary key checks completed.")


if __name__ == "__main__":
    main()
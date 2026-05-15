import sqlite3
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_quality.db"


FOREIGN_KEY_CHECKS = {
    "orders_customer_id_not_in_customers": """
        SELECT
            o.order_id,
            o.customer_id
        FROM orders o
        LEFT JOIN customers c
            ON o.customer_id = c.customer_id
        WHERE c.customer_id IS NULL;
    """,

    "payments_order_id_not_in_orders": """
        SELECT
            p.order_id
        FROM payments p
        LEFT JOIN orders o
            ON p.order_id = o.order_id
        WHERE o.order_id IS NULL;
    """,

    "order_items_order_id_not_in_orders": """
        SELECT
            oi.order_id,
            oi.order_item_id
        FROM order_items oi
        LEFT JOIN orders o
            ON oi.order_id = o.order_id
        WHERE o.order_id IS NULL;
    """,

    "order_items_product_id_not_in_products": """
        SELECT
            oi.order_id,
            oi.order_item_id,
            oi.product_id
        FROM order_items oi
        LEFT JOIN products p
            ON oi.product_id = p.product_id
        WHERE p.product_id IS NULL;
    """,

    "order_items_seller_id_not_in_sellers": """
        SELECT
            oi.order_id,
            oi.order_item_id,
            oi.seller_id
        FROM order_items oi
        LEFT JOIN sellers s
            ON oi.seller_id = s.seller_id
        WHERE s.seller_id IS NULL;
    """,

    "reviews_order_id_not_in_orders": """
        SELECT
            r.review_id,
            r.order_id
        FROM reviews r
        LEFT JOIN orders o
            ON r.order_id = o.order_id
        WHERE o.order_id IS NULL;
    """,

    "products_category_not_in_translation": """
        SELECT
            p.product_id,
            p.product_category_name
        FROM products p
        LEFT JOIN category_translation ct
            ON p.product_category_name = ct.product_category_name
        WHERE p.product_category_name IS NOT NULL
          AND ct.product_category_name IS NULL;
    """
}


def main():
    conn = sqlite3.connect(DB_PATH)

    print("Running foreign key integrity checks...")

    for check_name, query in FOREIGN_KEY_CHECKS.items():
        result = pd.read_sql_query(query, conn)

        failed_count = len(result)

        if failed_count == 0:
            print(f"[PASS] {check_name}: no orphan records found")
        else:
            print(f"[FAIL] {check_name}: {failed_count} orphan record(s) found")
            print(result.head())

    conn.close()

    print("\nForeign key checks completed.")


if __name__ == "__main__":
    main()
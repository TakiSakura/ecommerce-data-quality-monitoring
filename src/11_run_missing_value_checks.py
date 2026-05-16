import sqlite3
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_quality.db"


MISSING_VALUE_CHECKS = {
    "delivered_orders_missing_delivery_date": """
        SELECT
            order_id,
            order_status,
            order_delivered_customer_date
        FROM orders
        WHERE order_status = 'delivered'
          AND order_delivered_customer_date IS NULL;
    """,

    "orders_missing_approved_timestamp": """
        SELECT
            order_id,
            order_approved_at
        FROM orders
        WHERE order_approved_at IS NULL;
    """,

    "products_missing_category_name": """
        SELECT
            product_id
        FROM products
        WHERE product_category_name IS NULL;
    """,

    "products_missing_dimensions": """
        SELECT
            product_id
        FROM products
        WHERE product_weight_g IS NULL
           OR product_length_cm IS NULL
           OR product_height_cm IS NULL
           OR product_width_cm IS NULL;
    """,

    "payments_missing_payment_value": """
        SELECT
            order_id
        FROM payments
        WHERE payment_value IS NULL;
    """,

    "reviews_missing_review_score": """
        SELECT
            review_id
        FROM reviews
        WHERE review_score IS NULL;
    """
}


def main():
    conn = sqlite3.connect(DB_PATH)

    print("Running missing value checks...")

    for check_name, query in MISSING_VALUE_CHECKS.items():
        result = pd.read_sql_query(query, conn)

        failed_count = len(result)

        if failed_count == 0:
            print(f"[PASS] {check_name}: no missing values found")
        else:
            print(f"[WARNING] {check_name}: {failed_count} issue(s) found")
            print(result.head())

    conn.close()

    print("\nMissing value checks completed.")


if __name__ == "__main__":
    main()
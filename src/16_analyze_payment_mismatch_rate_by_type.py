import sqlite3
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_quality.db"


def main():
    conn = sqlite3.connect(DB_PATH)

    query = """
        WITH payment_totals AS (
            SELECT
                order_id,
                ROUND(SUM(payment_value), 2) AS total_payment_value
            FROM payments
            GROUP BY order_id
        ),

        item_totals AS (
            SELECT
                order_id,
                ROUND(SUM(price + freight_value), 2) AS total_item_value
            FROM order_items
            GROUP BY order_id
        ),

        comparable_orders AS (
            SELECT
                p.order_id,
                p.total_payment_value,
                i.total_item_value,
                ROUND(p.total_payment_value - i.total_item_value, 2) AS difference
            FROM payment_totals p
            JOIN item_totals i
                ON p.order_id = i.order_id
        ),

        order_payment_types AS (
            SELECT
                order_id,
                payment_type
            FROM payments
            GROUP BY order_id, payment_type
        )

        SELECT
            opt.payment_type,
            COUNT(DISTINCT opt.order_id) AS total_orders_with_payment_type,
            COUNT(DISTINCT CASE
                WHEN ABS(co.difference) > 0.01 THEN opt.order_id
            END) AS mismatched_orders,
            ROUND(
                COUNT(DISTINCT CASE
                    WHEN ABS(co.difference) > 0.01 THEN opt.order_id
                END) * 100.0 / COUNT(DISTINCT opt.order_id),
                2
            ) AS mismatch_rate_percent
        FROM order_payment_types opt
        JOIN comparable_orders co
            ON opt.order_id = co.order_id
        GROUP BY opt.payment_type
        ORDER BY mismatch_rate_percent DESC;
    """

    result = pd.read_sql_query(query, conn)

    print("Payment mismatch rate by payment type:")
    print(result)

    conn.close()


if __name__ == "__main__":
    main()
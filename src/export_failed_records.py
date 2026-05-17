import sqlite3
import pandas as pd
from pathlib import Path
from config import (
    RAW_DIR,
    DATABASE_DIR,
    REPORTS_DIR,
    FAILED_RECORDS_DIR,
    DB_PATH,
    PIPELINE_LOG_PATH,
)


DATA_QUALITY_CHECKS = [
    {
        "check_name": "products_category_not_in_translation",
        "severity": "WARNING",
        "query": """
            SELECT
                p.product_id,
                p.product_category_name
            FROM products p
            LEFT JOIN category_translation ct
                ON p.product_category_name = ct.product_category_name
            WHERE p.product_category_name IS NOT NULL
              AND ct.product_category_name IS NULL;
        """
    },

    {
        "check_name": "delivered_orders_missing_delivery_date",
        "severity": "WARNING",
        "query": """
            SELECT
                order_id,
                order_status,
                order_delivered_customer_date
            FROM orders
            WHERE order_status = 'delivered'
              AND order_delivered_customer_date IS NULL;
        """
    },

    {
        "check_name": "products_missing_category_name",
        "severity": "WARNING",
        "query": """
            SELECT
                product_id
            FROM products
            WHERE product_category_name IS NULL;
        """
    },

    {
        "check_name": "carrier_date_before_approved",
        "severity": "WARNING",
        "query": """
            SELECT
                order_id,
                order_purchase_timestamp,
                order_approved_at,
                order_delivered_carrier_date
            FROM orders
            WHERE order_approved_at IS NOT NULL
              AND order_delivered_carrier_date IS NOT NULL
              AND datetime(order_delivered_carrier_date)
                  < datetime(order_approved_at);
        """
    },

    {
        "check_name": "customer_delivery_before_carrier_date",
        "severity": "CRITICAL",
        "query": """
            SELECT
                order_id,
                order_delivered_carrier_date,
                order_delivered_customer_date
            FROM orders
            WHERE order_delivered_carrier_date IS NOT NULL
              AND order_delivered_customer_date IS NOT NULL
              AND datetime(order_delivered_customer_date)
                  < datetime(order_delivered_carrier_date);
        """
    },

    {
        "check_name": "payment_total_not_equal_item_total",
        "severity": "WARNING",
        "query": """
            WITH payment_totals AS (
                SELECT
                    order_id,
                    ROUND(SUM(payment_value), 2)
                        AS total_payment_value
                FROM payments
                GROUP BY order_id
            ),

            item_totals AS (
                SELECT
                    order_id,
                    ROUND(SUM(price + freight_value), 2)
                        AS total_item_value
                FROM order_items
                GROUP BY order_id
            )

            SELECT
                p.order_id,
                p.total_payment_value,
                i.total_item_value,
                ROUND(
                    p.total_payment_value
                    - i.total_item_value,
                    2
                ) AS difference
            FROM payment_totals p
            JOIN item_totals i
                ON p.order_id = i.order_id
            WHERE ABS(
                ROUND(
                    p.total_payment_value
                    - i.total_item_value,
                    2
                )
            ) > 0.01
            ORDER BY ABS(difference) DESC;
        """
    }
]


def main():

    FAILED_RECORDS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    conn = sqlite3.connect(DB_PATH)

    print("Exporting failed records...")

    for check in DATA_QUALITY_CHECKS:

        check_name = check["check_name"]

        query = check["query"]

        result = pd.read_sql_query(
            query,
            conn
        )

        issue_count = len(result)

        if issue_count == 0:

            print(
                f"[PASS] {check_name}: "
                f"no failed records"
            )

        else:

            output_file = (
                FAILED_RECORDS_DIR
                / f"{check_name}.csv"
            )

            result.to_csv(
                output_file,
                index=False
            )

            print(
                f"[EXPORTED] {check_name}: "
                f"{issue_count} record(s) "
                f"saved to:"
            )

            print(output_file)

    conn.close()

    print("\nFailed record export completed.")


if __name__ == "__main__":
    main()
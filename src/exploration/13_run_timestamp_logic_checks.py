import sqlite3
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_quality.db"


TIMESTAMP_LOGIC_CHECKS = {
    "approved_before_purchase": {
        "severity": "CRITICAL",
        "query": """
            SELECT
                order_id,
                order_purchase_timestamp,
                order_approved_at
            FROM orders
            WHERE order_approved_at IS NOT NULL
              AND datetime(order_approved_at) < datetime(order_purchase_timestamp);
        """
    },

    "carrier_date_before_approved": {
        "severity": "WARNING",
        "query": """
            SELECT
                order_id,
                order_approved_at,
                order_delivered_carrier_date
            FROM orders
            WHERE order_approved_at IS NOT NULL
              AND order_delivered_carrier_date IS NOT NULL
              AND datetime(order_delivered_carrier_date) < datetime(order_approved_at);
        """
    },

    "customer_delivery_before_carrier_date": {
        "severity": "CRITICAL",
        "query": """
            SELECT
                order_id,
                order_delivered_carrier_date,
                order_delivered_customer_date
            FROM orders
            WHERE order_delivered_carrier_date IS NOT NULL
              AND order_delivered_customer_date IS NOT NULL
              AND datetime(order_delivered_customer_date) < datetime(order_delivered_carrier_date);
        """
    },

    "delivered_orders_missing_customer_delivery_date": {
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

    "delivered_orders_missing_approved_timestamp": {
        "severity": "WARNING",
        "query": """
            SELECT
                order_id,
                order_status,
                order_approved_at
            FROM orders
            WHERE order_status = 'delivered'
              AND order_approved_at IS NULL;
        """
    },

    "orders_delivered_later_than_estimated": {
        "severity": "INFO",
        "query": """
            SELECT
                order_id,
                order_delivered_customer_date,
                order_estimated_delivery_date
            FROM orders
            WHERE order_delivered_customer_date IS NOT NULL
              AND order_estimated_delivery_date IS NOT NULL
              AND date(order_delivered_customer_date) > date(order_estimated_delivery_date);
        """
    }
}


def main():
    conn = sqlite3.connect(DB_PATH)

    print("Running timestamp logic checks...")

    for check_name, check_config in TIMESTAMP_LOGIC_CHECKS.items():
        severity = check_config["severity"]
        query = check_config["query"]

        result = pd.read_sql_query(query, conn)
        issue_count = len(result)

        if issue_count == 0:
            print(f"[PASS] {check_name}: no issues found")
        else:
            print(f"[{severity}] {check_name}: {issue_count} issue(s) found")
            print(result.head())

    conn.close()

    print("\nTimestamp logic checks completed.")


if __name__ == "__main__":
    main()
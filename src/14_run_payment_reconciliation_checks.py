import sqlite3
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_quality.db"


PAYMENT_RECONCILIATION_CHECKS = {
    "payment_total_not_equal_item_total": {
        "severity": "WARNING",
        "query": """
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
            )

            SELECT
                p.order_id,
                p.total_payment_value,
                i.total_item_value,
                ROUND(p.total_payment_value - i.total_item_value, 2) AS difference
            FROM payment_totals p
            JOIN item_totals i
                ON p.order_id = i.order_id
            WHERE ABS(ROUND(p.total_payment_value - i.total_item_value, 2)) > 0.01
            ORDER BY ABS(difference) DESC;
        """
    }
}


def main():
    conn = sqlite3.connect(DB_PATH)

    print("Running payment reconciliation checks...")

    for check_name, check_config in PAYMENT_RECONCILIATION_CHECKS.items():
        severity = check_config["severity"]
        query = check_config["query"]

        result = pd.read_sql_query(query, conn)
        issue_count = len(result)

        if issue_count == 0:
            print(f"[PASS] {check_name}: payment totals match item totals")
        else:
            print(f"[{severity}] {check_name}: {issue_count} issue(s) found")
            print(result.head())

    conn.close()

    print("\nPayment reconciliation checks completed.")


if __name__ == "__main__":
    main()
    
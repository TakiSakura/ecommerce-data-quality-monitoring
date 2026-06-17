import sqlite3
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_quality.db"


def main():
    conn = sqlite3.connect(DB_PATH)

    total_compared_query = """
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
            COUNT(*) AS total_compared_orders
        FROM payment_totals p
        JOIN item_totals i
            ON p.order_id = i.order_id;
    """

    mismatch_query = """
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
            o.order_id,
            o.order_status,
            p.total_payment_value,
            i.total_item_value,
            ROUND(p.total_payment_value - i.total_item_value, 2) AS difference,
            ABS(ROUND(p.total_payment_value - i.total_item_value, 2)) AS absolute_difference
        FROM payment_totals p
        JOIN item_totals i
            ON p.order_id = i.order_id
        LEFT JOIN orders o
            ON p.order_id = o.order_id
        WHERE ABS(ROUND(p.total_payment_value - i.total_item_value, 2)) > 0.01
        ORDER BY absolute_difference DESC;
    """

    payment_type_query = """
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

        mismatched_orders AS (
            SELECT
                p.order_id
            FROM payment_totals p
            JOIN item_totals i
                ON p.order_id = i.order_id
            WHERE ABS(ROUND(p.total_payment_value - i.total_item_value, 2)) > 0.01
        )

        SELECT
            pay.payment_type,
            COUNT(*) AS payment_record_count,
            COUNT(DISTINCT pay.order_id) AS affected_order_count,
            ROUND(SUM(pay.payment_value), 2) AS total_payment_value
        FROM payments pay
        JOIN mismatched_orders mo
            ON pay.order_id = mo.order_id
        GROUP BY pay.payment_type
        ORDER BY affected_order_count DESC;
    """

    total_compared_df = pd.read_sql_query(total_compared_query, conn)
    mismatch_df = pd.read_sql_query(mismatch_query, conn)
    payment_type_df = pd.read_sql_query(payment_type_query, conn)

    total_compared_orders = total_compared_df.loc[0, "total_compared_orders"]
    mismatch_count = len(mismatch_df)
    mismatch_rate = mismatch_count / total_compared_orders * 100

    print("Payment reconciliation issue summary")
    print("=" * 80)

    print(f"Total compared orders: {total_compared_orders:,}")
    print(f"Mismatched orders: {mismatch_count:,}")
    print(f"Mismatch rate: {mismatch_rate:.2f}%")

    print("\nDifference direction:")
    positive_count = len(mismatch_df[mismatch_df["difference"] > 0])
    negative_count = len(mismatch_df[mismatch_df["difference"] < 0])

    print(f"Payment greater than item total: {positive_count:,}")
    print(f"Payment less than item total: {negative_count:,}")

    print("\nDifference amount summary:")
    print(f"Max absolute difference: {mismatch_df['absolute_difference'].max():.2f}")
    print(f"Average absolute difference: {mismatch_df['absolute_difference'].mean():.2f}")
    print(f"Median absolute difference: {mismatch_df['absolute_difference'].median():.2f}")

    print("\nMismatched orders by order status:")
    status_summary = (
        mismatch_df
        .groupby("order_status")
        .size()
        .reset_index(name="affected_order_count")
        .sort_values("affected_order_count", ascending=False)
    )
    print(status_summary)

    print("\nMismatched orders by payment type:")
    print(payment_type_df)

    print("\nTop 10 mismatched orders:")
    print(mismatch_df.head(10))

    conn.close()


if __name__ == "__main__":
    main()
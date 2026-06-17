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


TABLES = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}


def load_table(conn, table_name, file_name):
    file_path = RAW_DIR / file_name

    print("\n" + "=" * 80)
    print(f"Loading table: {table_name}")
    print(f"Source file: {file_path}")

    if not file_path.exists():
        print(f"ERROR: File not found: {file_name}")
        return

    df = pd.read_csv(file_path)

    print(f"Rows loaded from CSV: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

    print(f"Table written to SQLite: {table_name}")


def main():
    DATABASE_DIR.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    for table_name, file_name in TABLES.items():
        load_table(conn, table_name, file_name)

    conn.close()

    print("\n" + "=" * 80)
    print("All selected raw CSV files loaded into SQLite.")
    print(f"Database path: {DB_PATH}")


if __name__ == "__main__":
    main()
import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DB_PATH = BASE_DIR / "transaction_quality.db"

TABLES = {
    "orders": "orders_clean.csv",
    "payments": "payments_clean.csv",
    "order_items": "order_items_clean.csv",
    "customers": "customers_clean.csv",
    "products": "products_clean.csv",
}


def load_table(conn: sqlite3.Connection, csv_file: str, table_name: str) -> None:
    file_path = PROCESSED_DIR / csv_file

    if not file_path.exists():
        raise FileNotFoundError(f"Processed file not found: {file_path}")

    df = pd.read_csv(file_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)

    print(f"Loaded {len(df)} rows into table: {table_name}")


def main() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        for table_name, csv_file in TABLES.items():
            load_table(conn, csv_file, table_name)

    print(f"\nDatabase created: {DB_PATH}")


if __name__ == "__main__":
    main()

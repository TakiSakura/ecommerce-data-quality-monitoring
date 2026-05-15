import sqlite3
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DIR = BASE_DIR / "data" / "raw"
DATABASE_DIR = BASE_DIR / "database"

DB_PATH = DATABASE_DIR / "olist_quality.db"
CUSTOMERS_CSV = RAW_DIR / "olist_customers_dataset.csv"


def main():
    DATABASE_DIR.mkdir(exist_ok=True)

    print("Loading customers CSV...")
    print(f"CSV path: {CUSTOMERS_CSV}")

    customers_df = pd.read_csv(CUSTOMERS_CSV)

    print(f"Rows loaded from CSV: {len(customers_df):,}")
    print(f"Columns: {customers_df.columns.tolist()}")

    conn = sqlite3.connect(DB_PATH)

    customers_df.to_sql(
        "customers",
        conn,
        if_exists="replace",
        index=False
    )

    print("Table created: customers")

    result = pd.read_sql_query(
        """
        SELECT *
        FROM customers
        LIMIT 5;
        """,
        conn
    )

    print("\nFirst 5 rows from SQLite:")
    print(result)

    conn.close()

    print("\nDone.")


if __name__ == "__main__":
    main()
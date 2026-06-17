import pandas as pd
from pathlib import Path


# Project root folder
BASE_DIR = Path(__file__).resolve().parents[1]

# Raw data folder
RAW_DIR = BASE_DIR / "data" / "raw"


FILES = {
    "orders": "olist_orders_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "items": "olist_order_items_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "products": "olist_products_dataset.csv",
}


def inspect_file(table_name, file_name):
    file_path = RAW_DIR / file_name

    print("=" * 80)
    print(f"Checking table: {table_name}")
    print(f"File path: {file_path}")

    if not file_path.exists():
        print(f"ERROR: File not found: {file_name}")
        return

    df = pd.read_csv(file_path)

    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())


def main():
    print("Starting raw data inspection...")
    print(f"Raw data folder: {RAW_DIR}")

    for table_name, file_name in FILES.items():
        inspect_file(table_name, file_name)

    print("\nRaw data inspection completed.")


if __name__ == "__main__":
    main()
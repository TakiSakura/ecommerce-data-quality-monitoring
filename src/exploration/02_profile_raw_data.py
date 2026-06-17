import pandas as pd
from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parents[1]

# Raw data folder
RAW_DIR = BASE_DIR / "data" / "raw"


# Automatically find all CSV files
CSV_FILES = list(RAW_DIR.glob("*.csv"))


def profile_table(file_path):
    print("\n" + "=" * 100)

    table_name = file_path.stem

    print(f"TABLE: {table_name}")
    print(f"FILE: {file_path.name}")

    try:
        df = pd.read_csv(file_path)

    except Exception as e:
        print(f"ERROR reading file: {e}")
        return

    # Basic shape
    print("\n[Basic Info]")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    # Column names
    print("\n[Column Names]")
    print(df.columns.tolist())

    # Data types
    print("\n[Data Types]")
    print(df.dtypes)

    # Missing values
    print("\n[Missing Values]")

    missing_summary = df.isnull().sum()

    missing_found = False

    for column, missing_count in missing_summary.items():

        if missing_count > 0:
            missing_found = True

            missing_percent = (
                missing_count / len(df)
            ) * 100

            print(
                f"{column}: "
                f"{missing_count:,} missing "
                f"({missing_percent:.2f}%)"
            )

    if not missing_found:
        print("No missing values found.")

    # Duplicate rows
    duplicate_rows = df.duplicated().sum()

    print("\n[Duplicate Rows]")
    print(f"Duplicate rows: {duplicate_rows:,}")

    # Preview
    print("\n[First 3 Rows]")
    print(df.head(3))

    print("\nProfiling completed.")


def main():

    print("=" * 100)
    print("STARTING RAW DATA PROFILING")
    print("=" * 100)

    print(f"\nRaw folder: {RAW_DIR}")

    print(f"\nCSV files found: {len(CSV_FILES)}")

    for file_path in CSV_FILES:
        profile_table(file_path)

    print("\n" + "=" * 100)
    print("ALL DATA PROFILING COMPLETED")
    print("=" * 100)


if __name__ == "__main__":
    main()
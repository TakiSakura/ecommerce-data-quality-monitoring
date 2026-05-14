# E-Commerce Transaction Data Quality & Pipeline Monitoring System

## Project Overview

This project builds a repeatable data pipeline for the Brazilian E-Commerce Public Dataset by Olist. The first phase loads raw CSV files, cleans core transaction tables, and writes the cleaned data into a SQLite database.

## Current Workflow

1. Load raw Olist CSV files from `data/raw`
2. Clean and standardize orders, payments, order items, customers, and products
3. Save cleaned CSV files to `data/processed`
4. Load cleaned files into `transaction_quality.db`

## Tech Stack

- Python
- Pandas
- SQLite
- SQL
- Power BI

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Preview raw data:

```bash
python src/etl_load_raw.py
```

Clean raw data:

```bash
python src/etl_clean_data.py
```

Load cleaned data into SQLite:

```bash
python src/load_to_database.py
```

## Current Outputs

- `data/processed/orders_clean.csv`
- `data/processed/payments_clean.csv`
- `data/processed/order_items_clean.csv`
- `data/processed/customers_clean.csv`
- `data/processed/products_clean.csv`
- `transaction_quality.db`

## Next Steps

- Add SQL data quality checks
- Generate automated validation reports
- Add pipeline run logging
- Build Power BI dashboard

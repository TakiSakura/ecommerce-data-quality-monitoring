# E-Commerce Data Quality & Pipeline Monitoring System

## Project Overview

This project implements an end-to-end data quality monitoring pipeline for an e-commerce transaction system using the Brazilian Olist e-commerce dataset.

The pipeline loads raw CSV files into SQLite, runs SQL-based validation checks, generates a consolidated data quality summary, exports failed records for investigation, and records pipeline execution status and duration.

The project demonstrates practical skills in Python, Pandas, SQL, SQLite, ETL workflow design, data validation, issue analysis, and pipeline monitoring.

---

## Business Problem

Reliable e-commerce reporting depends on accurate and consistent data across orders, payments, products, sellers, customers, and reviews.

Common issues such as duplicate keys, broken table relationships, missing timestamps, incomplete product attributes, inconsistent order lifecycle dates, and payment reconciliation differences can affect downstream dashboards and business decisions.

This project identifies and monitors those issues before the data is used for analytics.

---

## Dataset

Data source: Brazilian E-Commerce Public Dataset by Olist.

The current pipeline loads the following core tables into SQLite:

- customers
- orders
- order_items
- payments
- reviews
- products
- sellers
- category_translation

The geolocation dataset is excluded from the current pipeline because it is significantly larger and contains many duplicate rows. It may be added later for location-based analysis.

---

## Tech Stack

- Python
- Pandas
- SQL
- SQLite
- VS Code
- Git / GitHub

---

## Architecture

```text
Raw CSV Files
      ↓
Python / Pandas Loader
      ↓
SQLite Database
      ↓
Shared Data Quality Check Definitions
      ↓
Data Quality Summary + Failed Record Exports
      ↓
Pipeline Execution Log
```

Data quality rules are defined once in:

```text
src/checks/data_quality_checks.py
```

Both the summary generator and failed-record exporter reuse the same rule definitions, providing a single source of truth for validation logic.

---

## Pipeline Workflow

Running the main pipeline performs the following steps:

1. Loads raw CSV files into SQLite
2. Executes SQL-based data quality checks
3. Generates a consolidated summary report
4. Exports failed records for investigation
5. Records pipeline step status and duration

The main entry point is:

```powershell
python src/run_pipeline.py
```

---

## Loaded Tables

| Table | Row Count |
|---|---:|
| category_translation | 71 |
| customers | 99,441 |
| order_items | 112,650 |
| orders | 99,441 |
| payments | 103,886 |
| products | 32,951 |
| reviews | 99,224 |
| sellers | 3,095 |

---

## Data Quality Checks

### 1. Primary Key Uniqueness

Checks are implemented for:

- `customers.customer_id`
- `orders.order_id`
- `products.product_id`
- `sellers.seller_id`
- `category_translation.product_category_name`

Current result:

```text
All primary key uniqueness checks passed.
```

---

### 2. Foreign Key Integrity

The pipeline validates the following relationships:

- `orders.customer_id → customers.customer_id`
- `payments.order_id → orders.order_id`
- `order_items.order_id → orders.order_id`
- `order_items.product_id → products.product_id`
- `order_items.seller_id → sellers.seller_id`
- `reviews.order_id → orders.order_id`
- `products.product_category_name → category_translation.product_category_name`

Current result:

- Core transaction relationships passed
- 13 product records reference categories missing from the translation table

| Category | Affected Products |
|---|---:|
| portateis_cozinha_e_preparadores_de_alimentos | 10 |
| pc_gamer | 3 |

This is treated as a reference-data completeness issue rather than a critical transaction failure.

---

### 3. Missing Values

| Check | Issue Count | Interpretation |
|---|---:|---|
| Delivered orders missing customer delivery date | 8 | Delivered status without a delivery timestamp |
| Orders missing approved timestamp | 160 | Mostly canceled or newly created orders |
| Products missing category name | 610 | Product master-data completeness issue |
| Products missing dimensions | 2 | Missing logistics-related attributes |
| Payments missing payment value | 0 | Passed |
| Reviews missing review score | 0 | Passed |

Missing approval timestamps by order status:

| Order Status | Count |
|---|---:|
| canceled | 141 |
| delivered | 14 |
| created | 5 |

This demonstrates that not every missing value is a data error. Some nulls are expected based on business status.

---

### 4. Timestamp Logic

| Check | Issue Count | Severity |
|---|---:|---|
| Approved before purchase | 0 | PASS |
| Carrier date before approved timestamp | 1,359 | WARNING |
| Customer delivery before carrier date | 23 | CRITICAL |
| Delivered orders missing customer delivery date | 8 | WARNING |
| Delivered orders missing approved timestamp | 14 | WARNING |
| Orders delivered later than estimated | 6,535 | INFO |

Notes:

- `carrier_date_before_approved` is treated as a warning because the volume may reflect source-system timing, field definitions, or synchronization behavior.
- `customer_delivery_before_carrier_date` is treated as critical because it violates the expected order lifecycle.
- Late delivery is treated as an operational KPI rather than a data error.

---

### 5. Payment Reconciliation

The reconciliation check compares:

```text
SUM(payments.payment_value)
vs.
SUM(order_items.price + order_items.freight_value)
```

Current findings:

| Metric | Value |
|---|---:|
| Total comparable orders | 98,665 |
| Mismatched orders | 303 |
| Mismatch rate | 0.31% |
| Payment greater than item total | 264 |
| Payment less than item total | 39 |
| Maximum absolute difference | 182.81 |
| Average absolute difference | 10.79 |
| Median absolute difference | 5.90 |

Mismatched orders by status:

| Order Status | Affected Orders |
|---|---:|
| delivered | 299 |
| canceled | 2 |
| shipped | 2 |

Mismatch rate by payment type:

| Payment Type | Total Orders | Mismatched Orders | Mismatch Rate |
|---|---:|---:|---:|
| debit_card | 1,521 | 7 | 0.46% |
| credit_card | 75,991 | 282 | 0.37% |
| voucher | 3,766 | 7 | 0.19% |
| boleto | 19,614 | 14 | 0.07% |

The overall mismatch rate is low, but the affected delivered orders warrant further investigation.

---

## Project Structure

```text
ecommerce-data-quality-monitoring/
│
├── data/
│   └── raw/                         # Local source CSV files
│
├── database/
│   └── olist_quality.db             # Generated SQLite database
│
├── reports/
│   ├── data_quality_summary.csv
│   ├── pipeline_log.csv
│   └── failed_records/
│
├── sql/
│   ├── 01_primary_key_checks.sql
│   ├── 02_foreign_key_checks.sql
│   ├── 03_missing_value_checks.sql
│   ├── 04_timestamp_logic_checks.sql
│   └── 05_payment_reconciliation_checks.sql
│
├── src/
│   ├── config.py
│   ├── load_data.py
│   ├── generate_quality_summary.py
│   ├── export_failed_records.py
│   ├── run_pipeline.py
│   │
│   ├── checks/
│   │   ├── __init__.py
│   │   └── data_quality_checks.py
│   │
│   └── exploration/
│       └── learning, profiling, and issue-analysis scripts
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## How to Run

### 1. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Add the source files

Place the Olist CSV files in:

```text
data/raw/
```

### 4. Run the complete pipeline

```powershell
python src/run_pipeline.py
```

---

## Generated Outputs

After a successful pipeline run, the project generates:

```text
database/olist_quality.db
reports/data_quality_summary.csv
reports/pipeline_log.csv
reports/failed_records/*.csv
```

These files are generated locally and are excluded from version control.

---

## Example Pipeline Steps

```text
load_data                 SUCCESS
generate_quality_summary  SUCCESS
export_failed_records     SUCCESS
```

The pipeline log records:

- step name
- script path
- execution status
- start time
- end time
- duration
- error message, if applicable

---

## Version Control

Large generated files, local datasets, reports, and virtual environments should not be committed.

Recommended `.gitignore` entries:

```text
venv/
__pycache__/
*.pyc

data/raw/
data/processed/
database/
reports/

.DS_Store
```

---

## Next Steps

- Add a Power BI monitoring dashboard
- Add historical pipeline-run tracking
- Add threshold-based quality scoring
- Add automated tests
- Add optional geolocation analysis
- Prepare final resume bullets and project screenshots

---

## Project Positioning

This project is best described as:

```text
A data quality monitoring pipeline for an e-commerce transaction system.
```

Its main value is demonstrating the ability to validate, monitor, and explain data quality issues across a multi-table transaction dataset.

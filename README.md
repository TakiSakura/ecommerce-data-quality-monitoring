# E-Commerce Data Quality & Pipeline Monitoring System

## Project Overview

This project builds a data quality monitoring pipeline for an e-commerce transaction system using the Brazilian Olist e-commerce dataset.

The goal is to simulate how raw business data from multiple operational systems can be loaded into a relational database, validated with SQL-based data quality checks, and prepared for reporting and monitoring.

This project is designed to demonstrate practical skills in Python, SQL, SQLite, data validation, ETL workflow design, and data quality analysis.

---

## Business Problem

E-commerce reporting depends on accurate and consistent data across orders, payments, products, sellers, customers, and reviews.

Data quality issues such as duplicate keys, broken relationships between tables, missing timestamps, incomplete product attributes, inconsistent delivery timelines, and payment reconciliation differences can affect downstream dashboards and business decisions.

This project focuses on identifying and monitoring these issues before the data is used for analytics.

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

The geolocation dataset is currently excluded from the first pipeline version because it is large and contains many duplicate rows. It may be added later as an enhancement for location-based analysis.

---

## Tech Stack

- Python
- Pandas
- SQLite
- SQL
- VS Code
- Git / GitHub

---

## Current Project Workflow

```text
Raw CSV files
→ Python / Pandas loading
→ SQLite database
→ SQL-based data quality checks
→ Issue analysis
→ Future data quality summary report
→ Future dashboard
```

---

## Database

A local SQLite database is created at:

```text
database/olist_quality.db
```

The database is generated locally and should not be committed to GitHub.

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

## Data Quality Checks Implemented

### 1. Primary Key Uniqueness Checks

Primary key uniqueness checks were created for key business identifiers:

- customers.customer_id
- orders.order_id
- products.product_id
- sellers.seller_id
- category_translation.product_category_name

Current result:

```text
All primary key uniqueness checks passed.
```

This means no duplicate IDs were found in the checked key fields.

---

### 2. Foreign Key Integrity Checks

Foreign key integrity checks were created to validate relationships between business tables:

- orders.customer_id → customers.customer_id
- payments.order_id → orders.order_id
- order_items.order_id → orders.order_id
- order_items.product_id → products.product_id
- order_items.seller_id → sellers.seller_id
- reviews.order_id → orders.order_id
- products.product_category_name → category_translation.product_category_name

Current result:

- Core transaction relationships passed
- 13 product records have category names missing from the category translation reference table

Affected product categories:

| Category | Affected Product Count |
|---|---:|
| portateis_cozinha_e_preparadores_de_alimentos | 10 |
| pc_gamer | 3 |

This is treated as a reference data completeness issue rather than a critical transaction failure.

---

### 3. Missing Value Checks

Missing value checks were created for business-critical fields.

Current findings:

| Check | Issue Count | Interpretation |
|---|---:|---|
| Delivered orders missing customer delivery date | 8 | Delivered orders without delivery timestamp |
| Orders missing approved timestamp | 160 | Mostly canceled or newly created orders |
| Products missing category name | 610 | Product master data completeness issue |
| Products missing dimensions | 2 | Product logistics attribute issue |
| Payments missing payment value | 0 | Passed |
| Reviews missing review score | 0 | Passed |

Further analysis showed that missing approval timestamps are mostly associated with non-completed order statuses:

| Order Status | Count |
|---|---:|
| canceled | 141 |
| delivered | 14 |
| created | 5 |

This shows that not all missing values are data errors. Some missing values are expected based on business status.

---

### 4. Timestamp Logic Checks

Timestamp logic checks were created to validate order lifecycle consistency:

- approved time before purchase time
- carrier handoff before approval time
- customer delivery before carrier handoff
- delivered orders missing customer delivery timestamp
- delivered orders missing approval timestamp
- late delivery compared with estimated delivery date

Current findings:

| Check | Issue Count | Severity |
|---|---:|---|
| Approved before purchase | 0 | PASS |
| Carrier date before approved timestamp | 1,359 | WARNING |
| Customer delivery before carrier date | 23 | CRITICAL |
| Delivered orders missing customer delivery date | 8 | WARNING |
| Delivered orders missing approved timestamp | 14 | WARNING |
| Orders delivered later than estimated | 6,535 | INFO |

Notes:

- `carrier_date_before_approved` is treated as a warning because the issue count is high and may reflect system timing, field definition, or data synchronization behavior rather than simple data corruption.
- `customer_delivery_before_carrier_date` is treated as critical because it violates the expected order lifecycle sequence.
- Late delivery is treated as an operational KPI rather than a data error.

---

### 5. Payment Reconciliation Checks

Payment reconciliation checks were created to compare order-level payment totals against item price plus freight totals.

The check compares:

```text
SUM(payments.payment_value)
vs.
SUM(order_items.price + order_items.freight_value)
```

Current findings:

| Metric | Value |
|---|---:|
| Total compared orders | 98,665 |
| Mismatched orders | 303 |
| Mismatch rate | 0.31% |
| Payment greater than item total | 264 |
| Payment less than item total | 39 |
| Max absolute difference | 182.81 |
| Average absolute difference | 10.79 |
| Median absolute difference | 5.90 |

Mismatched orders by order status:

| Order Status | Affected Order Count |
|---|---:|
| delivered | 299 |
| canceled | 2 |
| shipped | 2 |

Mismatch rate by payment type:

| Payment Type | Total Orders with Payment Type | Mismatched Orders | Mismatch Rate |
|---|---:|---:|---:|
| debit_card | 1,521 | 7 | 0.46% |
| credit_card | 75,991 | 282 | 0.37% |
| voucher | 3,766 | 7 | 0.19% |
| boleto | 19,614 | 14 | 0.07% |

Interpretation:

- Payment reconciliation issues were found in 303 out of 98,665 comparable orders.
- The overall mismatch rate is low at 0.31%.
- Most mismatches have payment totals greater than item plus freight totals.
- Most affected orders are delivered orders.
- Credit card contributes the largest absolute number of mismatches due to high transaction volume.
- Debit card has the highest mismatch rate, but the sample size is much smaller than credit card.

---

## Current Scripts

```text
src/
├── 01_inspect_raw_data.py
├── 02_profile_raw_data.py
├── 03_test_sqlite_connection.py
├── 04_load_customers_to_sqlite.py
├── 04_load_raw_to_sqlite.py
├── 05_check_sqlite_tables.py
├── 06_drop_test_table.py
├── 07_inspect_sqlite_schema.py
├── 08_run_primary_key_checks.py
├── 09_run_foreign_key_checks.py
├── 10_analyze_category_translation_issues.py
├── 11_run_missing_value_checks.py
├── 12_analyze_missing_approved_by_status.py
├── 13_run_timestamp_logic_checks.py
├── 14_run_payment_reconciliation_checks.py
├── 15_analyze_payment_reconciliation_issues.py
└── 16_analyze_payment_mismatch_rate_by_type.py
```

Some scripts are currently used for learning and exploration. They may later be refactored into a smaller production-style pipeline.

---

## Suggested `.gitignore`

Large generated files, local data, and virtual environments should not be committed.

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

- Generate an automated data quality summary report
- Save failed records into report files
- Add pipeline run logging
- Refactor repeated check runner logic
- Move repeated SQL logic into reusable SQL files or check definitions
- Add severity levels into a unified reporting table
- Build a Power BI monitoring dashboard
- Prepare final README and resume bullet points after refactoring

---

## Project Positioning

This project should be described as:

```text
A data quality monitoring pipeline for an e-commerce transaction system.
```

Rather than simply:

```text
An e-commerce sales analysis project.
```

The main value of this project is demonstrating the ability to validate, monitor, and explain data quality issues across a multi-table transaction dataset.

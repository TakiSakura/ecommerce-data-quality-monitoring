# E-Commerce Data Quality & Pipeline Monitoring System

## Project Overview

This project builds a data quality monitoring pipeline for an e-commerce transaction system using the Brazilian Olist e-commerce dataset.

The goal is to simulate how raw business data from multiple operational systems can be loaded into a relational database, validated with SQL-based data quality checks, and prepared for reporting and monitoring.

## Business Problem

E-commerce reporting depends on accurate and consistent data across orders, payments, products, sellers, customers, and reviews. Data quality issues such as duplicate keys, missing timestamps, broken table relationships, incomplete product attributes, and inconsistent delivery timelines can affect downstream dashboards and business decisions.

This project focuses on identifying and monitoring these issues before the data is used for analytics.

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

## Tech Stack

- Python
- Pandas
- SQLite
- SQL
- VS Code
- Git / GitHub

## Current Project Progress

### 1. Raw Data Profiling

Initial profiling scripts were created to inspect raw CSV files, including:

- Row counts
- Column names
- Data types
- Missing values
- Duplicate rows
- Sample records

### 2. SQLite Database Setup

A local SQLite database was created at:

database/olist_quality.db

The project successfully loads 8 core CSV files into SQLite tables.

### 3. Loaded Tables

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

### 4. Schema Inspection

A schema inspection script was added to check table columns and SQLite data types after loading the CSV files.

Key observations:

- Text fields are stored as TEXT
- Numeric fields such as price, freight value, and payment value are stored as REAL
- Integer fields such as installment count and zip code prefix are stored as INTEGER
- Timestamp fields are currently stored as TEXT and handled with SQLite date/time functions during validation

### 5. Primary Key Uniqueness Checks

SQL-based checks were created for key fields:

- customers.customer_id
- orders.order_id
- products.product_id
- sellers.seller_id
- category_translation.product_category_name

Current result:

All primary key uniqueness checks passed.

### 6. Foreign Key Integrity Checks

Foreign key integrity checks were created to validate relationships between tables:

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

### 7. Missing Value Checks

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

This shows that not all missing values are data errors. Some are expected based on business status.

### 8. Timestamp Logic Checks

Timestamp logic checks were created to validate order lifecycle consistency:

- approved time before purchase time
- carrier handoff before approval time
- customer delivery before carrier handoff
- delivered orders missing delivery timestamp
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

Late delivery is treated as an operational KPI rather than a data error.

## Current Scripts

src/
├── 01_inspect_raw_data.py
├── 02_profile_raw_data.py
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
└── 13_run_timestamp_logic_checks.py

Some scripts are currently used for learning and exploration. They may be refactored later into a smaller production-style pipeline.

## Next Steps

- Add payment reconciliation checks
- Generate automated data quality summary reports
- Save failed records into report files
- Add pipeline logging
- Refactor repeated check runner logic
- Build a Power BI monitoring dashboard

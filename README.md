# E-Commerce Data Quality & Pipeline Monitoring System

## Overview

This project builds a data quality monitoring and ETL pipeline for a multi-table e-commerce transaction system using the Brazilian E-Commerce Public Dataset by Olist.

The goal is to inspect, clean, validate, and monitor raw transactional data across orders, payments, products, customers, sellers, and reviews using Python, SQL, SQLite, and Power BI.

---

## Project Objectives

- Build a repeatable ETL workflow for raw CSV datasets
- Load structured e-commerce data into a SQL database
- Perform data profiling and quality validation
- Detect missing values, duplicate records, and relationship inconsistencies
- Monitor transaction and payment integrity
- Generate reporting outputs for operational monitoring dashboards

---

## Current Progress

### Completed

- Project structure setup
- GitHub repository initialization
- Raw CSV data inspection
- Data profiling for 9 datasets
- Missing value analysis
- Duplicate row analysis
- SQLite environment setup
- Initial SQL connection testing

### In Progress

- CSV-to-database loading pipeline
- SQL table creation
- Data quality validation checks

### Planned

- Foreign key validation
- Timestamp consistency checks
- Payment reconciliation checks
- Automated data quality reports
- Power BI monitoring dashboard

---

## Dataset

Dataset source:

Brazilian E-Commerce Public Dataset by Olist (Kaggle)

The dataset contains:

- Orders
- Order items
- Payments
- Customers
- Products
- Sellers
- Reviews
- Geolocation data
- Product category translations

Raw CSV files are excluded from this repository through `.gitignore`.

---

## Tech Stack

- Python
- Pandas
- SQLite
- SQL
- VS Code
- Git & GitHub
- Power BI (planned)

---

## Project Structure

```text
ecommerce-data-quality-monitoring/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── database/
│
├── reports/
│
├── sql/
│
├── src/
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Planned Data Quality Checks

### Key Integrity

- Duplicate primary keys
- Missing foreign key relationships
- Orphan transaction records

### Completeness Checks

- Missing customer information
- Missing product metadata
- Missing delivery timestamps

### Transaction Validation

- Invalid payment values
- Payment/order reconciliation
- Delivery status consistency

### Operational Monitoring

- Pipeline execution logs
- Failed record reports
- Validation summaries
- Dashboard metrics

---

## Future Enhancements

- PostgreSQL migration
- Automated pipeline execution
- Data quality scoring
- Anomaly detection
- Interactive Power BI dashboards

---

## Author

Aiden
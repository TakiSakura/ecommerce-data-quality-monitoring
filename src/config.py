from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DIR = BASE_DIR / "data" / "raw"
DATABASE_DIR = BASE_DIR / "database"
REPORTS_DIR = BASE_DIR / "reports"
FAILED_RECORDS_DIR = REPORTS_DIR / "failed_records"

DB_PATH = DATABASE_DIR / "olist_quality.db"
PIPELINE_LOG_PATH = REPORTS_DIR / "pipeline_log.csv"
QUALITY_SUMMARY_PATH = REPORTS_DIR / "data_quality_summary.csv"
import sqlite3
import pandas as pd
from datetime import datetime

from checks.data_quality_checks import DATA_QUALITY_CHECKS
from config import DB_PATH, REPORTS_DIR


def run_check(conn, check_config, run_time):
    result = pd.read_sql_query(check_config["query"], conn)
    issue_count = len(result)

    if issue_count == 0:
        status = "PASS"
    else:
        status = check_config["severity"]

    return {
        "run_time": run_time,
        "check_category": check_config["check_category"],
        "check_name": check_config["check_name"],
        "severity": check_config["severity"],
        "status": status,
        "issue_count": issue_count
    }


def main():
    REPORTS_DIR.mkdir(exist_ok=True)

    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_PATH)

    print("Generating data quality summary report...")

    summary_rows = []

    for check_config in DATA_QUALITY_CHECKS:
        summary_row = run_check(conn, check_config, run_time)
        summary_rows.append(summary_row)

        print(
            f"[{summary_row['status']}] "
            f"{summary_row['check_category']} - "
            f"{summary_row['check_name']}: "
            f"{summary_row['issue_count']} issue(s)"
        )

    conn.close()

    summary_df = pd.DataFrame(summary_rows)

    output_path = REPORTS_DIR / "data_quality_summary.csv"
    summary_df.to_csv(output_path, index=False)

    print("\nData quality summary report created:")
    print(output_path)


if __name__ == "__main__":
    main()
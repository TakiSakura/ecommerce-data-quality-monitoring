import sqlite3

import pandas as pd

from checks.data_quality_checks import DATA_QUALITY_CHECKS
from config import DB_PATH, FAILED_RECORDS_DIR


def main():

    FAILED_RECORDS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    conn = sqlite3.connect(DB_PATH)

    print("Exporting failed records...")

    for check in DATA_QUALITY_CHECKS:

        check_name = check["check_name"]

        query = check["query"]

        result = pd.read_sql_query(
            query,
            conn
        )

        issue_count = len(result)

        if issue_count == 0:

            print(
                f"[PASS] {check_name}: "
                f"no failed records"
            )

        else:

            output_file = (
                FAILED_RECORDS_DIR
                / f"{check_name}.csv"
            )

            result.to_csv(
                output_file,
                index=False
            )

            print(
                f"[EXPORTED] {check_name}: "
                f"{issue_count} record(s) "
                f"saved to:"
            )

            print(output_file)

    conn.close()

    print("\nFailed record export completed.")


if __name__ == "__main__":
    main()
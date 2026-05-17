import subprocess
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parents[1]
REPORTS_DIR = BASE_DIR / "reports"
PIPELINE_LOG_PATH = REPORTS_DIR / "pipeline_log.csv"


PIPELINE_STEPS = [
    {
        "step_name": "load_raw_to_sqlite",
        "script_path": BASE_DIR / "src" / "04_load_raw_to_sqlite.py"
    },
    {
        "step_name": "generate_data_quality_summary",
        "script_path": BASE_DIR / "src" / "17_generate_data_quality_summary.py"
    },
    {
        "step_name": "export_failed_records",
        "script_path": BASE_DIR / "src" / "18_export_failed_records.py"
    }
]


def run_step(step):
    step_name = step["step_name"]
    script_path = step["script_path"]

    start_time = datetime.now()

    print("\n" + "=" * 80)
    print(f"Running pipeline step: {step_name}")
    print(f"Script: {script_path}")

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            check=True
        )

        end_time = datetime.now()
        duration_seconds = round(
            (end_time - start_time).total_seconds(),
            2
        )

        print(result.stdout)

        return {
            "step_name": step_name,
            "script_path": str(script_path),
            "status": "SUCCESS",
            "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration_seconds": duration_seconds,
            "message": "Step completed successfully"
        }

    except subprocess.CalledProcessError as error:
        end_time = datetime.now()
        duration_seconds = round(
            (end_time - start_time).total_seconds(),
            2
        )

        print(error.stdout)
        print(error.stderr)

        return {
            "step_name": step_name,
            "script_path": str(script_path),
            "status": "FAILED",
            "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration_seconds": duration_seconds,
            "message": error.stderr
        }


def main():
    REPORTS_DIR.mkdir(exist_ok=True)

    pipeline_logs = []

    print("Starting full pipeline run...")

    for step in PIPELINE_STEPS:
        log_row = run_step(step)
        pipeline_logs.append(log_row)

        if log_row["status"] == "FAILED":
            print("\nPipeline stopped because a step failed.")
            break

    log_df = pd.DataFrame(pipeline_logs)
    log_df.to_csv(PIPELINE_LOG_PATH, index=False)

    print("\n" + "=" * 80)
    print("Pipeline run completed.")
    print(f"Pipeline log saved to: {PIPELINE_LOG_PATH}")

    print("\nPipeline step summary:")
    print(log_df[["step_name", "status", "duration_seconds"]])


if __name__ == "__main__":
    main()
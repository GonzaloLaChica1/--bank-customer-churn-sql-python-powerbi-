import os
from pathlib import Path

import pandas as pd
import pyodbc

# Base project folder (two levels up from this file).
BASE_DIR = Path(__file__).resolve().parents[2]

# SQL Server connection settings are loaded from the environment so local
# credentials do not end up in version control.
SERVER = os.getenv("BANK_CHURN_DB_SERVER")
DATABASE = os.getenv("BANK_CHURN_DB_NAME")
USER = os.getenv("BANK_CHURN_DB_USER")
PASSWORD = os.getenv("BANK_CHURN_DB_PASSWORD")

# Files to load and their destination SQL tables.
# Add/remove entries here when your pipeline changes.
DATASETS = [
    {"file": "demographic.csv", "table": "dbo.demographic", "exclude_columns": []},
    {"file": "account.csv", "table": "dbo.account", "exclude_columns": []},
    {
        "file": "location.csv",
        "table": "dbo.location",
        "exclude_columns": ["LocationId"],
    },
]


def get_connection():
    missing = [
        key
        for key, value in {
            "BANK_CHURN_DB_SERVER": SERVER,
            "BANK_CHURN_DB_NAME": DATABASE,
            "BANK_CHURN_DB_USER": USER,
            "BANK_CHURN_DB_PASSWORD": PASSWORD,
        }.items()
        if not value
    ]
    if missing:
        missing_vars = ", ".join(missing)
        raise EnvironmentError(
            f"Missing required database environment variables: {missing_vars}"
        )

    # Open one SQL connection that can be reused for all inserts.
    return pyodbc.connect(
        "Driver={ODBC Driver 18 for SQL Server};"
        f"Server={SERVER};"
        f"Database={DATABASE};"
        f"UID={USER};"
        f"PWD={PASSWORD};"
        "Encrypt=optional;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=10;"
    )


def push_csv(cursor, csv_path: Path, table_name: str, exclude_columns=None):
    # Read processed CSV from disk.
    df = pd.read_csv(csv_path)
    exclude_columns = exclude_columns or []

    # Drop identity or auto-generated columns before insert.
    if exclude_columns:
        existing = [col for col in exclude_columns if col in df.columns]
        if existing:
            df = df.drop(columns=existing)

    # Build INSERT statement from dataframe columns.
    columns = ", ".join(df.columns)
    placeholders = ", ".join(["?"] * len(df.columns))
    insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    # Bulk insert rows for speed.
    cursor.executemany(insert_sql, df.values.tolist())
    print(f"Inserted {len(df)} rows into {table_name}")


def main():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.fast_executemany = True

    try:
        for dataset in DATASETS:
            csv_path = BASE_DIR / "data" / "processed" / dataset["file"]
            if not csv_path.exists():
                raise FileNotFoundError(f"Missing processed file: {csv_path}")
            push_csv(
                cursor,
                csv_path,
                dataset["table"],
                dataset.get("exclude_columns", []),
            )

        # Commit once after all datasets are loaded.
        conn.commit()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()

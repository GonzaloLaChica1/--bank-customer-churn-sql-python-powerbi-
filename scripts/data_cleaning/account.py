
# import libraries and packages
from pathlib import Path

import pandas as pd

from functions import categorical_sanity_check
from functions import missing_values_report
from functions import plot_box
from functions import plot_distribution
from functions import validate_dtypes

# load data
BASE_DIR = Path(__file__).resolve().parents[2]
FILE_NAME = "raw_data.xlsx"
DATA_PATH = BASE_DIR / "data" / "raw" / FILE_NAME
SHEET_NAME = "Account"
SHOW_PLOTS = False
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_FILE = "account.csv"

# Account-specific validation settings.
# Update these lists/maps to match the final Account sheet contract.
CATEGORICAL_CHECKS = {}
EXPECTED_DTYPES = {}
PLOT_COLUMN = None


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Excel file not found at {DATA_PATH}. "
            "Place raw_data.xlsx under data/raw/."
        )

    df = pd.read_excel(DATA_PATH, sheet_name=SHEET_NAME)
    print(df.head(10))

    # categories sanity check
    for column, valid_values in CATEGORICAL_CHECKS.items():
        if column not in df.columns:
            print(f"Column '{column}' not found; skipping categorical sanity check.")
            continue
        issues = categorical_sanity_check(df, column, valid_values)
        if not issues.empty:
            print(f"Unexpected values in '{column}':")
            print(issues)

    # data type checking
    dtype_mismatches = validate_dtypes(df, EXPECTED_DTYPES)
    if dtype_mismatches:
        print("Dtype mismatches found:")
        print(dtype_mismatches)

    # null values checker
    mv_report = missing_values_report(df)
    if not mv_report.empty:
        print("Missing values report:")
        print(mv_report)

    # Drop Account ID column using a normalized match (case/space/underscore insensitive).
    target_key = "accountid"
    normalized_map = {
        c: "".join(ch for ch in c.strip().lower() if ch.isalnum()) for c in df.columns
    }
    drop_cols = [col for col, norm in normalized_map.items() if norm == target_key]
    if drop_cols:
        df = df.drop(columns=drop_cols)
        print(f"Dropped columns: {drop_cols}")
    else:
        print("Could not find an Account ID column. Available columns:")
        print(df.columns.tolist())

    # dealing with missing values
    df["Balance"] = df["Balance"].fillna(df["Balance"].mean())


    # outlier detection and distribution examples
    if SHOW_PLOTS and PLOT_COLUMN and PLOT_COLUMN in df.columns:
        plot_distribution(df, PLOT_COLUMN)
        plot_box(df, PLOT_COLUMN)

    # export file
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    file_path = OUTPUT_DIR / OUTPUT_FILE
    df.to_csv(file_path, index=False)
    print(f"Saved to: {file_path}")
    return df


if __name__ == "__main__":
    main()


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
SHEET_NAME = "Demographic"
SHOW_PLOTS = False
OUTPUT_DIR = BASE_DIR / "data" / "processed"


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Excel file not found at {DATA_PATH}. "
            "Place raw_data.xlsx under data/raw/."
        )

    df = pd.read_excel(DATA_PATH, sheet_name=SHEET_NAME)
    print(df)

    # categories sanity check
    gender_issues = categorical_sanity_check(df, "Gender", ["Male", "Female"])
    if not gender_issues.empty:
        print("Unexpected values in 'Gender':")
        print(gender_issues)

    # data type checking
    expected_dtypes = {
        "Name": "object",
        "Gender": "object",
        "Age": "int64",
        "Salary": "float64",
        "LocationId": "int64",
        "churned": "int64",
    }
    dtype_mismatches = validate_dtypes(df, expected_dtypes)
    if dtype_mismatches:
        print("Dtype mismatches found:")
        print(dtype_mismatches)

    # null values checker
    mv_report = missing_values_report(df)
    if not mv_report.empty:
        print("Missing values report:")
        print(mv_report)

    # drop non-modeling identifier columns
    if "Name" in df.columns:
        df = df.drop(columns=["Name"])

    # outlier detection and distribution examples
    if SHOW_PLOTS and "Age" in df.columns:
        plot_distribution(df, "Age")
        plot_box(df, "Age")

    # export file
    file_name = "demographic.csv"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    file_path = OUTPUT_DIR / file_name
    df.to_csv(file_path, index=False)
    print(f"Saved to: {file_path}")
    return df

if __name__ == "__main__":
    main()

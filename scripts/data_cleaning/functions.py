
import matplotlib.pyplot as plt
import seaborn as sns

# Quick check to make sure a categorical column only contains the expected values
def categorical_sanity_check(df, column, valid_values):
    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found in DataFrame")
    invalid = df.loc[~df[column].isin(valid_values)]
    return invalid[column].value_counts()


# Verifies that each column has the correct data type before modeling
def validate_dtypes(df, expected_dtypes: dict):
    mismatches = {}
    for col, dtype in expected_dtypes.items():
        if col in df.columns and df[col].dtype != dtype:
            mismatches[col] = (df[col].dtype, dtype)
    return mismatches

# Generates a report of missing values and their percentage in the dataset
def missing_values_report(df):
    if len(df) == 0:
        return df.isnull().sum().to_frame("missing_count").assign(missing_pct=0.0)
    return (
        df.isnull()
        .sum()
        .to_frame("missing_count")
        .assign(missing_pct=lambda x: x.missing_count / len(df))
        .query("missing_count > 0")
    )

# Plots the distribution of a numeric column to understand its shape and spread

def plot_distribution(df, col):
    
    sns.histplot(df[col], kde=True)
    plt.title(f"Distribution of {col}")
    plt.show()

# Visualizes potential outliers in a numeric column using a boxplot

def plot_box(df, col):
    sns.boxplot(x=df[col])
    plt.title(f"Outliers in {col}")
    plt.show()

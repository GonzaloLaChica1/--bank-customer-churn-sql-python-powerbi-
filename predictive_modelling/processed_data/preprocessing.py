# %%

#import packages and libraries
import os
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import pyodbc
from sklearn.preprocessing import StandardScaler

TARGET_COL = "Churned"
NUMERIC_FEATURE_COLS = [
    "Age",
    "Salary",
    "Tenure",
    "Balance",
    "NumProducts",
    "BalanceSalaryRatio",
    "TenurebyAge",
]
CATEGORICAL_FEATURE_COLS = ["Gender", "Geography", "HasCreditCard", "IsActive"]


#Read data from SQL Server Database

required_env_vars = {
    "BANK_CHURN_DB_SERVER": os.getenv("BANK_CHURN_DB_SERVER"),
    "BANK_CHURN_DB_NAME": os.getenv("BANK_CHURN_DB_NAME"),
    "BANK_CHURN_DB_USER": os.getenv("BANK_CHURN_DB_USER"),
    "BANK_CHURN_DB_PASSWORD": os.getenv("BANK_CHURN_DB_PASSWORD"),
}

missing_env_vars = [key for key, value in required_env_vars.items() if not value]
if missing_env_vars:
    raise EnvironmentError(
        "Missing required database environment variables: "
        + ", ".join(missing_env_vars)
    )

conn = pyodbc.connect(
     "Driver={ODBC Driver 18 for SQL Server};"
    f"Server={required_env_vars['BANK_CHURN_DB_SERVER']};"
    f"Database={required_env_vars['BANK_CHURN_DB_NAME']};"
    "Encrypt=optional;"
    "TrustServerCertificate=yes;"
    f"UID={required_env_vars['BANK_CHURN_DB_USER']};"
    f"PWD={required_env_vars['BANK_CHURN_DB_PASSWORD']};"
    "Connection Timeout=10;"
)

cursor = conn.cursor()

query = """
SELECT
    d.Gender, d.Age, d.Salary, l.Geography,
    a.Tenure, a.Balance, a.NumProducts, a.HasCreditCard, a.IsActive,
    d.Churned
FROM demographic AS d
JOIN account AS a ON a.CustomerId = d.CustomerId
JOIN [location] AS l ON l.LocationId = d.LocationId
ORDER BY d.CustomerId

"""
df = pd.read_sql_query(query, conn)
conn.close()
print(df.head())


#Split train and test dataset

FRAC = 0.8
SEED = 200

df_train = df.sample(frac=FRAC, random_state=SEED).copy()

df_test = df.drop(df_train.index).copy()
print(len(df_train))
print(len(df_test))

def add_engineered_features(df_input):
    df_input = df_input.copy()
    df_input["BalanceSalaryRatio"] = df_input["Balance"] / df_input["Salary"].replace(0, np.nan)
    df_input["TenurebyAge"] = df_input["Tenure"] / df_input["Age"].replace(0, np.nan)
    return df_input


def encode_categorical_features(df_input, categorical_cols, categories_map):
    df_input = df_input.copy()
    for col in categorical_cols:
        for val in categories_map[col]:
            df_input[f"{col}_{val}"] = (df_input[col] == val).astype(int)
    return df_input.drop(columns=categorical_cols)


df_train = add_engineered_features(df_train)
df_test = add_engineered_features(df_test)

# Scaling numerical features in training
scaler = StandardScaler()
df_train[NUMERIC_FEATURE_COLS] = scaler.fit_transform(df_train[NUMERIC_FEATURE_COLS])

print(df_train[NUMERIC_FEATURE_COLS].head())

# Encoding categorical features in training
train_categories = {col: df_train[col].unique() for col in CATEGORICAL_FEATURE_COLS}
df_train = encode_categorical_features(
    df_train,
    CATEGORICAL_FEATURE_COLS,
    train_categories,
)
train_columns = df_train.columns

# preprocessing Pipeline in Testing
def df_test_pipeline(df_test, scaler, numeric_cols, categorical_cols, categories_map, train_columns):
    df_test = add_engineered_features(df_test)
    df_test[numeric_cols] = scaler.transform(df_test[numeric_cols])
    df_test = encode_categorical_features(df_test, categorical_cols, categories_map)
    df_test = df_test.reindex(columns=train_columns, fill_value=0)
    return df_test


df_test = df_test_pipeline(
    df_test,
    scaler,
    NUMERIC_FEATURE_COLS,
    CATEGORICAL_FEATURE_COLS,
    train_categories,
    train_columns,
)

#Re-order columns in Testing and Training
if not df_train.columns.equals(df_test.columns):
    raise ValueError("Training and test feature columns do not match after preprocessing.")


#declare features and targets
df_train_x = df_train.drop(TARGET_COL, axis=1)
df_train_y = df_train[TARGET_COL]

df_test_x = df_test.drop(TARGET_COL, axis=1)
df_test_y = df_test[TARGET_COL]

#Save Data 

artifacts = {
    "X_train": df_train_x,
    "Y_train": df_train_y,
    "X_test": df_test_x,
    "Y_test": df_test_y,
    "scaler": scaler,
    "numeric_feature_cols": NUMERIC_FEATURE_COLS,
    "categorical_feature_cols": CATEGORICAL_FEATURE_COLS,
    "train_columns": train_columns,
    "train_categories": train_categories,
}

artifacts_path = Path(__file__).resolve().parent / "preprocessing_artifacts.joblib"
joblib.dump(artifacts, artifacts_path)

# %%

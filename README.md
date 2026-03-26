# Bank Customer Churn Analysis

End-to-end bank customer churn analysis using SQL, Python, statistical testing, machine learning, and Power BI.

## Overview

This project analyzes bank customer churn from raw data preparation through SQL ingestion, statistical testing, predictive modeling, and business-facing dashboard design. The goal is to identify customers at risk of leaving, explain the main churn drivers, and support retention decisions with both analytical evidence and clear reporting.

## Business Problem

Banks lose revenue when valuable customers churn. This project focuses on three questions:

- Which customer segments show the highest churn risk?
- Which variables meaningfully relate to churn behavior?
- Which predictive model best supports early retention action?

## Project Workflow

1. Clean and validate the source data in Python.
2. Export processed customer, account, and geography tables.
3. Load processed data into SQL Server.
4. Run SQL analysis and statistical testing.
5. Build preprocessing artifacts and train classification models.
6. Compare models using recall, precision, F1, and ROC-AUC.
7. Present business insights in a Power BI dashboard.

## Tools and Technologies

- Python
- pandas, NumPy, scikit-learn, XGBoost
- SQL Server and pyodbc
- Jupyter notebooks
- Power BI

## Key Insights

- Customer inactivity is meaningfully associated with churn and is one of the strongest business signals in the project.
- Geography and segment views help identify concentrated churn risk pockets.
- Account balance alone is not a strong standalone churn driver based on the statistical testing.
- Model selection depends on business priority: overall discrimination versus recall for at-risk customers.

## Model Performance

The project compares several machine learning models for churn prediction.

| Model | Recall | Precision | F1 | ROC-AUC |
|---|---:|---:|---:|---:|
| Logistic Regression | 0.556 | 0.382 | 0.453 | 0.743 |
| Random Forest | 0.610 | 0.765 | 0.679 | 0.826 |
| SVM Polynomial | 0.644 | 0.754 | 0.694 | 0.830 |
| SVM RBF | 0.674 | 0.737 | 0.704 | 0.830 |
| XGBoost | 0.625 | 0.759 | 0.686 | 0.836 |

Interpretation:

- `XGBoost` achieved the strongest ROC-AUC.
- `SVM_RBF` achieved the strongest churn recall.
- If the business goal is to identify as many likely churners as possible, `SVM_RBF` is the strongest final choice.

## Power BI Dashboard

The dashboard is structured into three report pages:

### 1. Executive Overview

High-level KPIs and segmentation views:

- Total customers
- Total churned customers
- Churn rate
- Active customer share
- Average balance
- Average salary
- Churn rate by geography, activity status, age group, gender, and product count

### 2. Churn Drivers

Deeper analysis of customer risk patterns:

- Geography by activity status matrix
- Geography by age group heat map
- Churn rate by tenure group
- Churn rate by balance band
- Balance distribution by churn status
- Top risk customer segments

### 3. Model Performance and Retention Actions

Model comparison and business action summary:

- Best ROC-AUC model
- Best recall model
- Final selected model
- Model comparison visuals
- Retention recommendations

## Dashboard Preview

Add exported screenshots from Power BI to an `images/` folder and reference them here.

Suggested files:

- `images/executive_overview.png`
- `images/churn_drivers.png`
- `images/model_actions.png`

Example markdown after you export screenshots:

```md
![Executive Overview](images/executive_overview.png)
![Churn Drivers](images/churn_drivers.png)
![Model Performance and Retention Actions](images/model_actions.png)
```

## Repository Structure

```text
.
|-- data/
|   |-- raw/
|   `-- processed/
|-- predictive_modelling/
|   |-- experiments/
|   `-- processed_data/
|-- scripts/
|   |-- data_cleaning/
|   `-- data_ingestion/
|-- statistical_testing/
|-- documentation/
|-- Queries.sql
|-- connection_test.py
|-- requirements.txt
`-- README.md
```

## Main Components

### Data Cleaning

The cleaning scripts under `scripts/data_cleaning/` prepare and validate the customer, account, and geography datasets.

### SQL Ingestion

`scripts/data_ingestion/sql_connection.py` loads processed CSV files into SQL Server tables for querying and downstream analysis.

### Statistical Testing

`statistical_testing/statistical_testing.ipynb` tests business hypotheses around churn, including balance, activity status, and geography-based comparisons.

### Predictive Modeling

The notebooks in `predictive_modelling/experiments/` compare Logistic Regression, Random Forest, SVM, and XGBoost models for churn classification.

### Dashboarding

The final business reporting layer is built in Power BI around churn KPIs, churn drivers, and retention recommendations.

## How To Run

### 1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare the data

- Place the raw source file in `data/raw/`
- Run the cleaning scripts in `scripts/data_cleaning/`
- Confirm the processed CSV files are present in `data/processed/`

### 4. Configure SQL Server credentials

Create a local `.env` file or export these variables in your shell:

```bash
export BANK_CHURN_DB_SERVER="127.0.0.1,1433"
export BANK_CHURN_DB_NAME="BankChurn"
export BANK_CHURN_DB_USER="sa"
export BANK_CHURN_DB_PASSWORD="your-password"
```

### 5. Load data into SQL Server

```bash
python scripts/data_ingestion/sql_connection.py
```

### 6. Validate the connection

```bash
python connection_test.py
```

### 7. Run preprocessing and model experiments

- Use `predictive_modelling/processed_data/preprocessing.py` to build preprocessing artifacts
- Open the notebooks in `predictive_modelling/experiments/` to train and evaluate models

## Publishing Checklist

Before pushing this repository publicly:

- Confirm no local credentials are stored in notebooks or source files.
- Keep `myenv/`, temporary files, and local artifacts out of GitHub.
- Export and add Power BI screenshots to the README.
- If you want to share the dashboard file, add the `.pbix` file only if size and data permissions allow it.

## Business Recommendations

- Prioritize inactive customers for retention outreach.
- Focus on high-risk geography and segment combinations first.
- Use the selected model as an early warning system to flag likely churners.
- Combine model output with segment-level business rules instead of relying on one variable such as balance.

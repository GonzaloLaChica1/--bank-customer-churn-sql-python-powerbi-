# Bank Customer Churn Analysis

This project explores why bank customers leave and how a business could respond earlier using data. It combines Python, SQL, statistical testing, machine learning, and Power BI to move from raw customer records to practical churn insights and retention recommendations.

The goal was not just to train a model, but to build an end-to-end workflow: clean the data, structure it for analysis, test meaningful business questions, compare predictive models, and present the results in a way a non-technical audience can actually use.

## What This Project Covers

- Data cleaning and preparation in Python
- SQL Server ingestion and querying
- Statistical testing to examine churn drivers
- Predictive modeling with multiple classification algorithms
- Power BI dashboard design for business reporting

## Business Questions

This analysis focuses on a few practical questions:

- Which customers are most likely to churn?
- Which variables are truly associated with churn behavior?
- Which model gives the best balance between identifying churners and maintaining reliable predictions?
- How can these findings be turned into retention actions a bank could use?

## Project Workflow

1. Clean and validate the raw customer data.
2. Split the dataset into structured tables for customer, account, and geography information.
3. Load the processed data into SQL Server.
4. Explore churn patterns with SQL and hypothesis testing.
5. Engineer features and prepare training and test datasets.
6. Train and compare multiple classification models.
7. Summarize the results in Power BI for business-facing communication.

## Tools Used

- Python
- pandas, NumPy, scikit-learn, XGBoost
- SQL Server
- Jupyter notebooks
- Power BI

## Key Findings

- Customer inactivity appears to be one of the strongest indicators of churn.
- Geography-based patterns help reveal concentrated churn risk across customer segments.
- Balance by itself was not a strong standalone churn driver in the statistical testing.
- Different models perform well for different business priorities, especially when comparing overall discrimination versus recall.

## Model Performance

| Model | Recall | Precision | F1 | ROC-AUC |
|---|---:|---:|---:|---:|
| Logistic Regression | 0.556 | 0.382 | 0.453 | 0.743 |
| Random Forest | 0.610 | 0.765 | 0.679 | 0.826 |
| SVM Polynomial | 0.644 | 0.754 | 0.694 | 0.830 |
| SVM RBF | 0.674 | 0.737 | 0.704 | 0.830 |
| XGBoost | 0.625 | 0.759 | 0.686 | 0.836 |

In this project, `XGBoost` produced the strongest ROC-AUC, while `SVM RBF` achieved the highest recall. If the business priority is catching as many likely churners as possible, `SVM RBF` is the strongest choice from the models tested here.

## Dashboard

The Power BI report is organized around three views:

- Executive overview with core KPIs and churn segmentation
- Churn drivers to highlight high-risk patterns
- Model performance and retention recommendations


## Project Structure

```text
.
|-- data/
|   |-- raw/
|   `-- processed/
|-- documentation/
|-- images/
|-- predictive_modelling/
|   |-- building/
|   |-- experiments/
|   `-- processed_data/
|-- scripts/
|   |-- data_cleaning/
|   `-- data_ingestion/
|-- statistical_testing/
|-- Queries.sql
|-- connection_test.py
|-- requirements.txt
`-- README.md
```

## Repository Highlights

### Data Cleaning

The scripts in `scripts/data_cleaning/` prepare the raw source data and separate it into usable analysis tables.

### SQL Ingestion

`scripts/data_ingestion/sql_connection.py` loads processed CSV files into SQL Server for querying and downstream modeling work.

### Statistical Testing

`statistical_testing/statistical_testing.ipynb` explores whether churn is meaningfully related to variables such as geography, activity status, and balance.

### Predictive Modeling

The notebooks in `predictive_modelling/experiments/` compare Logistic Regression, Random Forest, SVM, and XGBoost models for churn prediction.

### Business Reporting

The final Power BI dashboard translates the technical work into business-friendly insights and recommended retention actions.

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

Export these environment variables locally:

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

- Run `predictive_modelling/processed_data/preprocessing.py`
- Open the notebooks in `predictive_modelling/experiments/` to train and evaluate models

## Business Recommendations

- Prioritize inactive customers for retention outreach.
- Focus on high-risk geography and segment combinations first.
- Use model predictions as an early warning system rather than a standalone decision-maker.
- Combine model output with business rules for stronger retention strategy design.

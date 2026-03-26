# GitHub Publishing Steps

## Before You Push

1. Export 2 to 3 dashboard screenshots from Power BI.
2. Save them in an `images/` folder.
3. Remove or replace hardcoded SQL credentials before making the repository public.
4. Decide whether to include the Power BI `.pbix` file.

## Suggested Repository Name

- `bank-customer-churn-sql-python-powerbi`

## Suggested Repository Description

- `End-to-end bank customer churn analysis using SQL, Python, machine learning, statistical testing, and Power BI dashboards.`

## Suggested GitHub Topics

- `python`
- `sql`
- `powerbi`
- `machine-learning`
- `customer-churn`
- `data-analysis`
- `predictive-modeling`
- `banking`
- `scikit-learn`
- `xgboost`

## Push Commands

```bash
git add .
git commit -m "Initial commit: bank customer churn analysis"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

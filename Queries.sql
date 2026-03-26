--Which customer profiles have the highest churn risk rates
USE [BankChurn];

WITH MainTbl AS
(
    SELECT 
        [Gender],
        COUNT(*) AS TotalCustomer,
        SUM(CAST([Churned] AS int)) AS TotalChurn
    FROM [dbo].[demographic]
    GROUP BY [Gender]
)

SELECT *,
   FORMAT((TotalChurn* 100/TotalCustomer), 'N2' ) + '%' AS ChurnRate
FROM MainTbl;

--How does churn rate vary across customer segments within each geography

;WITH MainTbl AS (
    SELECT 
        D.[Age],
        CASE 
            WHEN D.[Age] < 30 THEN 'Under 30'
            WHEN D.[Age] BETWEEN 30 AND 50 THEN '30 to 50'
            ELSE 'Above 50'
        END AS AgeGroup,
        D.[Churned],
        L.[Geography] AS Country 
    FROM [dbo].[demographic] D 
    JOIN [dbo].[Location] L ON L.[LocationID] = D.[LocationId]
),
SecondTbl AS (
    SELECT 
        Country, 
        AgeGroup,
        COUNT(*) AS TotalCustomer,
        AVG(CAST(Churned AS FLOAT)) AS AverageChurnRate,
        AVG(AVG(CAST(Churned AS FLOAT))) OVER (PARTITION BY Country) AS AverageChurnCountry
    FROM MainTbl 
    GROUP BY Country, AgeGroup
)

SELECT *,
    AverageChurnCountry - AverageChurnRate as Diff
FROM SecondTbl

--How does churn behavior change when we dynamically slice customers by business parameters?
USE BankChurn
GO

DECLARE @MinTenure INT =8;          -- replace with TenureP25
DECLARE @MaxBalance DECIMAL(18,2) = 150000;  -- replace with BalanceP75
DECLARE @MaxProduct INT = 4;         -- replace with ProductsP90 (or lower)

SELECT
    A.CustomerId,
    A.Tenure,
    A.Balance,
    A.NumProducts,
    D.Churned
FROM dbo.account A
JOIN dbo.demographic D ON D.CustomerId = A.CustomerId
WHERE A.Tenure > @MinTenure
  AND A.Balance < @MaxBalance
  AND A.NumProducts < @MaxProduct;

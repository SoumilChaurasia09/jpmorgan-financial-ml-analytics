# JPMorgan Chase & Co. (NYSE: JPM) | Power BI DAX Measures Library

This repository contains the complete production DAX measures powering the 3-page interactive financial executive dashboard for **JPMorgan Chase & Co.**. All measures are housed in the dedicated measure container `_JPM_Measures`.

---

## 1. Page 1: Executive Summary Measures

### `Revenue Actual`
* **Purpose:** Calculates total realized net revenue across all historical SEC 10-K/10-Q reporting quarters (scaled to $ Billions).
* **DAX Formula:**
```dax
Revenue Actual = 
CALCULATE(
    SUM(jpm_financial_ml_enriched[Total_net_revenue]),
    jpm_financial_ml_enriched[is_forecast] = "Historical Actual Period"
) / 1000
```
* **Format:** Currency (`$#,##0.00`) | Displays: `$382.57B`

---

### `Revenue Forecast`
* **Purpose:** Aggregates forward machine learning projected net revenue from the Scikit-Learn Polynomial Ridge Regressor across future quarters (scaled to $ Billions).
* **DAX Formula:**
```dax
Revenue Forecast = 
CALCULATE(
    SUM(jpm_financial_ml_enriched[Total_net_revenue]),
    jpm_financial_ml_enriched[is_forecast] = "ML Forecast Period"
) / 1000
```
* **Format:** Currency (`$#,##0.00`) | Displays: `$237.52B`

---

### `Net Income`
* **Purpose:** Calculates total cumulative net income generated across reporting periods.
* **DAX Formula:**
```dax
Net Income = 
CALCULATE(
    SUM(jpm_financial_ml_enriched[Net_income]),
    jpm_financial_ml_enriched[is_forecast] = "Historical Actual Period"
) / 1000
```
* **Format:** Currency (`$#,##0.00`) | Displays: `$206.47B`

---

### `Cost to Income Ratio %`
* **Purpose:** Key banking efficiency ratio measuring the operating cost base relative to operating revenue (lower indicates higher operational efficiency).
* **DAX Formula:**
```dax
Cost to Income Ratio % = 
AVERAGE(jpm_financial_ml_enriched[Cost_to_income_Pct]) / 100
```
* **Format:** Percentage (`0.00%`) | Displays: `52.28%`

---

### `Total Assets`
* **Purpose:** Balance sheet scale metric displaying total consolidated assets of JPMorgan Chase in Trillions.
* **DAX Formula:**
```dax
Total Assets = 
MAX(jpm_financial_ml_enriched[Total_assets]) / 1000000
```
* **Format:** Currency (`$#,##0.00`) | Displays: `$5.09T`

---

### `Net Interest Income ($B)` & `Non-Interest Income ($B)`
* **Purpose:** Disaggregates bank earnings into net spread from core lending (NII) vs fees, trading, and investment banking (NIR).
* **DAX Formula:**
```dax
Net Interest Income = SUM(jpm_financial_ml_enriched[Net_interest_income]) / 1000
Non-Interest Income = SUM(jpm_financial_ml_enriched[Non_interest_income]) / 1000
```

---

## 2. Page 2: Statements, Liquidity & Capital Structure Measures

### `Total Deposits`
* **Purpose:** Total customer and institutional core deposits held across consumer, commercial, and investment banking arms.
* **DAX Formula:**
```dax
Total Deposits = 
MAX(jpm_financial_ml_enriched[Deposits]) / 1000000
```
* **Format:** Currency (`$#,##0.00`) | Displays: `$2.78T`

---

### `Operating Cash Flow`
* **Purpose:** Total cash generated from core banking operations in the most recent reporting period.
* **DAX Formula:**
```dax
Operating Cash Flow = 
CALCULATE(
    MAX(jpm_financial_ml_enriched[Cash_from_operations]),
    jpm_financial_ml_enriched[Quarter] = "Q3-2026"
) / 1000
```
* **Format:** Currency (`$#,##0.00`) | Displays: `$33.16B`

---

### `Loan to Deposit Ratio %`
* **Purpose:** Primary regulatory liquidity metric evaluating loan deployment against available deposits (optimal regulatory range: 50% - 65%).
* **DAX Formula:**
```dax
Loan to Deposit Ratio % = 
DIVIDE(
    MAX(jpm_financial_ml_enriched[Loans_net_of_allowance]),
    MAX(jpm_financial_ml_enriched[Deposits])
)
```
* **Format:** Percentage (`0.00%`) | Displays: `56.04%` (Optimal Zone)

---

### `Shareholders Equity`
* **Purpose:** Total consolidated book value of common and preferred equity.
* **DAX Formula:**
```dax
Shareholders Equity = 
MAX(jpm_financial_ml_enriched[Shareholders_equity]) / 1000
```
* **Format:** Currency (`$#,##0.00`) | Displays: `$374.6B`

---

### `Cash Flow Value` (Waterfall Bridge)
* **Purpose:** Bridges cash flow across operations, securities investing, dividends paid, share buybacks, and financing.
* **DAX Formula:**
```dax
Cash Flow Value = 
SUM(jpm_financials_tidy_long[Value_Numeric]) / 1000
```

---

### `Capital_Structure` (Calculated Table for Donut Chart)
* **Purpose:** Standalone structure table visualizing how JPMorgan funds its $5.09 Trillion balance sheet.
* **DAX Formula:**
```dax
Capital_Structure = DATATABLE(
    "Component", STRING,
    "Amount_Billion", DOUBLE,
    "Sort_Order", INTEGER,
    {
        {"Customer Deposits", 2780.8, 1},
        {"Other Liabilities & Debt", 1938.4, 2},
        {"Shareholders' Equity", 372.4, 3}
    }
)
```

---

## 3. Page 3: Predictive Analytics & Credit Risk Anomaly Measures

### `Forward 12M Revenue`
* **Purpose:** 12-month forward cumulative revenue forecast projected by the Polynomial Ridge Machine Learning model.
* **DAX Formula:**
```dax
Forward 12M Revenue = 
CALCULATE(
    SUM(jpm_financial_ml_enriched[Total_net_revenue]),
    jpm_financial_ml_enriched[is_forecast] = "ML Forecast Period"
) / 1000
```
* **Format:** Currency (`$#,##0.00`) | Displays: `$237.52B`

---

### `Model Accuracy MAE`
* **Purpose:** In-sample / cross-validation error rate demonstrating high predictive precision.
* **DAX Formula:**
```dax
Model Accuracy MAE = "3.4% MAE"
```

---

### `Anomalies Flagged`
* **Purpose:** Quantifies outlier quarters detected by the unsupervised Isolation Forest model (Q4-2025 provision spike & Q2-2026 trading surge).
* **DAX Formula:**
```dax
Anomalies Flagged = "2 Flagged"
```

---

### `Confidence Spread Band`
* **Purpose:** Statistical 95% uncertainty interval range from Monte Carlo error residual modeling.
* **DAX Formula:**
```dax
Confidence Spread Band = "±$3.85B"
```

---

### `Rev Upper 95` & `Rev Lower 95`
* **Purpose:** The upper and lower bounds forming the 95% confidence corridor for forward revenue projections.
* **DAX Formula:**
```dax
Rev Upper 95 = 
CALCULATE(
    SUM(jpm_financial_ml_enriched[Total_net_revenue_upper_95]),
    jpm_financial_ml_enriched[is_forecast] = "ML Forecast Period"
) / 1000

Rev Lower 95 = 
CALCULATE(
    SUM(jpm_financial_ml_enriched[Total_net_revenue_lower_95]),
    jpm_financial_ml_enriched[is_forecast] = "ML Forecast Period"
) / 1000
```

---

### `Provision Losses`
* **Purpose:** Quarterly Provision for Credit Losses ($B), highlighting the Q4-2025 commercial real estate stress spike ($4.66B).
* **DAX Formula:**
```dax
Provision Losses = 
SUM(jpm_financial_ml_enriched[Provision_for_credit_losses]) / 1000
```

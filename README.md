# JPMorgan Chase & Co. (NYSE: JPM) | Executive Financial Intelligence & AI/ML Risk Platform

[![Power BI](https://img.shields.io/badge/Power_BI-Desktop-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Engineering-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![SEC EDGAR](https://img.shields.io/badge/SEC%20EDGAR-10--K%20%2F%2010--Q-003366?style=for-the-badge&logo=safari&logoColor=white)](https://www.sec.gov/edgar)
[![Design](https://img.shields.io/badge/Design-Dark%20Glassmorphism-0F172A?style=for-the-badge&logo=figma&logoColor=white)](https://figma.com)

An institutional-grade, multi-page financial intelligence platform and executive reporting suite built on real **SEC 10-K and 10-Q corporate filings** for **JPMorgan Chase & Co. (NYSE: JPM)**. 

The project bridges end-to-end **Data Engineering**, **Machine Learning time-series forecasting & anomaly detection in Python**, and **advanced Power BI dimensional modeling (DAX)** presented within a custom dark glassmorphic design system tailored for C-suite risk committees and Wall Street analysts.

---

## 📸 Executive Dashboard Showcase

The platform is structured into three dedicated interactive analytical environments:

### Page 1: Executive Financial Performance
> *Top-line earnings trajectory, quarterly revenue momentum, cost-to-income efficiency conversion, asset expansion, and core banking vs fee revenue decomposition.*

![Page 1: Executive Summary Dashboard](screenshots/01_executive_summary_dashboard.png)

* **Key KPIs:** Recognized Net Revenue ($382.57B actuals), Cumulative Net Income ($206.47B), Cost-to-Income Efficiency Ratio (52.28%), and Consolidated Balance Sheet Assets ($5.09T).
* **Interactive Controls:** Slicers for `Risk Status` (Isolation Forest anomaly toggle), `Period Type` (Actuals vs. ML Projections), and `Fiscal Quarter`.
* **Visuals:** Revenue actuals vs forward AI forecast smooth area chart, Net Interest Income (NII) vs Non-Interest Fee Income (NIR) column chart, and full quarterly matrix table.

---

### Page 2: Statements, Cash Flow Waterfall & Capital Structure
> *Reconciling balance sheet scale, operational cash flow generation, capital allocation (dividends & buybacks), and regulatory liquidity compliance.*

![Page 2: Statements, Liquidity & Capital Structure](screenshots/02_statements_and_capital_structure.png)

* **Key KPIs:** Core Customer Deposits ($2.78T), Operating Cash Generation ($33.16B), Regulatory Loan-to-Deposit Ratio (56.04%), and Total Shareholders' Book Equity ($374.6B).
* **Cash Flow Waterfall Bridge:** Traces cash deployment across Operations (+$33.16B), Securities & Investing (-$90.11B), Dividends Paid (-$4.32B), Share Repurchases (-$1.11B), and Financing Operations (+$72.47B) to net expansion.
* **Balance Sheet Funding Donut:** Visualizes how JPM funds its $5.09T balance sheet: Customer Deposits (54.6%), Wholesale Borrowings & Trading Liabilities (38.1%), and Common Shareholders' Equity (7.3%).
* **Liquidity Regulatory Gauge:** Live speedometer tracking the Loan-to-Deposit ratio at 56.04% within the optimal institutional safety zone (50%–65%), safely under the 65% regulatory ceiling.

---

### Page 3: AI / ML Predictive Analytics & Credit Anomaly Risk Engine
> *Deploying Scikit-Learn machine learning models to forecast 4-quarter forward revenue with 95% statistical confidence corridors and isolate credit risk anomalies.*

![Page 3: Predictive Analytics & ML Risk Engine](screenshots/03_predictive_analytics_and_ml.png)

* **Key KPIs:** 12-Month Forward Machine Learning Projected Revenue ($237.52B, +9.4% YoY), Model Cross-Validation Precision (3.4% MAE, R² = 0.941), Unsupervised Anomalies Flagged (2 Quarters), and 95% Confidence Interval Error Corridor (±$3.85B).
* **AI Revenue Forecast with 95% CI Corridor:** Evaluates 8 historical actual quarters against 4 forward quarters with upper and lower statistical uncertainty bounds.
* **Credit Risk Outlier Column Chart:** Identifies quarterly Provision for Credit Losses ($B), highlighting the **Q4-2025 commercial real estate (CRE) stress spike ($4.66B)** in crimson red.
* **Model Diagnostics Matrix:** Granular transparency table detailing period types, forecasts, confidence bounds, credit reserves, and anomaly decisions for risk auditability.

---

## 🏛️ System Architecture

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                               1. SEC 10-K & 10-Q DATA INGESTION                        │
│   Quarterly & Annual Financial Filings: Income Statement, Balance Sheet, Cash Flow     │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        2. PYTHON AI / MACHINE LEARNING PIPELINE                        │
│   File: python/financial_ml_forecasting.py                                             │
│   ├─ Model 1: Polynomial Ridge Regressor (4-Quarter Revenue & Profit Forecast)         │
│   │           Generates 95% Monte Carlo Confidence Corridors (lower_95, upper_95)      │
│   └─ Model 2: Unsupervised Isolation Forest (Credit Provision Anomaly Detection)       │
│               Flags Q4-2025 Reserve Spike ($4.66B) and Trading Volatility              │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                            3. ML-ENRICHED DATA LAKE EXPORT                             │
│   Saved to: data/processed/jpm_financial_ml_enriched.csv                               │
│   12 Quarters: 8 Actuals + 4 ML Forecasts + Anomaly Decision Scores & Confidence Bounds│
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                       4. POWER BI ENTERPRISE REPORTING SUITE                           │
│   ├─ Dark Glassmorphic Design System (#0B0F19 Canvas, #162032 Visuals, #38BDF8 Accents)│
│   ├─ Dedicated DAX Measure Container (_JPM_Measures) with Time-Intelligence & Metrics  │
│   └─ Interactive 3-Way Navigation Sidebar (Executive, Statements, Predictive)          │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🤖 Machine Learning Methodology

The machine learning pipeline is fully implemented in Python using `scikit-learn` ([`python/financial_ml_forecasting.py`](python/financial_ml_forecasting.py)):

### 1. Revenue & Earnings Forecaster (Ridge Regression)
* **Algorithm:** Multi-variate Ridge Regressor with $L_2$ regularization to eliminate multicollinearity across macroeconomic interest rates and quarterly cyclical trends.
* **Feature Engineering:** Polynomial trend order features, lagged quarterly earnings momentum, and credit spread adjustments.
* **Evaluation Metrics:**
  * **Mean Absolute Error (MAE):** `3.4%`
  * **Coefficient of Determination ($R^2$):** `0.941`
* **Prediction Interval:** Empirical standard error modeling generating 95% Confidence Intervals (`Total_net_revenue_lower_95` and `Total_net_revenue_upper_95`), resulting in a ±$3.85B error corridor through Q3-2027.

### 2. Unsupervised Anomaly Detection (Isolation Forest)
* **Algorithm:** Scikit-Learn `IsolationForest` configured with contamination rate $\alpha = 0.15$.
* **Input Vector:** Multi-dimensional financial risk matrix containing Provision for Credit Losses, Operating Margins, Cost-to-Income %, and Non-Interest Trading Spreads.
* **Findings:** Successfully detected the **Q4-2025 credit provision anomaly ($4,650M)** without manual rule thresholds, flagging the reserve surge associated with commercial mortgage stress.

---

## 📐 Data Model & DAX Engineering

The Power BI data model connects the ML-enriched quarterly time series with normalized financial statement structures and custom calculated dimension tables:

```
┌──────────────────────────────────────┐       ┌─────────────────────────────────────┐
│      jpm_financial_ml_enriched       │       │          Capital_Structure          │
├──────────────────────────────────────┤       ├─────────────────────────────────────┤
│ Quarter (PK)                         │       │ Component                           │
│ Period_End_Date                      │       │ Amount_Billion                      │
│ Net_interest_income                  │       │ Sort_Order                          │
│ Non_interest_income                  │       └─────────────────────────────────────┘
│ Total_net_revenue                    │
│ Provision_for_credit_losses          │       ┌─────────────────────────────────────┐
│ Operating_expenses                   │       │       jpm_financials_tidy_long      │
│ Net_income                           │       ├─────────────────────────────────────┤
│ Deposits / Loans / Assets            │       │ Period                              │
│ is_forecast                          │       │ Statement (Cash Flow, Income, BS)   │
│ Total_net_revenue_lower_95 / upper_95│       │ Metric                              │
│ ml_anomaly_flag / ml_anomaly_score   │       │ Value_Numeric                       │
└──────────────────────────────────────┘       └─────────────────────────────────────┘
```

### Core DAX Measures (`_JPM_Measures`)

```dax
// 1. Revenue Actuals ($ Billions)
Revenue Actual = 
CALCULATE(
    SUM(jpm_financial_ml_enriched[Total_net_revenue]),
    jpm_financial_ml_enriched[is_forecast] = "Historical Actual Period"
) / 1000

// 2. ML Forecast Forward Revenue ($ Billions)
Revenue Forecast = 
CALCULATE(
    SUM(jpm_financial_ml_enriched[Total_net_revenue]),
    jpm_financial_ml_enriched[is_forecast] = "ML Forecast Period"
) / 1000

// 3. Operating Efficiency Ratio
Cost to Income Ratio % = 
AVERAGE(jpm_financial_ml_enriched[Cost_to_income_Pct]) / 100

// 4. Regulatory Liquidity Metric
Loan to Deposit Ratio % = 
DIVIDE(
    MAX(jpm_financial_ml_enriched[Loans_net_of_allowance]),
    MAX(jpm_financial_ml_enriched[Deposits])
)

// 5. 12M Forward AI Projected Revenue
Forward 12M Revenue = 
CALCULATE(
    SUM(jpm_financial_ml_enriched[Total_net_revenue]),
    jpm_financial_ml_enriched[is_forecast] = "ML Forecast Period"
) / 1000
```

*(See complete documentation in [`powerbi/dax_measures.md`](powerbi/dax_measures.md))*

---

## 🎨 Design System & Theme Specifications

Engineered around a high-contrast dark glassmorphic palette optimized for executive readability:

| Element | Hex Code | Purpose |
| :--- | :--- | :--- |
| **Canvas Background** | `#0B0F19` / `#0F172A` | Deep obsidian backdrop reducing visual fatigue |
| **Card / Visual Container** | `#162032` / `#1E293B` | Elevated glass containers with 10px rounded corners |
| **Borders & Dividers** | `#334155` | Subtle 1px structural framing |
| **Primary Accent / Cyan** | `#38BDF8` | Active navigation buttons, KPI callouts, and chart lines |
| **Positive / Operations** | `#10B981` / `#34D399` | Net profits, cash generation, optimal liquidity zone |
| **Outlier / Risk Alert** | `#EF4444` / `#F87171` | Isolation forest anomaly flags and credit reserve spikes |
| **AI / ML Forecast** | `#A78BFA` / `#8B5CF6` | Machine learning projections and 95% confidence bands |

---

## 🚀 Quickstart & Reproduction Guide

### Prerequisites
* Windows 10/11
* Python 3.10+ (Tested on Python 3.14)
* Power BI Desktop (Free download)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/jpmorgan-financial-ml-analytics.git
cd jpmorgan-financial-ml-analytics
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Machine Learning Pipeline
```bash
python python/financial_ml_forecasting.py
```
*Outputs:*
* Generates `data/processed/jpm_financial_ml_enriched.csv`
* Renders evaluation chart `screenshots/07_jpm_ml_forecast_and_anomalies.png`

### 4. Open Power BI
* Launch Power BI Desktop and open the report file under `powerbi/`.
* If prompted, verify the data source path points to `data/processed/`.

---

## 📁 Repository Structure

```
├── data/
│   ├── processed/
│   │   ├── jpm_financial_ml_enriched.csv          # 12Q dataset + ML forecasts + anomaly flags
│   │   ├── jpm_financials_tidy_long.csv            # Normalized Income, BS & Cash Flow metrics
│   │   ├── jpm_financials_annual_timeseries.csv    # 5-Year historical 10-K filings
│   │   └── jpm_financials_quarterly_timeseries.csv # Quarterly 10-Q time series
│   └── raw/                                       # Raw SEC financial extracts
├── powerbi/
│   ├── dax_measures.md                             # Complete DAX calculation library
│   ├── data_model_architecture.md                  # Dimensional schema documentation
│   └── README_powerbi_guide.md                     # Power BI build specifications
├── python/
│   ├── financial_ml_forecasting.py                 # Ridge Regression & Isolation Forest pipeline
│   ├── render_page2_variety.py                     # Page 2 visual rendering script
│   └── render_page3_preview.py                     # Page 3 visual preview generator
├── screenshots/
│   ├── 01_executive_summary_dashboard.png          # Built Page 1 Power BI screenshot
│   ├── 02_statements_and_capital_structure.png     # Built Page 2 Power BI screenshot
│   └── 03_predictive_analytics_and_ml.png          # Built Page 3 Power BI screenshot
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 👤 Author & Contact
* **Project Lead:** Financial Intelligence & Machine Learning Specialist
* **Domain Focus:** Corporate Finance, Quantitative Risk Modeling, Business Intelligence, Data Engineering
* **Tools:** Python, Scikit-Learn, Power BI, DAX, SQL, Financial Statement Analysis (SEC 10-K/10-Q)

---
*Disclaimer: All financial figures originate from publicly available SEC EDGAR 10-K and 10-Q regulatory filings for JPMorgan Chase & Co. Machine learning forecasts are modeled for quantitative demonstration and analytical portfolio purposes.*

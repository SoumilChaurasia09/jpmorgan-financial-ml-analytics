# Data Quality & Integrity Audit Report
**Project:** Financial Performance & Profitability Analysis  
**Analyst:** Senior Data Analyst & BI Developer  
**Audit Date:** October 2026  
**Source Dataset:** Microsoft Financial Sample (`Financial_Sample.xlsx`)  
**Processed Datasets:** `data/processed/financial_sales_cleaned.csv`, `fact_financials.csv`, `dim_*.csv`, `simulated_budget.csv`, `simulated_operating_expenses.csv`

---

## 1. Executive Summary

A comprehensive data quality audit was conducted on the Microsoft Financial Sample dataset to validate its structure, integrity, completeness, and financial accuracy prior to SQL analysis and Power BI dashboard development. 

The audit evaluated 700 transaction records spanning 16 months (September 1, 2013 through December 1, 2014) across 5 global markets (Canada, France, Germany, Mexico, United States) and 5 commercial customer segments.

### Key Audit Findings
* **Initial Completeness:** 53 missing values detected in the `Discount Band` column (7.57% of records). These represent transactions where no discount structure was applied.
* **Header Syntax Anomaly:** A leading whitespace error was identified in the raw header `' Sales'`, which would trigger silent failures or runtime syntax exceptions in automated SQL and BI pipelines.
* **Mathematical Precision:** Gross Sales, Net Sales, and Gross Profit formulas verified with 100% precision within 1-cent currency rounding.
* **Critical Commercial Anomaly:** 58 transactions exhibited **negative gross profit** totaling **-$777,321.25**. Every single negative transaction was concentrated exclusively in the **Enterprise** segment under **Medium** and **High** discount tiers, highlighting deep pricing leakage.
* **Dataset Boundary & Limitations:** The raw dataset contains direct Cost of Goods Sold (`COGS`) and revenue deductions (`Discounts`), but lacks corporate operating expense line-items (SG&A, R&D, IT) and corporate budget targets. A separated, clearly labeled simulation model was constructed to support budget variance and expense analysis without modifying or falsifying actual historical results.

---

## 2. Dataset Schema & Profile

### Raw Source Profile
| Property | Value |
| :--- | :--- |
| **Source File** | `Financial_Sample.xlsx` |
| **Row Count** | 700 transactions |
| **Raw Column Count** | 16 fields |
| **Temporal Span** | 2013-09-01 to 2014-12-01 (16 months) |
| **Entities Covered** | 5 Countries, 5 Segments, 6 Products, 4 Discount Bands |
| **Total Gross Sales** | $127,931,598.50 |
| **Total Discounts** | $9,205,248.24 |
| **Total Net Sales (Revenue)** | $118,726,350.26 |
| **Total COGS** | $101,832,648.00 |
| **Total Gross Profit** | $16,893,702.26 |
| **Overall Gross Margin %** | 14.23% |

---

## 3. Detailed Data Quality Issues & Remediation

### Issue 1: Whitespace in Column Header
* **Observation:** The net revenue column was formatted as `' Sales'` (with a leading space).
* **Impact:** In SQL queries (`SELECT Sales FROM ...`) and Python dataframes, unstripped whitespace causes `KeyError` or column-not-found exceptions.
* **Remediation:** Automated stripping applied to all column names in `python/data_cleaning.py`. Renamed to standardized snake_case identifier `net_sales`.

### Issue 2: Missing Values in `Discount Band`
* **Observation:** 53 records had `NaN` / blank values in `Discount Band`.
* **Root Cause Analysis:** Transactions without promotional discounting were recorded as blank rather than an explicit categorical string. In standard Python parsers, string `'None'` can also inadvertently be parsed as null.
* **Remediation:** Imputed all 53 null values with `'No Discount'`. Verified that in these 53 transactions, `Discounts` equals `$0.00`, confirming complete business consistency.

### Issue 3: Duplicate Record Audit
* **Observation:** A full-row duplicate check across all 16 fields yielded 0 duplicate records.
* **Conclusion:** All 700 records represent distinct transaction events.

### Issue 4: Primary Key Creation
* **Observation:** The raw source table lacked a unique surrogate primary key.
* **Remediation:** Generated an explicit integer surrogate primary key `transaction_id` (values 1001 to 1700), facilitating relational integrity and fact-dimension indexing.

### Issue 5: Financial Formula Verification
The raw numbers were tested against fundamental accounting identities:

$$\text{Gross Sales} = \text{Units Sold} \times \text{Sale Price}$$
$$\text{Net Sales} = \text{Gross Sales} - \text{Discounts}$$
$$\text{Gross Profit} = \text{Net Sales} - \text{COGS}$$

| Formula Identity | Max Absolute Discrepancy | Result | Status |
| :--- | :--- | :--- | :--- |
| $\text{Units Sold} \times \text{Sale Price} == \text{Gross Sales}$ | $0.0000 | 0 discrepancies | **PASS** |
| $\text{Gross Sales} - \text{Discounts} == \text{Net Sales}$ | $0.0100 | Within 1¢ penny rounding | **PASS** |
| $\text{Net Sales} - \text{COGS} == \text{Gross Profit}$ | $0.0000 | 0 discrepancies | **PASS** |

### Issue 6: Clarification of Profit Metric
* **Observation:** The raw column is labeled `Profit`. However, the mathematical calculation is strictly $\text{Net Sales} - \text{COGS}$.
* **Accounting Reality:** Because operating expenses (SG&A, administrative, marketing, depreciation) are not deducted, this metric is **Gross Profit**, not Net Profit.
* **Remediation:** Renamed to `gross_profit` across all processed tables, SQL views, and Power BI DAX measures to maintain strict GAAP/IFRS conceptual rigor.

---

## 4. Deep-Dive: Loss-Making Commercial Transactions

An analysis of profit distributions uncovered **58 transactions (8.29% of all sales)** that generated negative gross profit.

### Negative Profit Breakdown by Segment
| Segment | Transaction Count | Loss Count | Total Gross Profit ($) | Total Loss ($) | Avg Margin % |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Enterprise** | 100 | **58** | **-$614,545.60** | **-$777,321.25** | **-3.13%** |
| Government | 300 | 0 | +$11,388,173.53 | $0.00 | +21.69% |
| Small Business | 100 | 0 | +$4,143,168.00 | $0.00 | +9.77% |
| Channel Partners | 100 | 0 | +$1,316,803.18 | $0.00 | +73.13% |
| Midmarket | 100 | 0 | +$660,103.15 | $0.00 | +27.71% |

### Negative Profit by Discount Band within Enterprise
| Discount Band | Loss Transaction Count | Total Loss ($) |
| :--- | :--- | :--- |
| **High** | 33 | -$622,368.75 |
| **Medium** | 25 | -$154,952.50 |
| **Low** | 0 | $0.00 |
| **No Discount** | 0 | $0.00 |

* **Root Cause:** Enterprise contracts feature fixed contractual Sale Prices of $125/unit with unit COGS of $120/unit (gross margin before discount is only $5/unit or 4.0%). When Medium (7-10%) or High (10-15%) discounts are applied, the net price drops well below the $120 manufacturing/delivery cost, guaranteeing negative gross margin on every unit delivered.

---

## 5. Architectural Separation of Simulated Datasets

Per project guidelines:
> *"If the source dataset does not contain operating expenses, budget data, or other necessary fields, do not fabricate them or present estimates as actual company financial results. If budget analysis is needed, create a separate, clearly labelled illustrative budget dataset with documented assumptions."*

To satisfy executive requirements for **Expense Analysis (Page 3)** and **Budget vs Actual (Page 4)** without corrupting historical actuals:

1. **`simulated_budget.csv`**:
   - Contains 400 monthly target records across 5 Countries and 5 Segments for 2013-2014.
   - Budget revenue targets are established at +5% over benchmark actuals.
   - Target COGS calibrated at 82% of budget revenue (targeting 18% gross margin).
   - Target Operating Expenses calibrated at 8% of budget revenue.
2. **`simulated_operating_expenses.csv`**:
   - Contains 80 departmental cost allocation records across SG&A (2.5%), Marketing & Advertising (3.5%), Research & Development (1.5%), and IT/Operations (1.0%).
   - Stored in a separate fact table clearly tagged as illustrative departmental OPEX.

---

## 6. Data Validation Audit Summary Table

| # | Validation Audit Item | Test Methodology | Result | Status |
| :-: | :--- | :--- | :--- | :--- |
| **1** | Completeness (Null check) | `df.isnull().sum()` | 0 nulls remaining | **PASS** |
| **2** | Primary Key Integrity | `df['transaction_id'].is_unique` | 700 unique IDs verified | **PASS** |
| **3** | Date Consistency | Min/Max date boundary audit | 2013-09-01 to 2014-12-01 | **PASS** |
| **4** | Gross Sales Accuracy | `abs(gross_sales - units * price)` | Max variance $0.0000 | **PASS** |
| **5** | Net Sales Accuracy | `abs(net_sales - (gross_sales - discounts))` | Max variance $0.0100 (penny rounding) | **PASS** |
| **6** | Gross Profit Accuracy | `abs(gross_profit - (net_sales - cogs))` | Max variance $0.0000 | **PASS** |
| **7** | Star Schema FK Integrity | Fact table key existence in Dimensions | 0 orphan foreign keys | **PASS** |
| **8** | Category Consistency | Domain value set inspection | Clean match across all dimensions | **PASS** |
| **9** | Loss-Making Flagging | Filter `gross_profit < 0` | 58 Enterprise transactions flagged | **AUDITED** |
| **10** | Budget Model Alignment | Foreign key join audit on budget fact | 100% relational referential integrity | **PASS** |

**Conclusion:** The cleaned dataset and dimensional tables meet enterprise quality standards and are fully certified for SQL querying and Power BI report ingestion.

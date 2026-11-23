# Power BI Desktop Implementation & Dashboard Build Guide
**Project:** Financial Performance & Profitability Analysis  
**Target Audience:** Power BI Developers, BI Analysts, Finance Stakeholders  
**Deliverable:** 4-Page Executive Financial BI Solution  

---

## 1. Quick Start & Data Import Steps

To build the interactive report in **Power BI Desktop**, follow these sequential steps:

### Step 1: Ingest Data Files
1. Open **Power BI Desktop**.
2. Click **Get Data** > **Text/CSV**.
3. Browse to the project folder `data/processed/` and import the following 7 files:
   - `dim_date.csv`
   - `dim_product.csv`
   - `dim_country.csv`
   - `dim_segment.csv`
   - `fact_financials.csv`
   - `simulated_budget.csv`
   - `simulated_operating_expenses.csv`
4. Click **Load** (data is already cleaned and schema-validated by Python).

### Step 2: Establish Star Schema Relationships (Model View)
Navigate to the **Model View** and verify/create the following 1-to-many relationships (Single filter direction):
1. `dim_date[date_key]` $\rightarrow$ `fact_financials[date_key]` (`1:*`)
2. `dim_product[product_id]` $\rightarrow$ `fact_financials[product_id]` (`1:*`)
3. `dim_country[country_id]` $\rightarrow$ `fact_financials[country_id]` (`1:*`)
4. `dim_segment[segment_id]` $\rightarrow$ `fact_financials[segment_id]` (`1:*`)
5. `dim_date[date_key]` $\rightarrow$ `fact_budget[date_key]` (`1:*`)
6. `dim_country[country_id]` $\rightarrow$ `fact_budget[country_id]` (`1:*`)
7. `dim_segment[segment_id]` $\rightarrow$ `fact_budget[segment_id]` (`1:*`)
8. `dim_date[date_key]` $\rightarrow$ `fact_operating_expenses[date_key]` (`1:*`)

### Step 3: Column Sorting Configuration
1. Select `dim_date[month_name]` $\rightarrow$ Click **Column Tools** $\rightarrow$ **Sort by Column** $\rightarrow$ Select `month_number`.
2. Select `dim_date[quarter_name]` $\rightarrow$ Sort by `quarter`.

### Step 4: Create Dedicated DAX Measure Table
1. In the **Home** tab, click **Enter Data**.
2. Name the table `_Financial_Measures` and click **Load**.
3. Create all DAX measures documented in [`powerbi/dax_measures.md`](./dax_measures.md).
4. Hide the dummy column `Column1` in `_Financial_Measures`.

---

## 2. Page-by-Page Visual Design Specifications

---

### Page 1: Executive Financial Overview
* **Purpose:** High-level strategic health check for the C-Suite and executive leadership.
* **Top Slicers Panel (Horizontal Bar across top):**
  - **Date Range Slicer:** `dim_date[year]`, `dim_date[month_name]` (Tile / Dropdown)
  - **Country Slicer:** `dim_country[country_name]`
  - **Segment Slicer:** `dim_segment[segment_name]`
  - **Product Slicer:** `dim_product[product_name]`

* **Visual 1 to 5: Executive KPI Cards (Row 1):**
  1. **Total Net Revenue:** `[Total Revenue]` (Display Units: Millions, e.g. `$118.73M`)
  2. **Total COGS:** `[Total COGS]` (Display Units: Millions, e.g. `$101.83M`)
  3. **Gross Profit:** `[Gross Profit]` (Display Units: Millions, e.g. `$16.89M`)
  4. **Gross Margin %:** `[Gross Profit Margin %]` (Format: `14.2%`)
  5. **Revenue YoY Growth %:** `[Revenue YoY Growth %]` (Format: `+62.4%`, Green font)

* **Visual 6: Monthly Financial Trajectory (Line and Clustered Column Chart):**
  - **X-axis:** `dim_date[year_month]` (or `dim_date[month_name]` sorted by month_number)
  - **Column Y-axis:** `[Total Revenue]`, `[Total COGS]`
  - **Line Y-axis:** `[Gross Profit Margin %]`
  - **Data Colors:** Revenue (Blue `#3B82F6`), COGS (Slate `#64748B`), Margin (Emerald `#10B981`)
  - **Data Labels:** Turned ON for Margin line.

* **Visual 7: Profit Contribution by Region (Donut Chart):**
  - **Legend:** `dim_country[country_name]`
  - **Values:** `[Gross Profit]`
  - **Detail Labels:** Category and Percentage of total.

* **Visual 8: Financial Performance by Product Line (Clustered Bar Chart):**
  - **Y-axis:** `dim_product[product_name]`
  - **X-axis:** `[Total Revenue]`, `[Gross Profit]`
  - **Legend:** Metric Name
  - **Tooltips:** `[Gross Profit Margin %]`, `[Total Units Sold]`

---

### Page 2: Profitability Analysis
* **Purpose:** Deep-dive into profit generation, margin conversion, and contract-level value erosion.
* **Header Alert Banner:**
  - Multi-row Card / Callout: *"Attention Management: Enterprise Segment is operating at a -$614K Gross Loss (-3.1% margin) driven by high discounting."*

* **Visual 1: Product Profitability & Ranking (Matrix Table):**
  - **Rows:** `dim_product[product_name]`
  - **Values:** 
    - `[Total Units Sold]`
    - `[Total Revenue]`
    - `[Total COGS]`
    - `[Gross Profit]`
    - `[Gross Profit Margin %]`
    - `[Avg Realized Price per Unit]`
    - `[Avg Cost per Unit]`
  - **Conditional Formatting:** Background color on `[Gross Profit Margin %]` (Color scale: Green $\ge 15\%$, Red $< 10\%$).

* **Visual 2: Top 5 and Bottom 5 Products by Profit (Clustered Bar Chart):**
  - **Y-axis:** `dim_product[product_name]` (Filtered using Top N visual filter: Top 5 / Bottom 5 by `[Gross Profit]`)
  - **X-axis:** `[Gross Profit]`
  - **Data Color:** Rules-based color (`[Gross Profit] >= 0` $\rightarrow$ Green, `< 0` $\rightarrow$ Red)

* **Visual 3: Product Commercial Matrix: Revenue vs Profit Bubble Chart (Scatter Plot):**
  - **X-axis:** `[Total Revenue]`
  - **Y-axis:** `[Gross Profit]`
  - **Size:** `[Total Units Sold]`
  - **Legend:** `dim_product[product_name]`
  - **Zoom / Reference Line:** 15% Margin Target Reference Line.

* **Visual 4: Customer Segment Profitability & Loss Exposure (Waterfall / Clustered Column):**
  - **X-axis:** `dim_segment[segment_name]`
  - **Y-axis:** `[Gross Profit]`
  - **Callout:** Red bar for Enterprise segment (`-$614K`).

* **Visual 5: Discount Band Margin Erosion (Line and Clustered Column):**
  - **X-axis:** `fact_financials[discount_band]` (Ordered: No Discount, Low, Medium, High)
  - **Column Y-axis:** `[Total Discounts]`, `[Gross Profit]`
  - **Line Y-axis:** `[Gross Profit Margin %]`

---

### Page 3: Expense & Cost Structure Analysis
* **Purpose:** Analyze corporate expenditure, COGS burden, and departmental operating expenses.
* **Top KPI Cards:**
  1. **Total Cost Base:** `[Total COGS] + [Total Discounts]` ($111.04M)
  2. **COGS Ratio:** `DIVIDE([Total COGS], [Total Gross Sales])` (79.6%)
  3. **Promotional Concessions (Discounts):** `[Total Discounts]` ($9.21M, 7.2% of Gross Sales)
  4. **Operating Expenses (Illustrative OPEX):** `[Total Operating Expenses]` ($10.69M)

* **Visual 1: Cost Distribution: Direct COGS vs Commercial Discounts (100% Stacked Bar):**
  - **Y-axis:** `dim_segment[segment_name]`
  - **X-axis:** `[Total COGS]`, `[Total Discounts]`
  - **Color:** COGS (Slate Gray `#64748B`), Discounts (Amber Gold `#F59E0B`)

* **Visual 2: Monthly Cost Trajectory (Stacked Area Chart):**
  - **X-axis:** `dim_date[year_month]`
  - **Y-axis:** `[Total COGS]`, `[Total Discounts]`
  - **Legend:** Cost Category

* **Visual 3: Departmental Operating Expense Breakdown (Donut Chart - Illustrative):**
  - **Legend:** OPEX Department (`Marketing & Advertising`, `SG&A`, `R&D`, `IT Operations`)
  - **Values:** `[Total Operating Expenses]`
  - **Subtitle Note:** *"Based on illustrative enterprise operational cost allocation model."*

* **Visual 4: Revenue Growth vs Cost Growth (Line Chart):**
  - **X-axis:** `dim_date[year_month]`
  - **Y-axis:** `[Revenue MoM Growth %]`, `MoM Cost Growth %`
  - **Purpose:** Identifies operational jaws (periods where cost expansion outpaced revenue growth).

---

### Page 4: Budget vs Actual Variance Analysis
* **Purpose:** Management accountability report comparing actual commercial execution against budget targets.
* **Top Variance KPI Cards:**
  1. **Actual Revenue:** `[Total Revenue]` ($118.73M)
  2. **Budget Revenue Target:** `[Budget Revenue]` ($124.66M)
  3. **Revenue Budget Variance:** `[Revenue Budget Variance]` (-$5.93M, Red)
  4. **Budget Achievement Rate:** `[Revenue Target Achievement %]` (95.2%, Amber)
  5. **Profit Budget Variance:** `[Profit Budget Variance]` (-$5.55M, Red)

* **Visual 1: Actual vs Budget Revenue by Segment (Bullet Chart / Clustered Bar):**
  - **Y-axis:** `dim_segment[segment_name]`
  - **X-axis:** `[Total Revenue]` (Bar), `[Budget Revenue]` (Marker line or secondary bar)
  - **Data Labels:** `[Revenue Target Achievement %]`

* **Visual 2: Monthly Budget Variance Waterfall Chart:**
  - **Category:** `dim_date[year_month]`
  - **Y-axis:** `[Revenue Budget Variance]`
  - **Sentiment Colors:** Favorable (Green), Unfavorable (Red)

* **Visual 3: Budget vs Actual Profitability Matrix (Table with Data Bars):**
  - **Rows:** `dim_country[country_name]`, `dim_segment[segment_name]`
  - **Values:**
    - `[Total Revenue]`
    - `[Budget Revenue]`
    - `[Revenue Budget Variance]`
    - `[Revenue Budget Variance %]`
    - `[Gross Profit]`
    - `[Budget Gross Profit]`
    - `[Profit Budget Variance %]`
  - **Conditional Formatting:** Red/Green icon indicators on Variance % columns.

---

## 3. Theme & Styling Guidelines

* **Color Palette:**
  - **Primary Corporate:** Navy `#1E293B`
  - **Revenue / Primary Action:** Royal Blue `#3B82F6`
  - **Cost / Baseline:** Slate Gray `#64748B`
  - **Favorable / Profit:** Emerald Green `#10B981`
  - **Unfavorable / Deficit / Loss:** Crimson Red `#EF4444`
  - **Warning / Promotional Discount:** Amber Gold `#F59E0B`
* **Canvas Settings:** 16:9 ratio (1280 × 720 px), Light Gray background `#F8FAFC`.
* **Typography:** Segoe UI or Arial throughout all visuals, KPI callout numbers 24-28pt bold, visual titles 12-14pt bold.

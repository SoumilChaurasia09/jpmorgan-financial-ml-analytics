# Power BI Data Model Architecture & Star Schema Design
**Project:** Financial Performance & Profitability Analysis  
**Architecture Type:** Enterprise Kimball Star Schema  
**Target BI Tool:** Microsoft Power BI Desktop / Power BI Service  

---

## 1. Architectural Overview & Star Schema Diagram

The data model is engineered following Kimball dimensional modeling best practices to optimize query performance, simplify DAX measure calculation, and prevent ambiguity in filter propagation.

```mermaid
erDiagram
    dim_date ||--o{ fact_financials : "date_key (1:M)"
    dim_date ||--o{ fact_budget : "date_key (1:M)"
    dim_date ||--o{ fact_operating_expenses : "date_key (1:M)"
    dim_product ||--o{ fact_financials : "product_id (1:M)"
    dim_country ||--o{ fact_financials : "country_id (1:M)"
    dim_country ||--o{ fact_budget : "country_id (1:M)"
    dim_segment ||--o{ fact_financials : "segment_id (1:M)"
    dim_segment ||--o{ fact_budget : "segment_id (1:M)"

    dim_date {
        int date_key PK
        date date
        int year
        int quarter
        string quarter_name
        int month_number
        string month_name
        string month_short
        string year_month
        int is_weekend
    }

    dim_product {
        string product_id PK
        string product_name
        decimal standard_manufacturing_price
    }

    dim_country {
        string country_id PK
        string country_name
        string region
    }

    dim_segment {
        string segment_id PK
        string segment_name
        string channel_type
    }

    fact_financials {
        int transaction_id PK
        int date_key FK
        string product_id FK
        string country_id FK
        string segment_id FK
        string discount_band
        decimal units_sold
        decimal sale_price
        decimal gross_sales
        decimal discounts
        decimal net_sales
        decimal cogs
        decimal gross_profit
        decimal gross_margin_pct
    }

    fact_budget {
        string budget_id PK
        int date_key FK
        string country_id FK
        string segment_id FK
        decimal budget_revenue
        decimal budget_cogs
        decimal budget_gross_profit
    }

    fact_operating_expenses {
        int date_key FK
        string segment_name
        decimal marketing_advertising
        decimal selling_general_admin
        decimal research_development
        decimal it_operations
        decimal total_operating_expenses
    }
```

---

## 2. Table Classifications & Cardinality

| Table Name | Role | Primary Key | Foreign Keys | Granularity | Cross-Filter Direction |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`dim_date`** | Conformed Dimension | `date_key` | None | 1 Row per Calendar Day | Single (`1` to `*`) |
| **`dim_product`** | Dimension | `product_id` | None | 1 Row per Commercial Product Line | Single (`1` to `*`) |
| **`dim_country`** | Dimension | `country_id` | None | 1 Row per Global Market Country | Single (`1` to `*`) |
| **`dim_segment`** | Dimension | `segment_id` | None | 1 Row per Customer Market Segment | Single (`1` to `*`) |
| **`fact_financials`** | Core Fact | `transaction_id` | `date_key`, `product_id`, `country_id`, `segment_id` | 1 Row per Commercial Sales Transaction | Target |
| **`fact_budget`** | Illustrative Target Fact | `budget_id` | `date_key`, `country_id`, `segment_id` | 1 Row per Month × Country × Segment | Target |
| **`fact_operating_expenses`** | Illustrative Cost Fact | Composite (`date_key`, `segment_name`) | `date_key` | 1 Row per Month × Segment | Target |

---

## 3. Data Modeling Principles & Optimization Rules

1. **Strict 1-to-Many Relationships with Single-Direction Filtering:**
   - All relationships originate from the **1-side** (Dimension tables) and propagate to the **Many-side** (`fact_financials` / `fact_budget`).
   - Bidirectional cross-filtering is strictly disabled to avoid circular dependencies and unexpected filter context inflation.
2. **Dedicated Date Dimension:**
   - Auto Date/Time in Power BI Desktop options is disabled to reduce file size and ensure precise time-intelligence calculations (`SAMEPERIODLASTYEAR`, `TOTALYTD`).
   - `month_name` is explicitly set to sort by `month_number`.
   - `quarter_name` is set to sort by `quarter`.
3. **Dedicated Measure Table:**
   - All DAX calculations reside in `_Financial_Measures`. No naked aggregations (e.g. dragging raw numeric columns into visuals) are used.
4. **Hiding Foreign Keys:**
   - Key columns in the fact tables (`date_key`, `product_id`, `country_id`, `segment_id`) are hidden from the Report View to prevent end-users from accidentally aggregating keys or slicing from fact attributes.
5. **Separation of Actuals vs Simulated Models:**
   - Actual operational results reside in `fact_financials`.
   - Budget targets reside in `fact_budget`.
   - Operating expense line-items reside in `fact_operating_expenses`.
   - Measures combine these seamlessly in DAX (`[Total Revenue] - [Budget Revenue]`).

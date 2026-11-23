-- ============================================================================
-- Project: Financial Performance & Profitability Analysis
-- Script: views.sql
-- Description: Analytical Database Views for Power BI Reporting & BI Dashboards
-- Compatible with: PostgreSQL, MySQL 8.0+, SQLite, Microsoft SQL Server
-- ============================================================================

-- ----------------------------------------------------------------------------
-- VIEW 1: Executive Monthly Financial Summary
-- Pre-aggregates monthly corporate KPIs for fast dashboard rendering
-- ----------------------------------------------------------------------------
DROP VIEW IF EXISTS vw_monthly_financial_summary;
CREATE VIEW vw_monthly_financial_summary AS
SELECT 
    d.year,
    d.quarter,
    d.quarter_name,
    d.month_number,
    d.month_name,
    d.year_month,
    ROUND(SUM(f.units_sold), 0)                                              AS total_units_sold,
    ROUND(SUM(f.gross_sales), 2)                                             AS gross_sales,
    ROUND(SUM(f.discounts), 2)                                               AS total_discounts,
    ROUND(SUM(f.net_sales), 2)                                                AS net_revenue,
    ROUND(SUM(f.cogs), 2)                                                     AS total_cogs,
    ROUND(SUM(f.gross_profit), 2)                                             AS gross_profit,
    ROUND((SUM(f.gross_profit) * 100.0) / NULLIF(SUM(f.net_sales), 0), 2)      AS gross_margin_pct,
    ROUND((SUM(f.discounts) * 100.0) / NULLIF(SUM(f.gross_sales), 0), 2)     AS discount_rate_pct
FROM fact_financials f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.quarter, d.quarter_name, d.month_number, d.month_name, d.year_month;

-- ----------------------------------------------------------------------------
-- VIEW 2: Product Commercial Profitability
-- Provides product-level financial metrics, unit economics, and margins
-- ----------------------------------------------------------------------------
DROP VIEW IF EXISTS vw_product_profitability;
CREATE VIEW vw_product_profitability AS
SELECT 
    p.product_id,
    p.product_name,
    p.standard_manufacturing_price,
    ROUND(SUM(f.units_sold), 0)                                              AS total_units_sold,
    ROUND(SUM(f.gross_sales), 2)                                             AS gross_sales,
    ROUND(SUM(f.discounts), 2)                                               AS total_discounts,
    ROUND(SUM(f.net_sales), 2)                                                AS net_revenue,
    ROUND(SUM(f.cogs), 2)                                                     AS total_cogs,
    ROUND(SUM(f.gross_profit), 2)                                             AS gross_profit,
    ROUND((SUM(f.gross_profit) * 100.0) / NULLIF(SUM(f.net_sales), 0), 2)      AS gross_margin_pct,
    ROUND(SUM(f.net_sales) / NULLIF(SUM(f.units_sold), 0), 2)                AS avg_realized_price_per_unit,
    ROUND(SUM(f.cogs) / NULLIF(SUM(f.units_sold), 0), 2)                     AS avg_cost_per_unit
FROM fact_financials f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.standard_manufacturing_price;

-- ----------------------------------------------------------------------------
-- VIEW 3: Regional & Country Performance
-- Summarizes financial performance by geographic region and country
-- ----------------------------------------------------------------------------
DROP VIEW IF EXISTS vw_regional_performance;
CREATE VIEW vw_regional_performance AS
SELECT 
    c.country_id,
    c.country_name,
    c.region,
    ROUND(SUM(f.units_sold), 0)                                              AS total_units_sold,
    ROUND(SUM(f.net_sales), 2)                                                AS net_revenue,
    ROUND(SUM(f.cogs), 2)                                                     AS total_cogs,
    ROUND(SUM(f.gross_profit), 2)                                             AS gross_profit,
    ROUND((SUM(f.gross_profit) * 100.0) / NULLIF(SUM(f.net_sales), 0), 2)      AS gross_margin_pct,
    ROUND(
        (SUM(f.gross_profit) * 100.0) / SUM(SUM(f.gross_profit)) OVER (), 
        2
    ) AS pct_global_profit_share
FROM fact_financials f
JOIN dim_country c ON f.country_id = c.country_id
GROUP BY c.country_id, c.country_name, c.region;

-- ----------------------------------------------------------------------------
-- VIEW 4: Customer Segment Commercial Performance
-- Delivers customer segment contribution, margins, and loss-making exposure
-- ----------------------------------------------------------------------------
DROP VIEW IF EXISTS vw_segment_performance;
CREATE VIEW vw_segment_performance AS
SELECT 
    s.segment_id,
    s.segment_name,
    s.channel_type,
    ROUND(SUM(f.units_sold), 0)                                              AS total_units_sold,
    ROUND(SUM(f.net_sales), 2)                                                AS net_revenue,
    ROUND(SUM(f.cogs), 2)                                                     AS total_cogs,
    ROUND(SUM(f.gross_profit), 2)                                             AS gross_profit,
    ROUND((SUM(f.gross_profit) * 100.0) / NULLIF(SUM(f.net_sales), 0), 2)      AS gross_margin_pct,
    SUM(CASE WHEN f.gross_profit < 0 THEN 1 ELSE 0 END)                      AS loss_making_transactions_count,
    ROUND(SUM(CASE WHEN f.gross_profit < 0 THEN f.gross_profit ELSE 0 END), 2) AS total_contract_loss_amount
FROM fact_financials f
JOIN dim_segment s ON f.segment_id = s.segment_id
GROUP BY s.segment_id, s.segment_name, s.channel_type;

-- ----------------------------------------------------------------------------
-- VIEW 5: Budget vs Actual Performance
-- Integrated comparison view linking monthly actuals to budget targets
-- ----------------------------------------------------------------------------
DROP VIEW IF EXISTS vw_budget_vs_actual;
CREATE VIEW vw_budget_vs_actual AS
WITH actual_agg AS (
    SELECT 
        f.date_key,
        f.country_id,
        f.segment_id,
        SUM(f.net_sales)    AS actual_revenue,
        SUM(f.cogs)         AS actual_cogs,
        SUM(f.gross_profit) AS actual_gross_profit
    FROM fact_financials f
    GROUP BY f.date_key, f.country_id, f.segment_id
)
SELECT 
    b.budget_id,
    b.date_key,
    d.year,
    d.quarter_name,
    d.month_number,
    d.month_name,
    c.country_name,
    c.region,
    s.segment_name,
    ROUND(COALESCE(a.actual_revenue, 0), 2)      AS actual_revenue,
    ROUND(b.budget_revenue, 2)                   AS budget_revenue,
    ROUND(COALESCE(a.actual_revenue, 0) - b.budget_revenue, 2) AS revenue_variance,
    ROUND(
        ((COALESCE(a.actual_revenue, 0) - b.budget_revenue) * 100.0) 
        / NULLIF(b.budget_revenue, 0), 
        2
    ) AS revenue_variance_pct,
    ROUND(COALESCE(a.actual_gross_profit, 0), 2)  AS actual_profit,
    ROUND(b.budget_gross_profit, 2)              AS budget_profit,
    ROUND(COALESCE(a.actual_gross_profit, 0) - b.budget_gross_profit, 2) AS profit_variance,
    ROUND(
        (COALESCE(a.actual_revenue, 0) * 100.0) / NULLIF(b.budget_revenue, 0), 
        2
    ) AS target_achievement_pct
FROM fact_budget b
JOIN dim_date d ON b.date_key = d.date_key
JOIN dim_country c ON b.country_id = c.country_id
JOIN dim_segment s ON b.segment_id = s.segment_id
LEFT JOIN actual_agg a 
    ON b.date_key = a.date_key 
   AND b.country_id = a.country_id 
   AND b.segment_id = a.segment_id;

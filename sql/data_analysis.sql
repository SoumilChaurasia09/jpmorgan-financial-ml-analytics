-- ============================================================================
-- Project: Financial Performance & Profitability Analysis
-- Script: data_analysis.sql
-- Description: Core Analytical Queries, CTEs, Window Functions, and Financial KPIs
-- Compatible with: PostgreSQL, MySQL 8.0+, SQLite, Microsoft SQL Server
-- ============================================================================

-- ============================================================================
-- QUERY 1: Executive Financial Summary (Overall Business KPIs)
-- Business Question: What is the company's total revenue, total cost, and profit?
-- ============================================================================
SELECT 
    ROUND(SUM(f.gross_sales), 2)                                            AS total_gross_sales,
    ROUND(SUM(f.discounts), 2)                                              AS total_discounts,
    ROUND(SUM(f.net_sales), 2)                                               AS total_net_revenue,
    ROUND(SUM(f.cogs), 2)                                                    AS total_cogs,
    ROUND(SUM(f.gross_profit), 2)                                            AS total_gross_profit,
    ROUND((SUM(f.gross_profit) * 100.0) / NULLIF(SUM(f.net_sales), 0), 2)     AS overall_gross_margin_pct,
    ROUND((SUM(f.discounts) * 100.0) / NULLIF(SUM(f.gross_sales), 0), 2)    AS overall_discount_rate_pct
FROM fact_financials f;

-- ============================================================================
-- QUERY 2: Monthly Revenue, Cost, and Profit Trends with Month-over-Month Growth
-- Business Question: How has financial performance changed month-over-month?
-- ============================================================================
WITH monthly_metrics AS (
    SELECT 
        d.year,
        d.month_number,
        d.month_name,
        d.year_month,
        ROUND(SUM(f.net_sales), 2)     AS monthly_revenue,
        ROUND(SUM(f.cogs), 2)          AS monthly_cogs,
        ROUND(SUM(f.gross_profit), 2)  AS monthly_profit,
        ROUND((SUM(f.gross_profit) * 100.0) / NULLIF(SUM(f.net_sales), 0), 2) AS gross_margin_pct
    FROM fact_financials f
    JOIN dim_date d ON f.date_key = d.date_key
    GROUP BY d.year, d.month_number, d.month_name, d.year_month
)
SELECT 
    year,
    month_number,
    month_name,
    year_month,
    monthly_revenue,
    monthly_cogs,
    monthly_profit,
    gross_margin_pct,
    -- Previous Month Revenue using LAG window function
    LAG(monthly_revenue, 1) OVER (ORDER BY year, month_number) AS prev_month_revenue,
    -- Month-over-Month Revenue Growth %
    ROUND(
        ((monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY year, month_number)) * 100.0) 
        / NULLIF(LAG(monthly_revenue, 1) OVER (ORDER BY year, month_number), 0), 
        2
    ) AS mom_revenue_growth_pct,
    -- Month-over-Month Profit Growth %
    ROUND(
        ((monthly_profit - LAG(monthly_profit, 1) OVER (ORDER BY year, month_number)) * 100.0) 
        / NULLIF(LAG(monthly_profit, 1) OVER (ORDER BY year, month_number), 0), 
        2
    ) AS mom_profit_growth_pct
FROM monthly_metrics
ORDER BY year, month_number;

-- ============================================================================
-- QUERY 3: Year-over-Year (YoY) Financial Performance Comparison (Sep-Dec 2013 vs 2014)
-- Business Question: How does revenue and profit compare across years for matching periods?
-- ============================================================================
WITH annual_month_summary AS (
    SELECT 
        d.month_number,
        d.month_name,
        d.year,
        SUM(f.net_sales)    AS net_revenue,
        SUM(f.gross_profit) AS gross_profit
    FROM fact_financials f
    JOIN dim_date d ON f.date_key = d.date_key
    WHERE d.month_number IN (9, 10, 11, 12) -- Overlapping operational months in 2013 and 2014
    GROUP BY d.month_number, d.month_name, d.year
)
SELECT 
    m2014.month_number,
    m2014.month_name,
    ROUND(m2013.net_revenue, 2)     AS revenue_2013,
    ROUND(m2014.net_revenue, 2)     AS revenue_2014,
    ROUND(m2014.net_revenue - m2013.net_revenue, 2) AS yoy_revenue_variance,
    ROUND(((m2014.net_revenue - m2013.net_revenue) * 100.0) / NULLIF(m2013.net_revenue, 0), 2) AS yoy_revenue_growth_pct,
    ROUND(m2013.gross_profit, 2)    AS profit_2013,
    ROUND(m2014.gross_profit, 2)    AS profit_2014,
    ROUND(m2014.gross_profit - m2013.gross_profit, 2) AS yoy_profit_variance,
    ROUND(((m2014.gross_profit - m2013.gross_profit) * 100.0) / NULLIF(m2013.gross_profit, 0), 2) AS yoy_profit_growth_pct
FROM (SELECT * FROM annual_month_summary WHERE year = 2014) m2014
LEFT JOIN (SELECT * FROM annual_month_summary WHERE year = 2013) m2013 
    ON m2014.month_number = m2013.month_number
ORDER BY m2014.month_number;

-- ============================================================================
-- QUERY 4: Product Profitability & Commercial Ranking
-- Business Question: Which products generate the highest profit and margins?
-- ============================================================================
SELECT 
    p.product_name,
    p.standard_manufacturing_price,
    ROUND(SUM(f.units_sold), 0)                                              AS total_units_sold,
    ROUND(SUM(f.net_sales), 2)                                               AS total_revenue,
    ROUND(SUM(f.cogs), 2)                                                    AS total_cogs,
    ROUND(SUM(f.gross_profit), 2)                                            AS total_gross_profit,
    ROUND((SUM(f.gross_profit) * 100.0) / NULLIF(SUM(f.net_sales), 0), 2)     AS gross_margin_pct,
    RANK() OVER (ORDER BY SUM(f.gross_profit) DESC)                          AS profit_rank,
    RANK() OVER (ORDER BY (SUM(f.gross_profit) * 100.0) / NULLIF(SUM(f.net_sales), 0) DESC) AS margin_rank
FROM fact_financials f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.product_name, p.standard_manufacturing_price
ORDER BY total_gross_profit DESC;

-- ============================================================================
-- QUERY 5: Geographic & Regional Performance Analysis
-- Business Question: Which regions generate the highest profit and how do margins compare?
-- ============================================================================
SELECT 
    c.region,
    c.country_name,
    ROUND(SUM(f.net_sales), 2)                                               AS total_revenue,
    ROUND(SUM(f.cogs), 2)                                                    AS total_cogs,
    ROUND(SUM(f.gross_profit), 2)                                            AS total_gross_profit,
    ROUND((SUM(f.gross_profit) * 100.0) / NULLIF(SUM(f.net_sales), 0), 2)     AS gross_margin_pct,
    -- Regional Contribution to Global Profit
    ROUND(
        (SUM(f.gross_profit) * 100.0) / SUM(SUM(f.gross_profit)) OVER (), 
        2
    ) AS pct_share_of_global_profit
FROM fact_financials f
JOIN dim_country c ON f.country_id = c.country_id
GROUP BY c.region, c.country_name
ORDER BY total_gross_profit DESC;

-- ============================================================================
-- QUERY 6: Customer Segment Profitability & Commercial Contribution
-- Business Question: Which segments are driving profitability and which are eroding value?
-- ============================================================================
SELECT 
    s.segment_name,
    s.channel_type,
    ROUND(SUM(f.units_sold), 0)                                              AS total_units_sold,
    ROUND(SUM(f.net_sales), 2)                                               AS total_net_revenue,
    ROUND(SUM(f.cogs), 2)                                                    AS total_cogs,
    ROUND(SUM(f.gross_profit), 2)                                            AS total_gross_profit,
    ROUND((SUM(f.gross_profit) * 100.0) / NULLIF(SUM(f.net_sales), 0), 2)     AS gross_margin_pct,
    -- Percentage of Total Corporate Revenue
    ROUND(
        (SUM(f.net_sales) * 100.0) / SUM(SUM(f.net_sales)) OVER (), 
        2
    ) AS pct_revenue_contribution,
    -- Percentage of Total Corporate Profit
    ROUND(
        (SUM(f.gross_profit) * 100.0) / SUM(SUM(f.gross_profit)) OVER (), 
        2
    ) AS pct_profit_contribution
FROM fact_financials f
JOIN dim_segment s ON f.segment_id = s.segment_id
GROUP BY s.segment_name, s.channel_type
ORDER BY total_gross_profit DESC;

-- ============================================================================
-- QUERY 7: Cost & Expense Analysis by Category (Direct Costs & OPEX)
-- Business Question: Which expense categories contribute most to total costs?
-- ============================================================================
-- Part A: Direct Cost Breakdown (COGS vs Promotional Discounts) from Fact Financials
SELECT 
    'Direct COGS'                                                           AS cost_category,
    'Cost of Goods Sold'                                                    AS cost_type,
    ROUND(SUM(cogs), 2)                                                     AS total_amount,
    ROUND((SUM(cogs) * 100.0) / (SUM(cogs) + SUM(discounts)), 2)           AS pct_of_direct_cost_base
FROM fact_financials
UNION ALL
SELECT 
    'Commercial Discount'                                                   AS cost_category,
    'Revenue Reduction / Discount'                                          AS cost_type,
    ROUND(SUM(discounts), 2)                                                AS total_amount,
    ROUND((SUM(discounts) * 100.0) / (SUM(cogs) + SUM(discounts)), 2)      AS pct_of_direct_cost_base
FROM fact_financials;

-- Part B: Departmental Operating Expenses (from illustrative OPEX model)
SELECT 
    'Marketing & Advertising'   AS expense_category,
    ROUND(SUM(marketing_advertising), 2) AS total_expense,
    ROUND((SUM(marketing_advertising) * 100.0) / SUM(total_operating_expenses), 2) AS pct_of_opex
FROM fact_operating_expenses
UNION ALL
SELECT 
    'Selling, General & Admin (SG&A)' AS expense_category,
    ROUND(SUM(selling_general_admin), 2) AS total_expense,
    ROUND((SUM(selling_general_admin) * 100.0) / SUM(total_operating_expenses), 2) AS pct_of_opex
FROM fact_operating_expenses
UNION ALL
SELECT 
    'Research & Development (R&D)' AS expense_category,
    ROUND(SUM(research_development), 2) AS total_expense,
    ROUND((SUM(research_development) * 100.0) / SUM(total_operating_expenses), 2) AS pct_of_opex
FROM fact_operating_expenses
UNION ALL
SELECT 
    'IT & Technical Operations' AS expense_category,
    ROUND(SUM(it_operations), 2) AS total_expense,
    ROUND((SUM(it_operations) * 100.0) / SUM(total_operating_expenses), 2) AS pct_of_opex
FROM fact_operating_expenses
ORDER BY total_expense DESC;

-- ============================================================================
-- QUERY 8: Top 5 and Bottom 5 Products by Profit (CTE + Window Functions)
-- Business Question: What are the highest and lowest performing products?
-- ============================================================================
WITH ranked_products AS (
    SELECT 
        p.product_name,
        ROUND(SUM(f.net_sales), 2)    AS net_revenue,
        ROUND(SUM(f.gross_profit), 2) AS gross_profit,
        ROUND((SUM(f.gross_profit) * 100.0) / NULLIF(SUM(f.net_sales), 0), 2) AS gross_margin_pct,
        DENSE_RANK() OVER (ORDER BY SUM(f.gross_profit) DESC) AS rank_highest,
        DENSE_RANK() OVER (ORDER BY SUM(f.gross_profit) ASC)  AS rank_lowest
    FROM fact_financials f
    JOIN dim_product p ON f.product_id = p.product_id
    GROUP BY p.product_name
)
SELECT 
    'Top 5 Product' AS performance_tier,
    product_name,
    net_revenue,
    gross_profit,
    gross_margin_pct,
    rank_highest AS tier_rank
FROM ranked_products
WHERE rank_highest <= 5
UNION ALL
SELECT 
    'Bottom 5 Product' AS performance_tier,
    product_name,
    net_revenue,
    gross_profit,
    gross_margin_pct,
    rank_lowest AS tier_rank
FROM ranked_products
WHERE rank_lowest <= 5
ORDER BY performance_tier DESC, tier_rank ASC;

-- ============================================================================
-- QUERY 9: Budget vs Actual Variance Analysis (Revenue & Profit Targets)
-- Business Question: Is the company meeting its financial targets? Where are largest variances?
-- ============================================================================
WITH actual_monthly AS (
    SELECT 
        date_key,
        country_id,
        segment_id,
        SUM(net_sales)    AS actual_revenue,
        SUM(cogs)         AS actual_cogs,
        SUM(gross_profit) AS actual_gross_profit
    FROM fact_financials
    GROUP BY date_key, country_id, segment_id
),
budget_variance_calc AS (
    SELECT 
        b.year,
        b.month_number,
        s.segment_name,
        c.country_name,
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
    JOIN dim_segment s ON b.segment_id = s.segment_id
    JOIN dim_country c ON b.country_id = c.country_id
    LEFT JOIN actual_monthly a 
        ON b.date_key = a.date_key 
       AND b.country_id = a.country_id 
       AND b.segment_id = a.segment_id
)
SELECT 
    year,
    segment_name,
    ROUND(SUM(actual_revenue), 2)        AS total_actual_revenue,
    ROUND(SUM(budget_revenue), 2)        AS total_budget_revenue,
    ROUND(SUM(revenue_variance), 2)      AS total_revenue_variance,
    ROUND((SUM(revenue_variance) * 100.0) / NULLIF(SUM(budget_revenue), 0), 2) AS overall_rev_variance_pct,
    ROUND(SUM(actual_profit), 2)         AS total_actual_profit,
    ROUND(SUM(budget_profit), 2)         AS total_budget_profit,
    ROUND(SUM(profit_variance), 2)       AS total_profit_variance,
    ROUND((SUM(actual_revenue) * 100.0) / NULLIF(SUM(budget_revenue), 0), 2)   AS overall_target_achievement_pct
FROM budget_variance_calc
GROUP BY year, segment_name
ORDER BY year, total_revenue_variance ASC;

-- ============================================================================
-- QUERY 10: Window Function Financial Ranking across Months
-- Business Question: How do individual operating months rank within each calendar year?
-- ============================================================================
SELECT 
    d.year,
    d.month_name,
    ROUND(SUM(f.net_sales), 2)     AS monthly_revenue,
    ROUND(SUM(f.gross_profit), 2)  AS monthly_profit,
    ROUND((SUM(f.gross_profit) * 100.0) / NULLIF(SUM(f.net_sales), 0), 2) AS margin_pct,
    DENSE_RANK() OVER (PARTITION BY d.year ORDER BY SUM(f.net_sales) DESC)     AS revenue_rank_in_year,
    DENSE_RANK() OVER (PARTITION BY d.year ORDER BY SUM(f.gross_profit) DESC)  AS profit_rank_in_year
FROM fact_financials f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month_name, d.month_number
ORDER BY d.year, revenue_rank_in_year;

-- ============================================================================
-- QUERY 11: Multi-Tier Transaction Profitability Stratification (CTE Analysis)
-- Business Question: What volume of sales generates healthy margins vs loss-making contracts?
-- ============================================================================
WITH transaction_tiers AS (
    SELECT 
        transaction_id,
        net_sales,
        gross_profit,
        gross_margin_pct,
        CASE 
            WHEN gross_profit < 0 THEN 'Loss-Making (< 0%)'
            WHEN gross_margin_pct < 10.0 THEN 'Low Margin (0% - 10%)'
            WHEN gross_margin_pct <= 25.0 THEN 'Moderate Margin (10% - 25%)'
            ELSE 'High Margin (> 25%)'
        END AS margin_tier
    FROM fact_financials
)
SELECT 
    margin_tier,
    COUNT(transaction_id)                                                     AS transaction_count,
    ROUND((COUNT(transaction_id) * 100.0) / (SELECT COUNT(*) FROM fact_financials), 2) AS pct_of_transactions,
    ROUND(SUM(net_sales), 2)                                                  AS total_revenue,
    ROUND((SUM(net_sales) * 100.0) / (SELECT SUM(net_sales) FROM fact_financials), 2)   AS pct_of_revenue,
    ROUND(SUM(gross_profit), 2)                                               AS total_gross_profit,
    ROUND((SUM(gross_profit) * 100.0) / NULLIF(SUM(net_sales), 0), 2)         AS tier_margin_pct
FROM transaction_tiers
GROUP BY margin_tier
ORDER BY total_gross_profit DESC;

-- ============================================================================
-- QUERY 12: Cumulative / Running Total Financial Growth
-- Business Question: What is the cumulative trajectory of revenue and profit over time?
-- ============================================================================
WITH monthly_rollup AS (
    SELECT 
        d.date,
        d.year_month,
        SUM(f.net_sales)    AS monthly_sales,
        SUM(f.gross_profit) AS monthly_profit
    FROM fact_financials f
    JOIN dim_date d ON f.date_key = d.date_key
    GROUP BY d.date, d.year_month
)
SELECT 
    date,
    year_month,
    ROUND(monthly_sales, 2)  AS monthly_sales,
    ROUND(monthly_profit, 2) AS monthly_profit,
    -- Running Cumulative Net Sales
    ROUND(SUM(monthly_sales) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2)  AS cumulative_net_sales,
    -- Running Cumulative Gross Profit
    ROUND(SUM(monthly_profit) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS cumulative_gross_profit,
    -- Running Corporate Margin
    ROUND(
        (SUM(monthly_profit) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) * 100.0)
        / NULLIF(SUM(monthly_sales) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 0),
        2
    ) AS cumulative_margin_pct
FROM monthly_rollup
ORDER BY date;

-- ============================================================================
-- QUERY 13: Discount Band Impact on Profit Margin
-- Business Question: Are aggressive discount bands eroding product profitability?
-- ============================================================================
SELECT 
    discount_band,
    COUNT(transaction_id)                                                     AS transaction_count,
    ROUND(SUM(units_sold), 0)                                                 AS total_units,
    ROUND(SUM(gross_sales), 2)                                                AS gross_sales,
    ROUND(SUM(discounts), 2)                                                  AS total_discounts_granted,
    ROUND((SUM(discounts) * 100.0) / NULLIF(SUM(gross_sales), 0), 2)          AS effective_discount_rate_pct,
    ROUND(SUM(net_sales), 2)                                                  AS net_sales,
    ROUND(SUM(gross_profit), 2)                                               AS gross_profit,
    ROUND((SUM(gross_profit) * 100.0) / NULLIF(SUM(net_sales), 0), 2)         AS realized_gross_margin_pct
FROM fact_financials
GROUP BY discount_band
ORDER BY effective_discount_rate_pct ASC;

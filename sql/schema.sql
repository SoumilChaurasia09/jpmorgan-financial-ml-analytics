-- ============================================================================
-- Project: Financial Performance & Profitability Analysis
-- Script: schema.sql
-- Description: DDL Schema definitions for relational Star Schema database
-- Compatible with: PostgreSQL, MySQL 8.0+, Microsoft SQL Server, SQLite
-- ============================================================================

-- Drop tables if they already exist (in reverse dependency order)
DROP TABLE IF EXISTS fact_operating_expenses;
DROP TABLE IF EXISTS fact_budget;
DROP TABLE IF EXISTS fact_financials;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_segment;
DROP TABLE IF EXISTS dim_country;
DROP TABLE IF EXISTS dim_product;

-- ----------------------------------------------------------------------------
-- 1. Dimension: Products
-- ----------------------------------------------------------------------------
CREATE TABLE dim_product (
    product_id                  VARCHAR(10)     PRIMARY KEY,
    product_name                VARCHAR(50)     NOT NULL UNIQUE,
    standard_manufacturing_price DECIMAL(10,2)   NOT NULL
);

-- ----------------------------------------------------------------------------
-- 2. Dimension: Countries & Regions
-- ----------------------------------------------------------------------------
CREATE TABLE dim_country (
    country_id                  VARCHAR(10)     PRIMARY KEY,
    country_name                VARCHAR(50)     NOT NULL UNIQUE,
    region                      VARCHAR(50)     NOT NULL
);

-- ----------------------------------------------------------------------------
-- 3. Dimension: Customer Segments
-- ----------------------------------------------------------------------------
CREATE TABLE dim_segment (
    segment_id                  VARCHAR(10)     PRIMARY KEY,
    segment_name                VARCHAR(50)     NOT NULL UNIQUE,
    channel_type                VARCHAR(50)     NOT NULL
);

-- ----------------------------------------------------------------------------
-- 4. Dimension: Date Calendar
-- ----------------------------------------------------------------------------
CREATE TABLE dim_date (
    date_key                    INTEGER         PRIMARY KEY,
    date                        DATE            NOT NULL UNIQUE,
    year                        INTEGER         NOT NULL,
    quarter                     INTEGER         NOT NULL,
    quarter_name                VARCHAR(15)     NOT NULL,
    month_number                INTEGER         NOT NULL,
    month_name                  VARCHAR(20)     NOT NULL,
    month_short                 VARCHAR(10)     NOT NULL,
    year_month                  VARCHAR(10)     NOT NULL,
    day_of_month                INTEGER         NOT NULL,
    day_of_week                 VARCHAR(15)     NOT NULL,
    is_weekend                  INTEGER         NOT NULL
);

-- ----------------------------------------------------------------------------
-- 5. Fact: Actual Financial Transactions
-- ----------------------------------------------------------------------------
CREATE TABLE fact_financials (
    transaction_id              INTEGER         PRIMARY KEY,
    date_key                    INTEGER         NOT NULL,
    date                        DATE            NOT NULL,
    product_id                  VARCHAR(10)     NOT NULL,
    country_id                  VARCHAR(10)     NOT NULL,
    segment_id                  VARCHAR(10)     NOT NULL,
    discount_band               VARCHAR(20)     NOT NULL,
    units_sold                  DECIMAL(10,2)   NOT NULL,
    sale_price                  DECIMAL(10,2)   NOT NULL,
    gross_sales                 DECIMAL(14,2)   NOT NULL,
    discounts                   DECIMAL(14,2)   NOT NULL,
    net_sales                   DECIMAL(14,2)   NOT NULL,
    cogs                        DECIMAL(14,2)   NOT NULL,
    gross_profit                DECIMAL(14,2)   NOT NULL,
    gross_margin_pct            DECIMAL(6,2)    NOT NULL,
    discount_pct                DECIMAL(6,2)    NOT NULL,
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY (country_id) REFERENCES dim_country(country_id),
    FOREIGN KEY (segment_id) REFERENCES dim_segment(segment_id),
    FOREIGN KEY (date_key)   REFERENCES dim_date(date_key)
);

-- ----------------------------------------------------------------------------
-- 6. Fact: Illustrative Financial Budget Targets
-- ----------------------------------------------------------------------------
CREATE TABLE fact_budget (
    budget_id                   VARCHAR(30)     PRIMARY KEY,
    date_key                    INTEGER         NOT NULL,
    year                        INTEGER         NOT NULL,
    month_number                INTEGER         NOT NULL,
    country_id                  VARCHAR(10)     NOT NULL,
    segment_id                  VARCHAR(10)     NOT NULL,
    budget_revenue              DECIMAL(14,2)   NOT NULL,
    budget_cogs                 DECIMAL(14,2)   NOT NULL,
    budget_gross_profit         DECIMAL(14,2)   NOT NULL,
    budget_operating_expenses   DECIMAL(14,2)   NOT NULL,
    budget_operating_profit     DECIMAL(14,2)   NOT NULL,
    FOREIGN KEY (country_id) REFERENCES dim_country(country_id),
    FOREIGN KEY (segment_id) REFERENCES dim_segment(segment_id),
    FOREIGN KEY (date_key)   REFERENCES dim_date(date_key)
);

-- ----------------------------------------------------------------------------
-- 7. Fact: Illustrative Operating Expenses (OPEX)
-- ----------------------------------------------------------------------------
CREATE TABLE fact_operating_expenses (
    date_key                    INTEGER         NOT NULL,
    year                        INTEGER         NOT NULL,
    month_number                INTEGER         NOT NULL,
    segment_name                VARCHAR(50)     NOT NULL,
    marketing_advertising       DECIMAL(14,2)   NOT NULL,
    selling_general_admin       DECIMAL(14,2)   NOT NULL,
    research_development        DECIMAL(14,2)   NOT NULL,
    it_operations               DECIMAL(14,2)   NOT NULL,
    total_operating_expenses    DECIMAL(14,2)   NOT NULL,
    PRIMARY KEY (date_key, segment_name),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

-- ----------------------------------------------------------------------------
-- Indexes for Analytical Performance
-- ----------------------------------------------------------------------------
CREATE INDEX idx_fact_date ON fact_financials(date_key);
CREATE INDEX idx_fact_product ON fact_financials(product_id);
CREATE INDEX idx_fact_country ON fact_financials(country_id);
CREATE INDEX idx_fact_segment ON fact_financials(segment_id);
CREATE INDEX idx_budget_date ON fact_budget(date_key);

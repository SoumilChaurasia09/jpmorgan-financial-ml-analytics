"""
Financial Performance & Profitability Analysis - Data Cleaning & Transformation Pipeline
Author: Senior Data Analyst / Power BI Developer
Date: 2026-10-24

Purpose:
1. Ingest raw Microsoft Financial Sample Excel dataset.
2. Clean column headers, handle missing values, correct data types.
3. Validate financial identities (Gross Sales, Net Sales, COGS, Profit).
4. Create normalized Star Schema tables: Dim_Date, Dim_Product, Dim_Segment, Dim_Country, Fact_Financials.
5. Generate separate, clearly-labelled illustrative budget and operating expense datasets
   to satisfy business requirements for Budget vs Actual and Expense Analysis without corrupting raw data.
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime

# Define base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "Financial_Sample.xlsx")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

def clean_financial_data():
    print(f"[*] Loading raw dataset from: {RAW_DATA_PATH}")
    df_raw = pd.read_excel(RAW_DATA_PATH)
    
    initial_shape = df_raw.shape
    print(f"[*] Raw dataset loaded: {initial_shape[0]} rows, {initial_shape[1]} columns.")
    
    # 1. Standardize column names (strip whitespace, snake_case)
    df = df_raw.copy()
    df.columns = [c.strip() for c in df.columns]
    
    # Rename columns to standardized analytical naming
    rename_map = {
        'Segment': 'segment',
        'Country': 'country',
        'Product': 'product',
        'Discount Band': 'discount_band',
        'Units Sold': 'units_sold',
        'Manufacturing Price': 'manufacturing_price',
        'Sale Price': 'sale_price',
        'Gross Sales': 'gross_sales',
        'Discounts': 'discounts',
        'Sales': 'net_sales',
        'COGS': 'cogs',
        'Profit': 'gross_profit', # In this dataset, Profit = Net Sales - COGS, hence Gross Profit
        'Date': 'date',
        'Month Number': 'month_number',
        'Month Name': 'month_name',
        'Year': 'year'
    }
    df = df.rename(columns=rename_map)
    
    # 2. Handle missing values
    # In 'discount_band', NaN corresponds to transactions where no discount band applied ('No Discount')
    null_discount_count = df['discount_band'].isnull().sum()
    print(f"[*] Handling missing values: {null_discount_count} nulls in 'discount_band' imputed as 'No Discount'.")
    df['discount_band'] = df['discount_band'].fillna('No Discount')
    
    # Check for any remaining nulls
    remaining_nulls = df.isnull().sum().sum()
    if remaining_nulls > 0:
        print(f"[!] Warning: Remaining nulls found:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
    else:
        print("[*] Zero remaining nulls across all columns.")
        
    # 3. Check for duplicates
    dup_count = df.duplicated().sum()
    print(f"[*] Checked duplicate rows: {dup_count} duplicates detected.")
    
    # 4. Correct Data Types
    df['date'] = pd.to_datetime(df['date'])
    df['units_sold'] = pd.to_numeric(df['units_sold'], errors='coerce')
    df['manufacturing_price'] = pd.to_numeric(df['manufacturing_price'], errors='coerce')
    df['sale_price'] = pd.to_numeric(df['sale_price'], errors='coerce')
    df['gross_sales'] = pd.to_numeric(df['gross_sales'], errors='coerce').round(2)
    df['discounts'] = pd.to_numeric(df['discounts'], errors='coerce').round(2)
    df['net_sales'] = pd.to_numeric(df['net_sales'], errors='coerce').round(2)
    df['cogs'] = pd.to_numeric(df['cogs'], errors='coerce').round(2)
    df['gross_profit'] = pd.to_numeric(df['gross_profit'], errors='coerce').round(2)
    df['month_number'] = df['month_number'].astype(int)
    df['year'] = df['year'].astype(int)
    df['segment'] = df['segment'].astype(str).str.strip()
    df['country'] = df['country'].astype(str).str.strip()
    df['product'] = df['product'].astype(str).str.strip()
    df['discount_band'] = df['discount_band'].astype(str).str.strip()
    
    # 5. Financial Identity Validation
    # Mathematical checks:
    # A) Gross Sales = Units Sold * Sale Price
    gs_calc = (df['units_sold'] * df['sale_price']).round(2)
    gs_discrepancy = (df['gross_sales'] - gs_calc).abs() > 0.05
    print(f"[*] Financial validation 1 (Units * Sale Price == Gross Sales): {gs_discrepancy.sum()} discrepancies.")
    
    # B) Net Sales = Gross Sales - Discounts
    ns_calc = (df['gross_sales'] - df['discounts']).round(2)
    ns_discrepancy = (df['net_sales'] - ns_calc).abs() > 0.05
    print(f"[*] Financial validation 2 (Gross Sales - Discounts == Net Sales): {ns_discrepancy.sum()} discrepancies.")
    
    # C) Gross Profit = Net Sales - COGS
    gp_calc = (df['net_sales'] - df['cogs']).round(2)
    gp_discrepancy = (df['gross_profit'] - gp_calc).abs() > 0.05
    print(f"[*] Financial validation 3 (Net Sales - COGS == Gross Profit): {gp_discrepancy.sum()} discrepancies.")
    
    # 6. Derived Analytical Metrics
    # Calculate Gross Profit Margin %
    # When net_sales is 0, margin is 0
    df['gross_margin_pct'] = np.where(
        df['net_sales'] > 0,
        ((df['gross_profit'] / df['net_sales']) * 100).round(2),
        0.0
    )
    
    # Calculate Discount % on Gross Sales
    df['discount_pct'] = np.where(
        df['gross_sales'] > 0,
        ((df['discounts'] / df['gross_sales']) * 100).round(2),
        0.0
    )
    
    # Sort logically by date, country, segment, product
    df = df.sort_values(by=['date', 'country', 'segment', 'product']).reset_index(drop=True)
    
    # Add unique surrogate transaction key
    df.insert(0, 'transaction_id', range(1001, 1001 + len(df)))
    
    # 7. Build Relational Star Schema Tables
    print("[*] Generating Star Schema dimension and fact tables...")
    
    # Dim_Product
    products_unique = df[['product', 'manufacturing_price']].drop_duplicates().sort_values(by='product').reset_index(drop=True)
    products_unique.insert(0, 'product_id', [f"PRD{i+1:03d}" for i in range(len(products_unique))])
    dim_product = products_unique.rename(columns={
        'product': 'product_name',
        'manufacturing_price': 'standard_manufacturing_price'
    })
    
    # Dim_Country
    countries_unique = sorted(df['country'].unique())
    dim_country = pd.DataFrame({
        'country_id': [f"CTR{i+1:02d}" for i in range(len(countries_unique))],
        'country_name': countries_unique,
        'region': ['North America' if c in ['Canada', 'United States of America', 'Mexico'] else 'Europe' for c in countries_unique]
    })
    
    # Dim_Segment
    segments_unique = sorted(df['segment'].unique())
    dim_segment = pd.DataFrame({
        'segment_id': [f"SEG{i+1:02d}" for i in range(len(segments_unique))],
        'segment_name': segments_unique,
        'channel_type': ['B2B' if s in ['Enterprise', 'Midmarket', 'Channel Partners'] else ('B2G' if s == 'Government' else 'B2B/B2C') for s in segments_unique]
    })
    
    # Dim_Date
    min_date = df['date'].min()
    max_date = df['date'].max()
    date_range = pd.date_range(start='2013-01-01', end='2014-12-31', freq='D')
    dim_date = pd.DataFrame({'date': date_range})
    dim_date['date_key'] = dim_date['date'].dt.strftime('%Y%m%d').astype(int)
    dim_date['year'] = dim_date['date'].dt.year
    dim_date['quarter'] = dim_date['date'].dt.quarter
    dim_date['quarter_name'] = 'Q' + dim_date['quarter'].astype(str) + '-' + dim_date['year'].astype(str)
    dim_date['month_number'] = dim_date['date'].dt.month
    dim_date['month_name'] = dim_date['date'].dt.strftime('%B')
    dim_date['month_short'] = dim_date['date'].dt.strftime('%b')
    dim_date['year_month'] = dim_date['date'].dt.strftime('%Y-%m')
    dim_date['day_of_month'] = dim_date['date'].dt.day
    dim_date['day_of_week'] = dim_date['date'].dt.strftime('%A')
    dim_date['is_weekend'] = dim_date['date'].dt.weekday.isin([5, 6]).astype(int)
    
    # Map Foreign Keys to Fact Table
    fact_financials = df.copy()
    fact_financials = fact_financials.merge(dim_product[['product_id', 'product_name']], left_on='product', right_on='product_name')
    fact_financials = fact_financials.merge(dim_country[['country_id', 'country_name']], left_on='country', right_on='country_name')
    fact_financials = fact_financials.merge(dim_segment[['segment_id', 'segment_name']], left_on='segment', right_on='segment_name')
    fact_financials['date_key'] = fact_financials['date'].dt.strftime('%Y%m%d').astype(int)
    
    # Select fact columns
    fact_columns = [
        'transaction_id',
        'date_key',
        'date',
        'product_id',
        'country_id',
        'segment_id',
        'discount_band',
        'units_sold',
        'sale_price',
        'gross_sales',
        'discounts',
        'net_sales',
        'cogs',
        'gross_profit',
        'gross_margin_pct',
        'discount_pct'
    ]
    fact_financials = fact_financials[fact_columns].sort_values(by=['date', 'transaction_id']).reset_index(drop=True)
    
    # 8. Create Illustrative Budget & Operating Expense Models
    # To satisfy business questions on Budget Variance and Operating Expenses without corrupting raw data.
    print("[*] Generating illustrative budget and operating expense datasets...")
    
    # Budget Dataset: Generated at the monthly grain by Segment and Country for 2013 and 2014
    # Assumptions documented:
    # 1. Budget Revenue target is set based on management goal of +8% YoY growth over baseline.
    # 2. Budgeted COGS target set at 82% of Budgeted Revenue (targeting 18% Gross Margin).
    # 3. Budgeted Operating Expenses set at 7% of Budgeted Revenue.
    
    unique_months = df[['year', 'month_number', 'month_name']].drop_duplicates().sort_values(by=['year', 'month_number'])
    budget_records = []
    
    for _, m_row in unique_months.iterrows():
        yr = int(m_row['year'])
        mo = int(m_row['month_number'])
        date_rep = datetime(yr, mo, 1)
        date_key = int(date_rep.strftime('%Y%m%d'))
        
        for c_id, c_name in zip(dim_country['country_id'], dim_country['country_name']):
            for s_id, s_name in zip(dim_segment['segment_id'], dim_segment['segment_name']):
                # Find actuals for this slice to calibrate realistic benchmark
                actual_slice = df[(df['year'] == yr) & (df['month_number'] == mo) & 
                                  (df['country'] == c_name) & (df['segment'] == s_name)]
                actual_rev = actual_slice['net_sales'].sum()
                
                # If actual exists, target is baseline with small strategic variance (+/- 5% to 10%)
                # For realistic simulation, set strategic target:
                if actual_rev > 0:
                    # Target revenue: slightly challenging budget target (+5% above average)
                    target_rev = round(actual_rev * 1.05, 2)
                else:
                    target_rev = 150000.00
                
                target_cogs = round(target_rev * 0.82, 2)
                target_gross_profit = round(target_rev - target_cogs, 2)
                target_opex = round(target_rev * 0.08, 2)
                target_operating_profit = round(target_gross_profit - target_opex, 2)
                
                budget_records.append({
                    'budget_id': f"BGT-{yr}-{mo:02d}-{c_id}-{s_id}",
                    'date_key': date_key,
                    'year': yr,
                    'month_number': mo,
                    'country_id': c_id,
                    'segment_id': s_id,
                    'budget_revenue': target_rev,
                    'budget_cogs': target_cogs,
                    'budget_gross_profit': target_gross_profit,
                    'budget_operating_expenses': target_opex,
                    'budget_operating_profit': target_operating_profit
                })
                
    df_budget = pd.DataFrame(budget_records)
    
    # Operating Expenses Dataset (Simulated illustrative departmental expenses):
    # Expense categories: SG&A, Research & Development, Marketing & Advertising, IT & Infrastructure
    opex_records = []
    # Actual monthly sales total by segment
    monthly_seg = df.groupby(['year', 'month_number', 'segment'])['net_sales'].sum().reset_index()
    
    for _, r in monthly_seg.iterrows():
        yr = int(r['year'])
        mo = int(r['month_number'])
        seg = r['segment']
        seg_sales = r['net_sales']
        date_rep = datetime(yr, mo, 1)
        date_key = int(date_rep.strftime('%Y%m%d'))
        
        # Categorical cost allocations based on enterprise benchmark ratios
        marketing_exp = round(seg_sales * 0.035, 2)
        sga_exp = round(seg_sales * 0.025, 2)
        rd_exp = round(seg_sales * 0.015, 2)
        it_ops_exp = round(seg_sales * 0.010, 2)
        total_opex = round(marketing_exp + sga_exp + rd_exp + it_ops_exp, 2)
        
        opex_records.append({
            'date_key': date_key,
            'year': yr,
            'month_number': mo,
            'segment_name': seg,
            'marketing_advertising': marketing_exp,
            'selling_general_admin': sga_exp,
            'research_development': rd_exp,
            'it_operations': it_ops_exp,
            'total_operating_expenses': total_opex
        })
        
    df_opex = pd.DataFrame(opex_records)
    
    # 9. Save Files
    print("[*] Saving processed files to data/processed/ ...")
    
    # 1. Cleaned denormalized flat file
    cleaned_flat_path = os.path.join(PROCESSED_DATA_DIR, "financial_sales_cleaned.csv")
    df.to_csv(cleaned_flat_path, index=False)
    print(f"  -> {cleaned_flat_path} ({len(df)} rows)")
    
    # 2. Star Schema Tables
    dim_product.to_csv(os.path.join(PROCESSED_DATA_DIR, "dim_product.csv"), index=False)
    dim_country.to_csv(os.path.join(PROCESSED_DATA_DIR, "dim_country.csv"), index=False)
    dim_segment.to_csv(os.path.join(PROCESSED_DATA_DIR, "dim_segment.csv"), index=False)
    dim_date.to_csv(os.path.join(PROCESSED_DATA_DIR, "dim_date.csv"), index=False)
    fact_financials.to_csv(os.path.join(PROCESSED_DATA_DIR, "fact_financials.csv"), index=False)
    print(f"  -> Star schema dimension & fact tables saved successfully.")
    
    # 3. Illustrative Budget & Opex files
    budget_path = os.path.join(PROCESSED_DATA_DIR, "simulated_budget.csv")
    df_budget.to_csv(budget_path, index=False)
    print(f"  -> {budget_path} ({len(df_budget)} rows)")
    
    opex_path = os.path.join(PROCESSED_DATA_DIR, "simulated_operating_expenses.csv")
    df_opex.to_csv(opex_path, index=False)
    print(f"  -> {opex_path} ({len(df_opex)} rows)")
    
    print("\n[+] Data cleaning and transformation pipeline executed successfully!")
    return df, fact_financials, dim_product, dim_country, dim_segment, dim_date, df_budget, df_opex

if __name__ == "__main__":
    clean_financial_data()

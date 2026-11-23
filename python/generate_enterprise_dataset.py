"""
Enterprise Financial Performance & Profitability Dataset Generator
Generates a comprehensive, Fortune-500 scale corporate dataset featuring:
- Organizations: Commercial, Technology, Operations
- Product Lines under each Organization
- Hierarchical Geographies: EMEA (Western Europe, DACH, Nordics, UK&I), Americas (North America, LatAm), APAC (Greater China, Japan & ANZ)
- Multi-Year monthly financial actuals, budgets, and forecasts (2024 - 2026)
- Financial Line Items: Revenue, COGS, Gross Profit, Operating Expenses, EBITDA, Headcount
- Calibrated to match executive financial ratios (Gross Margin ~54.6%, EBITDA Margin ~25.4%)
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)

np.random.seed(42)

def generate_dataset():
    print("[*] Generating Enterprise Corporate Financial Dataset...")
    
    # 1. Dimension: Geography (Hierarchical Region -> Sub-Region -> Country)
    geography_data = [
        # EMEA
        {"geo_id": "GEO_WEU", "region": "EMEA", "sub_region": "Western Europe", "market_tier": "Tier 1", "executive_owner": "Sophie Laurent"},
        {"geo_id": "GEO_DAC", "region": "EMEA", "sub_region": "DACH", "market_tier": "Tier 1", "executive_owner": "Markus Weber"},
        {"geo_id": "GEO_UKI", "region": "EMEA", "sub_region": "UK & Ireland", "market_tier": "Tier 1", "executive_owner": "Oliver Smith"},
        {"geo_id": "GEO_NOR", "region": "EMEA", "sub_region": "Nordics", "market_tier": "Tier 2", "executive_owner": "Freja Lind"},
        # Americas
        {"geo_id": "GEO_NAM", "region": "Americas", "sub_region": "North America", "market_tier": "Tier 1", "executive_owner": "Michael Hayes"},
        {"geo_id": "GEO_LAM", "region": "Americas", "sub_region": "Latin America", "market_tier": "Tier 2", "executive_owner": "Carlos Silva"},
        # APAC
        {"geo_id": "GEO_GCH", "region": "APAC", "sub_region": "Greater China", "market_tier": "Tier 1", "executive_owner": "Wei Chen"},
        {"geo_id": "GEO_ANZ", "region": "APAC", "sub_region": "Japan & ANZ", "market_tier": "Tier 1", "executive_owner": "Kenji Sato"},
        {"geo_id": "GEO_SEA", "region": "APAC", "sub_region": "Southeast Asia", "market_tier": "Tier 2", "executive_owner": "Priya Sharma"}
    ]
    dim_geography = pd.DataFrame(geography_data)
    
    # 2. Dimension: Organization & Business Units
    org_data = [
        {"org_id": "ORG_COM", "organization_name": "Commercial", "division": "Global Sales & Enterprise Solutions", "lead_vp": "David Vance"},
        {"org_id": "ORG_TEC", "organization_name": "Technology", "division": "Cloud, Platforms & Software", "lead_vp": "Elena Rostova"},
        {"org_id": "ORG_OPS", "organization_name": "Operations", "division": "Manufacturing & Supply Chain Logistics", "lead_vp": "Arthur Pendelton"}
    ]
    dim_organization = pd.DataFrame(org_data)
    
    # 3. Dimension: Product Lines
    product_lines = [
        {"product_line_id": "PL_ENT", "org_id": "ORG_COM", "product_line": "Enterprise Licensing & SaaS", "category": "Software Subscriptions"},
        {"product_line_id": "PL_PRO", "org_id": "ORG_COM", "product_line": "Professional Advisory Services", "category": "Consulting"},
        {"product_line_id": "PL_CLD", "org_id": "ORG_TEC", "product_line": "Cloud Infrastructure & APIs", "category": "Cloud Services"},
        {"product_line_id": "PL_CYB", "org_id": "ORG_TEC", "product_line": "Cybersecurity & Data Governance", "category": "Security"},
        {"product_line_id": "PL_HWP", "org_id": "ORG_OPS", "product_line": "Hardware Systems & Edge Devices", "category": "Hardware"},
        {"product_line_id": "PL_LOG", "org_id": "ORG_OPS", "product_line": "Supply Chain & Fulfillment Ops", "category": "Logistics"}
    ]
    dim_product_line = pd.DataFrame(product_lines)
    
    # 4. Dimension: Date Calendar (2024 to 2026, 36 months)
    date_records = []
    date_range = pd.date_range(start="2024-01-01", end="2026-12-31", freq="MS") # Month Start
    
    for d in date_range:
        yr = d.year
        mo = d.month
        qtr = (mo - 1) // 3 + 1
        date_records.append({
            "date_key": int(d.strftime("%Y%m%d")),
            "date": d.strftime("%Y-%m-%d"),
            "fiscal_year": f"FY{yr}",
            "fiscal_quarter": f"FQ{qtr}",
            "fiscal_period": f"FQ{qtr} {yr}",
            "month_number": mo,
            "month_name": d.strftime("%B"),
            "month_short": d.strftime("%b"),
            "year_month": d.strftime("%Y-%m"),
            "year": yr
        })
    dim_date = pd.DataFrame(date_records)
    
    # 5. Fact Table: Monthly Financial Performance by Date, Org, Product Line, Geography
    # Calibrated so that 2025/2026 annualized matches the executive reference:
    # Total Revenue ~$19.81B, Budget ~$19.57B, Forecast ~$19.81B
    # Gross Margin ~54.63%, EBITDA ~$5.04B (~25.4%), Headcount ~1,240,000 (enterprise global)
    
    fact_records = []
    
    # Organization baseline weights
    org_weights = {
        "ORG_COM": 0.44, # 44% Commercial ($8.7B)
        "ORG_TEC": 0.36, # 36% Technology ($7.1B)
        "ORG_OPS": 0.20  # 20% Operations ($4.0B)
    }
    
    # Geography baseline weights
    geo_weights = {
        "GEO_WEU": 0.141, # Western Europe (~$2.80B)
        "GEO_DAC": 0.109, # DACH (~$2.17B)
        "GEO_UKI": 0.114, # UK & Ireland (~$2.26B)
        "GEO_NOR": 0.100, # Nordics (~$1.96B) -> EMEA Total ~46.4% (~$9.19B)
        "GEO_NAM": 0.280, # North America (~$5.55B)
        "GEO_LAM": 0.055, # Latin America (~$1.09B) -> Americas Total ~33.5%
        "GEO_GCH": 0.090, # Greater China (~$1.78B)
        "GEO_ANZ": 0.070, # Japan & ANZ (~$1.39B)
        "GEO_SEA": 0.041  # Southeast Asia (~$0.81B) -> APAC Total ~20.1%
    }
    
    # Base monthly run-rate for year 2025 (~$1.65B per month -> $19.8B annual)
    base_monthly_revenue = 1650000000.0
    
    for _, d_row in dim_date.iterrows():
        yr = d_row['year']
        mo = d_row['month_number']
        date_key = d_row['date_key']
        
        # Growth factor over time (2024: 0.90x, 2025: 1.00x, 2026: 1.12x)
        growth = 0.90 if yr == 2024 else (1.00 if yr == 2025 else 1.12)
        # Seasonal monthly wave factor (Q4 peaks in Oct/Dec, dip in Feb/Aug)
        seasonality = 1.0 + 0.12 * np.sin(mo * (2 * np.pi / 12) + 0.5)
        
        for _, pl_row in dim_product_line.iterrows():
            pl_id = pl_row['product_line_id']
            org_id = pl_row['org_id']
            org_wt = org_weights[org_id] / 2.0 # 2 product lines per org
            
            for _, g_row in dim_geography.iterrows():
                geo_id = g_row['geo_id']
                geo_wt = geo_weights[geo_id]
                
                # Baseline Expected Revenue for this slice
                slice_expected_rev = base_monthly_revenue * growth * seasonality * org_wt * geo_wt
                
                # Actual Revenue with realistic market noise (+/- 4%)
                noise_actual = np.random.normal(1.012, 0.035) # slight overperformance (+1.2% on avg)
                revenue_actual = round(slice_expected_rev * noise_actual, 2)
                
                # Budget Revenue (targets set at beginning of fiscal year)
                noise_budget = np.random.normal(1.000, 0.015)
                revenue_budget = round(slice_expected_rev * noise_budget, 2)
                
                # Forecast Revenue (re-forecasted with near-actual precision)
                noise_forecast = np.random.normal(1.000, 0.008)
                revenue_forecast = round(revenue_actual * noise_forecast, 2)
                
                # Cost of Goods Sold (COGS) -> targeting Gross Margin ~54.63%
                # COGS is ~45.37% of revenue
                cogs_ratio_actual = np.random.normal(0.4537, 0.015)
                cogs_actual = round(revenue_actual * cogs_ratio_actual, 2)
                cogs_budget = round(revenue_budget * 0.4600, 2)
                cogs_forecast = round(revenue_forecast * 0.4538, 2)
                
                # Gross Profit
                gross_profit_actual = round(revenue_actual - cogs_actual, 2)
                gross_profit_budget = round(revenue_budget - cogs_budget, 2)
                gross_profit_forecast = round(revenue_forecast - cogs_forecast, 2)
                
                # Operating Expenses (SG&A, R&D, IT) -> ~29.2% of revenue
                opex_ratio = np.random.normal(0.292, 0.012)
                opex_actual = round(revenue_actual * opex_ratio, 2)
                opex_budget = round(revenue_budget * 0.298, 2)
                opex_forecast = round(revenue_forecast * 0.292, 2)
                
                # EBITDA / Operating Profit -> Gross Profit - OPEX (~25.4% EBITDA margin)
                ebitda_actual = round(gross_profit_actual - opex_actual, 2)
                ebitda_budget = round(gross_profit_budget - opex_budget, 2)
                ebitda_forecast = round(gross_profit_forecast - opex_forecast, 2)
                
                # Headcount allocation (scaling with organization volume)
                headcount_actual = int(round((revenue_actual / 16000.0)))
                headcount_budget = int(round((revenue_budget / 16000.0)))
                
                fact_records.append({
                    "date_key": date_key,
                    "geo_id": geo_id,
                    "org_id": org_id,
                    "product_line_id": pl_id,
                    "revenue_actual": revenue_actual,
                    "revenue_budget": revenue_budget,
                    "revenue_forecast": revenue_forecast,
                    "cogs_actual": cogs_actual,
                    "cogs_budget": cogs_budget,
                    "cogs_forecast": cogs_forecast,
                    "gross_profit_actual": gross_profit_actual,
                    "gross_profit_budget": gross_profit_budget,
                    "gross_profit_forecast": gross_profit_forecast,
                    "opex_actual": opex_actual,
                    "opex_budget": opex_budget,
                    "opex_forecast": opex_forecast,
                    "ebitda_actual": ebitda_actual,
                    "ebitda_budget": ebitda_budget,
                    "ebitda_forecast": ebitda_forecast,
                    "headcount_actual": headcount_actual,
                    "headcount_budget": headcount_budget
                })
                
    fact_financials = pd.DataFrame(fact_records)
    
    # 6. Save Files into data/processed/
    print("[*] Saving new Enterprise Dataset to data/processed/ ...")
    
    dim_date.to_csv(os.path.join(OUTPUT_DIR, "dim_date.csv"), index=False)
    dim_geography.to_csv(os.path.join(OUTPUT_DIR, "dim_geography.csv"), index=False)
    dim_organization.to_csv(os.path.join(OUTPUT_DIR, "dim_organization.csv"), index=False)
    dim_product_line.to_csv(os.path.join(OUTPUT_DIR, "dim_product_line.csv"), index=False)
    fact_financials.to_csv(os.path.join(OUTPUT_DIR, "fact_financial_performance.csv"), index=False)
    
    # Print Validation Metrics
    print("\n[+] Enterprise Dataset Generated Successfully!")
    print(f"  -> Total Fact Records: {len(fact_financials):,} rows")
    
    # Check 2025 Full-Year Metrics
    f2025 = fact_financials.merge(dim_date, on="date_key")
    f2025 = f2025[f2025['year'] == 2025]
    tot_rev = f2025['revenue_actual'].sum()
    bgt_rev = f2025['revenue_budget'].sum()
    tot_ebitda = f2025['ebitda_actual'].sum()
    tot_gp = f2025['gross_profit_actual'].sum()
    gm_pct = (tot_gp / tot_rev) * 100
    var_pct = ((tot_rev - bgt_rev) / bgt_rev) * 100
    
    print("\n[+] 2025 Executive Metrics Summary:")
    print(f"  - Actual Revenue:     ${tot_rev/1e9:.2f} Billion")
    print(f"  - Budget Revenue:     ${bgt_rev/1e9:.2f} Billion (Variance: {var_pct:+.2f}%)")
    print(f"  - EBITDA:             ${tot_ebitda/1e9:.2f} Billion")
    print(f"  - Gross Margin %:     {gm_pct:.2f}%")
    print(f"  - Total Headcount:    {f2025['headcount_actual'].sum() / 12:,.0f} employees")
    
    # Regional breakdown for EMEA
    emea_actual = f2025.merge(dim_geography, on="geo_id")
    emea_tot = emea_actual[emea_actual['region'] == 'EMEA']['revenue_actual'].sum()
    print(f"  - EMEA Total Revenue: ${emea_tot/1e9:.2f} Billion")

if __name__ == "__main__":
    generate_dataset()

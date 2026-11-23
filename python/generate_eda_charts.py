"""
Financial Performance & Profitability Analysis - EDA & Visualization Generator
Author: Senior Data Analyst / Power BI Specialist
Date: 2026-10-24

Generates 6 publication-quality analytical charts exploring:
1. Monthly Revenue, COGS, and Profit Trend (with Margin trajectory)
2. Segment Profitability Breakdown & Enterprise Loss Exposure
3. Product Profitability vs Realized Revenue Scatter Matrix
4. Discount Band Impact on Profit Margin Erosion
5. Regional Revenue vs Profit Margin Comparison
6. Budget vs Actual Revenue and Profit Variance Analysis
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configure visual style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Palette definitions
NAVY = "#1E293B"
EMERALD = "#10B981"
CRIMSON = "#EF4444"
AMBER = "#F59E0B"
SLATE = "#64748B"
BLUE = "#3B82F6"

def load_data():
    df = pd.read_csv(os.path.join(DATA_DIR, "financial_sales_cleaned.csv"))
    df['date'] = pd.to_datetime(df['date'])
    budget = pd.read_csv(os.path.join(DATA_DIR, "simulated_budget.csv"))
    return df, budget

def plot_monthly_trend(df):
    print("[*] Generating Chart 1: Monthly Financial Trajectory...")
    monthly = df.groupby(['year', 'month_number', 'month_name']).agg(
        net_sales=('net_sales', 'sum'),
        cogs=('cogs', 'sum'),
        gross_profit=('gross_profit', 'sum')
    ).reset_index()
    monthly['date_sort'] = pd.to_datetime(monthly['year'].astype(str) + '-' + monthly['month_number'].astype(str) + '-01')
    monthly = monthly.sort_values(by='date_sort').reset_index(drop=True)
    monthly['period_label'] = monthly['date_sort'].dt.strftime('%b %Y')
    monthly['margin_pct'] = (monthly['gross_profit'] / monthly['net_sales']) * 100

    fig, ax1 = plt.subplots(figsize=(14, 6))

    # Bar chart for Sales and COGS
    x = np.arange(len(monthly))
    width = 0.38
    rects1 = ax1.bar(x - width/2, monthly['net_sales'] / 1e6, width, label='Net Revenue ($M)', color=BLUE, alpha=0.85)
    rects2 = ax1.bar(x + width/2, monthly['cogs'] / 1e6, width, label='COGS ($M)', color=SLATE, alpha=0.85)

    ax1.set_ylabel('Revenue & Costs ($ Millions)', fontsize=12, fontweight='bold', color=NAVY)
    ax1.set_xticks(x)
    ax1.set_xticklabels(monthly['period_label'], rotation=45, ha='right', fontsize=10)
    ax1.grid(axis='y', linestyle='--', alpha=0.5)

    # Line chart for Margin % on secondary axis
    ax2 = ax1.twinx()
    line = ax2.plot(x, monthly['margin_pct'], color=EMERALD, marker='o', linewidth=2.5, markersize=7, label='Gross Margin %')
    ax2.set_ylabel('Gross Margin (%)', fontsize=12, fontweight='bold', color=EMERALD)
    ax2.set_ylim(0, 25)
    ax2.grid(False)

    # Add Margin percentage annotations
    for i, txt in enumerate(monthly['margin_pct']):
        ax2.annotate(f"{txt:.1f}%", (x[i], txt + 0.8), ha='center', fontsize=9, fontweight='bold', color='#047857')

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=True, facecolor='white', framealpha=0.9)

    plt.title('Monthly Financial Performance: Revenue, COGS & Gross Margin Trajectory (Sep 2013 - Dec 2014)', 
              fontsize=14, fontweight='bold', pad=15, color=NAVY)
    plt.tight_layout()
    output_path = os.path.join(SCREENSHOTS_DIR, "01_monthly_financial_trajectory.png")
    plt.savefig(output_path)
    plt.close()
    print(f"  -> Saved: {output_path}")

def plot_segment_profitability(df):
    print("[*] Generating Chart 2: Customer Segment Profitability & Loss Exposure...")
    seg = df.groupby('segment').agg(
        net_sales=('net_sales', 'sum'),
        gross_profit=('gross_profit', 'sum')
    ).reset_index()
    seg['margin_pct'] = (seg['gross_profit'] / seg['net_sales']) * 100
    seg = seg.sort_values(by='gross_profit', ascending=False)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Bar chart of total profit
    colors = [CRIMSON if p < 0 else EMERALD for p in seg['gross_profit']]
    bars = ax1.bar(seg['segment'], seg['gross_profit'] / 1e6, color=colors, width=0.55, edgecolor='black', linewidth=0.8)
    ax1.set_ylabel('Total Gross Profit ($ Millions)', fontsize=12, fontweight='bold', color=NAVY)
    ax1.set_title('Cumulative Gross Profit by Segment ($M)\n(Highlighting Enterprise Loss)', fontsize=13, fontweight='bold', color=NAVY)
    ax1.axhline(0, color='black', linewidth=1)
    ax1.tick_params(axis='x', rotation=30)
    for bar in bars:
        height = bar.get_height()
        va = 'bottom' if height < 0 else 'bottom'
        offset = -0.6 if height < 0 else 0.2
        ax1.annotate(f"${height:.2f}M",
                     xy=(bar.get_x() + bar.get_width() / 2, height + offset),
                     ha='center', va=va, fontsize=10, fontweight='bold',
                     color=CRIMSON if height < 0 else NAVY)

    # Margin comparison bar chart
    margin_colors = [CRIMSON if m < 0 else (AMBER if m < 15 else EMERALD) for m in seg['margin_pct']]
    bars2 = ax2.bar(seg['segment'], seg['margin_pct'], color=margin_colors, width=0.55, edgecolor='black', linewidth=0.8)
    ax2.set_ylabel('Gross Margin (%)', fontsize=12, fontweight='bold', color=NAVY)
    ax2.set_title('Realized Gross Margin % by Segment', fontsize=13, fontweight='bold', color=NAVY)
    ax2.axhline(0, color='black', linewidth=1)
    ax2.tick_params(axis='x', rotation=30)
    for bar in bars2:
        h = bar.get_height()
        offset = -4.0 if h < 0 else 1.5
        ax2.annotate(f"{h:.1f}%",
                     xy=(bar.get_x() + bar.get_width() / 2, h + offset),
                     ha='center', fontsize=10, fontweight='bold',
                     color=CRIMSON if h < 0 else NAVY)

    plt.tight_layout()
    output_path = os.path.join(SCREENSHOTS_DIR, "02_segment_profitability_analysis.png")
    plt.savefig(output_path)
    plt.close()
    print(f"  -> Saved: {output_path}")

def plot_product_matrix(df):
    print("[*] Generating Chart 3: Product Profitability Matrix...")
    prod = df.groupby('product').agg(
        net_sales=('net_sales', 'sum'),
        cogs=('cogs', 'sum'),
        gross_profit=('gross_profit', 'sum'),
        units_sold=('units_sold', 'sum')
    ).reset_index()
    prod['margin_pct'] = (prod['gross_profit'] / prod['net_sales']) * 100

    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(
        prod['net_sales'] / 1e6,
        prod['gross_profit'] / 1e6,
        s=prod['units_sold'] / 400,
        c=prod['margin_pct'],
        cmap='viridis',
        alpha=0.85,
        edgecolors='black',
        linewidth=1.5
    )

    cbar = plt.colorbar(scatter)
    cbar.set_label('Gross Margin (%)', fontsize=11, fontweight='bold')

    for _, r in prod.iterrows():
        plt.annotate(
            f"{r['product']}\n(${r['gross_profit']/1e6:.2f}M, {r['margin_pct']:.1f}%)",
            xy=(r['net_sales']/1e6, r['gross_profit']/1e6),
            xytext=(10, 8),
            textcoords='offset points',
            fontsize=10,
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='gray')
        )

    plt.xlabel('Net Revenue ($ Millions)', fontsize=12, fontweight='bold', color=NAVY)
    plt.ylabel('Gross Profit ($ Millions)', fontsize=12, fontweight='bold', color=NAVY)
    plt.title('Product Commercial Matrix: Revenue vs. Gross Profit\n(Bubble size represents Units Sold)', 
              fontsize=13, fontweight='bold', color=NAVY, pad=15)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    output_path = os.path.join(SCREENSHOTS_DIR, "03_product_profitability_matrix.png")
    plt.savefig(output_path)
    plt.close()
    print(f"  -> Saved: {output_path}")

def plot_discount_impact(df):
    print("[*] Generating Chart 4: Discount Band Margin Erosion Analysis...")
    band = df.groupby('discount_band').agg(
        units_sold=('units_sold', 'sum'),
        gross_sales=('gross_sales', 'sum'),
        discounts=('discounts', 'sum'),
        net_sales=('net_sales', 'sum'),
        gross_profit=('gross_profit', 'sum')
    ).reset_index()
    band['effective_discount_pct'] = (band['discounts'] / band['gross_sales']) * 100
    band['realized_margin_pct'] = (band['gross_profit'] / band['net_sales']) * 100
    band = band.sort_values(by='effective_discount_pct')

    fig, ax1 = plt.subplots(figsize=(10, 5.5))
    x = np.arange(len(band))
    width = 0.35

    rects1 = ax1.bar(x - width/2, band['discounts'] / 1e6, width, label='Discounts Granted ($M)', color=AMBER, alpha=0.85)
    rects2 = ax1.bar(x + width/2, band['gross_profit'] / 1e6, width, label='Gross Profit ($M)', color=EMERALD, alpha=0.85)

    ax1.set_ylabel('$ Millions', fontsize=12, fontweight='bold', color=NAVY)
    ax1.set_xticks(x)
    ax1.set_xticklabels(band['discount_band'], fontsize=11, fontweight='bold')
    ax1.legend(loc='upper left', frameon=True)

    ax2 = ax1.twinx()
    ax2.plot(x, band['realized_margin_pct'], color=CRIMSON, marker='s', linewidth=2.5, markersize=8, label='Realized Gross Margin %')
    ax2.set_ylabel('Realized Margin (%)', fontsize=12, fontweight='bold', color=CRIMSON)
    ax2.set_ylim(0, 25)
    ax2.grid(False)

    for i, txt in enumerate(band['realized_margin_pct']):
        ax2.annotate(f"{txt:.1f}%", (x[i], txt + 0.9), ha='center', fontsize=10, fontweight='bold', color=CRIMSON)

    plt.title('Discount Band Impact: Discounts Granted vs Gross Profit & Realized Margin', 
              fontsize=13, fontweight='bold', pad=15, color=NAVY)
    plt.tight_layout()
    output_path = os.path.join(SCREENSHOTS_DIR, "04_discount_margin_erosion.png")
    plt.savefig(output_path)
    plt.close()
    print(f"  -> Saved: {output_path}")

def plot_regional_performance(df):
    print("[*] Generating Chart 5: Geographic & Regional Revenue vs Profit Comparison...")
    cntry = df.groupby(['country', 'segment']).agg(
        net_sales=('net_sales', 'sum'),
        gross_profit=('gross_profit', 'sum')
    ).reset_index()

    cntry_tot = df.groupby('country').agg(
        net_sales=('net_sales', 'sum'),
        gross_profit=('gross_profit', 'sum')
    ).reset_index()
    cntry_tot['margin_pct'] = (cntry_tot['gross_profit'] / cntry_tot['net_sales']) * 100
    cntry_tot = cntry_tot.sort_values(by='net_sales', ascending=False)

    fig, ax1 = plt.subplots(figsize=(11, 5.5))
    x = np.arange(len(cntry_tot))
    width = 0.38

    ax1.bar(x - width/2, cntry_tot['net_sales'] / 1e6, width, label='Net Revenue ($M)', color=BLUE, alpha=0.85)
    ax1.bar(x + width/2, cntry_tot['gross_profit'] / 1e6, width, label='Gross Profit ($M)', color=EMERALD, alpha=0.85)

    ax1.set_ylabel('$ Millions', fontsize=12, fontweight='bold', color=NAVY)
    ax1.set_xticks(x)
    ax1.set_xticklabels(cntry_tot['country'], fontsize=10, fontweight='bold', rotation=15)
    ax1.legend(loc='upper right')

    ax2 = ax1.twinx()
    ax2.plot(x, cntry_tot['margin_pct'], color=NAVY, marker='D', linewidth=2, markersize=7, label='Margin %')
    ax2.set_ylabel('Gross Margin (%)', fontsize=12, fontweight='bold', color=NAVY)
    ax2.set_ylim(0, 20)
    ax2.grid(False)

    for i, txt in enumerate(cntry_tot['margin_pct']):
        ax2.annotate(f"{txt:.1f}%", (x[i], txt + 0.7), ha='center', fontsize=9, fontweight='bold', color=NAVY)

    plt.title('Regional Comparison: Net Revenue, Gross Profit & Realized Margin by Country', 
              fontsize=13, fontweight='bold', pad=15, color=NAVY)
    plt.tight_layout()
    output_path = os.path.join(SCREENSHOTS_DIR, "05_regional_financial_comparison.png")
    plt.savefig(output_path)
    plt.close()
    print(f"  -> Saved: {output_path}")

def plot_budget_variance(df, budget):
    print("[*] Generating Chart 6: Budget vs Actual Variance Analysis...")
    dim_seg = pd.read_csv(os.path.join(DATA_DIR, "dim_segment.csv"))
    
    # Merge budget with dim_segment to get segment_name
    b_merged = budget.merge(dim_seg, on='segment_id')
    b_summary = b_merged.groupby('segment_name').agg(
        budget_rev=('budget_revenue', 'sum'),
        budget_prof=('budget_gross_profit', 'sum')
    ).reset_index()

    a_summary = df.groupby('segment').agg(
        actual_rev=('net_sales', 'sum'),
        actual_prof=('gross_profit', 'sum')
    ).reset_index().rename(columns={'segment': 'segment_name'})

    comp = b_summary.merge(a_summary, on='segment_name')
    comp['rev_variance'] = comp['actual_rev'] - comp['budget_rev']
    comp['prof_variance'] = comp['actual_prof'] - comp['budget_prof']
    comp['achievement_pct'] = (comp['actual_rev'] / comp['budget_rev']) * 100

    fig, ax = plt.subplots(figsize=(11, 5.5))
    x = np.arange(len(comp))
    width = 0.35

    rects1 = ax.bar(x - width/2, comp['budget_rev'] / 1e6, width, label='Budget Revenue ($M)', color=SLATE, alpha=0.7)
    rects2 = ax.bar(x + width/2, comp['actual_rev'] / 1e6, width, label='Actual Revenue ($M)', color=BLUE, alpha=0.9)

    ax.set_ylabel('Revenue ($ Millions)', fontsize=12, fontweight='bold', color=NAVY)
    ax.set_xticks(x)
    ax.set_xticklabels(comp['segment_name'], fontsize=10, fontweight='bold')
    ax.legend(loc='upper right')

    for i in range(len(comp)):
        ach = comp['achievement_pct'].iloc[i]
        col = EMERALD if ach >= 100 else AMBER
        ax.annotate(f"{ach:.1f}% Target",
                    xy=(x[i] + width/2, (comp['actual_rev'].iloc[i] / 1e6) + 1.2),
                    ha='center', fontsize=9, fontweight='bold', color=col)

    plt.title('Budget vs Actual Performance: Commercial Segment Revenue Achievement', 
              fontsize=13, fontweight='bold', pad=15, color=NAVY)
    plt.tight_layout()
    output_path = os.path.join(SCREENSHOTS_DIR, "06_budget_vs_actual_revenue.png")
    plt.savefig(output_path)
    plt.close()
    print(f"  -> Saved: {output_path}")

def run_all_eda():
    df, budget = load_data()
    plot_monthly_trend(df)
    plot_segment_profitability(df)
    plot_product_matrix(df)
    plot_discount_impact(df)
    plot_regional_performance(df)
    plot_budget_variance(df, budget)
    print("\n[+] All 6 EDA visualization figures generated and saved to screenshots/ successfully!")

if __name__ == "__main__":
    run_all_eda()

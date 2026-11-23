import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

fig = plt.figure(figsize=(16, 9), facecolor='#0B0F19')
ax = fig.add_axes([0, 0, 1, 1], facecolor='#0B0F19')
ax.axis('off')

# Sidebar
sidebar = patches.FancyBboxPatch((0.02, 0.04), 0.09, 0.92, boxstyle='round,pad=0.01,rounding_size=0.02', 
                                facecolor='#0A0E17', edgecolor='#1E293B', linewidth=1)
ax.add_patch(sidebar)

# Sidebar Logo
ax.text(0.065, 0.91, 'JPM', color='#FFFFFF', fontsize=16, fontweight='black', ha='center')
ax.text(0.065, 0.885, 'NYSE: JPM', color='#94A3B8', fontsize=8, ha='center')

# Sidebar Buttons
btn_y = [0.80, 0.73, 0.66]
btn_labels = ['Executive\nSummary', 'Statements &\nLiquidity', 'Predictive\nAnalytics']
for i, y in enumerate(btn_y):
    is_active = (i == 1) # Statements is active!
    bc = '#1E293B' if is_active else '#162032'
    ec = '#38BDF8' if is_active else '#334155'
    lw = 1.8 if is_active else 0.8
    tc = '#38BDF8' if is_active else '#94A3B8'
    btn = patches.FancyBboxPatch((0.028, y), 0.074, 0.052, boxstyle='round,pad=0.005,rounding_size=0.01',
                                facecolor=bc, edgecolor=ec, linewidth=lw)
    ax.add_patch(btn)
    ax.text(0.065, y + 0.026, btn_labels[i], color=tc, fontsize=8, fontweight='bold' if is_active else 'normal', ha='center', va='center')

# Reset Button
reset_btn = patches.FancyBboxPatch((0.028, 0.08), 0.074, 0.04, boxstyle='round,pad=0.005,rounding_size=0.01',
                                  facecolor='#162032', edgecolor='#334155', linewidth=0.8)
ax.add_patch(reset_btn)
ax.text(0.065, 0.10, 'RESET', color='#94A3B8', fontsize=8, fontweight='bold', ha='center', va='center')

# Top Header
ax.text(0.13, 0.92, 'JPMorgan Chase & Co.', color='#FFFFFF', fontsize=17, fontweight='bold')
ax.text(0.32, 0.92, '| Statements, Balance Sheet & Capital Allocation', color='#94A3B8', fontsize=15)

# Top Right Slicers
slicer_x = [0.72, 0.81, 0.90]
slicer_labels = ['Statement View', 'Fiscal Period', 'Reporting Scope']
slicer_vals = ['Balance Sheet v', 'Q3-2026 v', 'SEC Actuals v']
for i in range(3):
    slc = patches.FancyBboxPatch((slicer_x[i], 0.90), 0.08, 0.045, boxstyle='round,pad=0.005,rounding_size=0.008',
                                facecolor='#162032', edgecolor='#334155', linewidth=1)
    ax.add_patch(slc)
    ax.text(slicer_x[i] + 0.04, 0.932, slicer_labels[i], color='#94A3B8', fontsize=6.5, ha='center')
    ax.text(slicer_x[i] + 0.04, 0.912, slicer_vals[i], color='#FFFFFF', fontsize=7.5, fontweight='bold', ha='center')

# 4 KPI Cards
card_w = 0.20
card_h = 0.14
card_y = 0.73
cards_data = [
    ('TOTAL CUSTOMER DEPOSITS', '$2.78T', '+4.6% YoY Growth', 'Core Funding Reserve', '#60A5FA'),
    ('LOANS (NET OF ALLOWANCE)', '$1.56T', '+6.2% YoY Growth', 'Credit Assets Deployed', '#34D399'),
    ('LOAN-TO-DEPOSIT RATIO', '55.9%', 'Liquidity Buffer: $1.22T', 'Target: 50% - 65% (Optimal)', '#A78BFA'),
    ("SHAREHOLDERS' EQUITY", '$372.4B', '+5.8% Book Value', 'Common Equity Tier 1', '#F59E0B')
]

for i, (title, val, sub1, sub2, col) in enumerate(cards_data):
    cx = 0.13 + i * 0.215
    card = patches.FancyBboxPatch((cx, card_y), card_w, card_h, boxstyle='round,pad=0.008,rounding_size=0.015',
                                 facecolor='#162032', edgecolor='#334155', linewidth=1)
    ax.add_patch(card)
    ax.text(cx + 0.012, card_y + 0.115, title, color='#94A3B8', fontsize=7.5, fontweight='bold')
    ax.text(cx + 0.012, card_y + 0.065, val, color='#FFFFFF', fontsize=20, fontweight='black')
    ax.text(cx + 0.012, card_y + 0.025, sub1, color=col, fontsize=7.5, fontweight='bold')
    ax.text(cx + card_w - 0.012, card_y + 0.025, sub2, color='#64748B', fontsize=6.5, ha='right')

# Visual 1 (Bottom Left): Balance Sheet & Liquidity Area Chart
ax1_box = patches.FancyBboxPatch((0.13, 0.06), 0.44, 0.63, boxstyle='round,pad=0.008,rounding_size=0.015',
                                facecolor='#162032', edgecolor='#334155', linewidth=1)
ax.add_patch(ax1_box)
ax.text(0.145, 0.655, 'Balance Sheet Growth & Liquidity Buffer (2024 - 2026)', color='#FFFFFF', fontsize=11, fontweight='bold')
ax.text(0.145, 0.635, 'Customer Deposits ($T) vs. Loan Portfolio ($T) & Liquidity Gap', color='#94A3B8', fontsize=7.5)

# Sub-axes for Area chart
ax1 = fig.add_axes([0.155, 0.11, 0.39, 0.50], facecolor='#162032')
quarters = ['Q4-24', 'Q1-25', 'Q2-25', 'Q3-25', 'Q4-25', 'Q1-26', 'Q2-26', 'Q3-26']
deposits = [2.41, 2.50, 2.56, 2.55, 2.56, 2.68, 2.71, 2.78]
loans = [1.32, 1.33, 1.39, 1.41, 1.47, 1.48, 1.52, 1.56]

x = np.arange(len(quarters))
ax1.plot(x, deposits, color='#60A5FA', linewidth=2.5, marker='o', label='Customer Deposits ($T)')
ax1.fill_between(x, deposits, loans, color='#60A5FA', alpha=0.25, label='Excess Liquidity Reserve ($1.22T)')
ax1.plot(x, loans, color='#34D399', linewidth=2.5, marker='s', label='Loans Net of Allowance ($T)')

ax1.set_xticks(x)
ax1.set_xticklabels(quarters, color='#94A3B8', fontsize=8)
ax1.tick_params(colors='#94A3B8')
for spine in ax1.spines.values():
    spine.set_color('#334155')
ax1.grid(True, linestyle='--', alpha=0.3, color='#334155')
ax1.set_ylim(1.0, 3.2)
ax1.legend(loc='upper left', facecolor='#0B0F19', edgecolor='#334155', fontsize=7.5, labelcolor='#FFFFFF')

# Visual 2 (Top Right): Capital Return to Shareholders
ax2_box = patches.FancyBboxPatch((0.59, 0.39), 0.39, 0.30, boxstyle='round,pad=0.008,rounding_size=0.015',
                                facecolor='#162032', edgecolor='#334155', linewidth=1)
ax.add_patch(ax2_box)
ax.text(0.605, 0.66, 'Capital Returned to Shareholders ($ Billions)', color='#FFFFFF', fontsize=10.5, fontweight='bold')
ax.text(0.605, 0.64, 'Quarterly Dividends Paid vs. Share Repurchases', color='#94A3B8', fontsize=7.5)

ax2 = fig.add_axes([0.61, 0.42, 0.35, 0.20], facecolor='#162032')
divs = [3.86, 3.82, 4.21, 4.18, 4.42, 4.37, 4.34, 4.32]
buybacks = [4.30, 7.53, 7.51, 8.29, 8.26, 8.33, 6.79, 1.11]
w = 0.35
ax2.bar(x - w/2, divs, width=w, color='#818CF8', label='Dividends Paid ($B)')
ax2.bar(x + w/2, buybacks, width=w, color='#F59E0B', label='Share Repurchases ($B)')
ax2.set_xticks(x)
ax2.set_xticklabels(quarters, color='#94A3B8', fontsize=7.5)
ax2.tick_params(colors='#94A3B8')
for spine in ax2.spines.values():
    spine.set_color('#334155')
ax2.grid(True, linestyle='--', alpha=0.3, color='#334155')
ax2.legend(loc='upper right', facecolor='#0B0F19', edgecolor='#334155', fontsize=7, labelcolor='#FFFFFF')

# Visual 3 (Bottom Right): Liquidity & Balance Sheet Audit Table
ax3_box = patches.FancyBboxPatch((0.59, 0.06), 0.39, 0.30, boxstyle='round,pad=0.008,rounding_size=0.015',
                                facecolor='#162032', edgecolor='#334155', linewidth=1)
ax.add_patch(ax3_box)
ax.text(0.605, 0.33, 'Quarterly Balance Sheet & Credit Risk Summary', color='#FFFFFF', fontsize=10.5, fontweight='bold')
ax.text(0.605, 0.31, 'Loans, Deposits, Loan-to-Deposit Ratio & Credit Provisions', color='#94A3B8', fontsize=7.5)

# Render table text inside box 3
table_rows = [
    ['Quarter', 'Deposits', 'Loans', 'L/D %', 'Provision'],
    ['Q3-2026', '$2,781B', '$1,558B', '56.0%', '$2,743M'],
    ['Q2-2026', '$2,714B', '$1,516B', '55.9%', '$2,515M'],
    ['Q1-2026', '$2,676B', '$1,478B', '55.2%', '$2,507M'],
    ['Q4-2025', '$2,559B', '$1,468B', '57.3%', '$4,655M (Risk)'],
    ['Q3-2025', '$2,548B', '$1,410B', '55.3%', '$3,403M']
]

ty = 0.28
for r_i, row in enumerate(table_rows):
    is_hdr = (r_i == 0)
    col_x = [0.605, 0.68, 0.76, 0.84, 0.91]
    color = '#94A3B8' if is_hdr else ('#EF4444' if 'Risk' in row[4] else '#FFFFFF')
    weight = 'bold' if is_hdr or 'Risk' in row[4] else 'normal'
    for c_i, cell in enumerate(row):
        ax.text(col_x[c_i], ty, cell, color=color, fontsize=7.5, fontweight=weight)
    ty -= 0.038

out_path = r'C:\Users\soumi\.gemini\antigravity\scratch\financial-performance-analysis\screenshots\08_jpm_dashboard_page2_mockup.png'
art_path = r'C:\Users\soumi\.gemini\antigravity\brain\348d2d73-5d0e-4b57-9de6-eec98a33e1d2\jpm_page2_preview.png'
os.makedirs(os.path.dirname(out_path), exist_ok=True)
plt.savefig(out_path, dpi=200, facecolor='#0B0F19')
plt.savefig(art_path, dpi=200, facecolor='#0B0F19')
plt.close()
print('Generated Page 2 mockup image successfully!')

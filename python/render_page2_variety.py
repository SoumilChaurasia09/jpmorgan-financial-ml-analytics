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
ax.text(0.065, 0.91, 'JPM', color='#FFFFFF', fontsize=16, fontweight='black', ha='center')
ax.text(0.065, 0.885, 'NYSE: JPM', color='#94A3B8', fontsize=8, ha='center')

btn_y = [0.80, 0.73, 0.66]
btn_labels = ['Executive\nSummary', 'Statements &\nLiquidity', 'Predictive\nAnalytics']
for i, y in enumerate(btn_y):
    is_active = (i == 1)
    bc = '#1E293B' if is_active else '#162032'
    ec = '#38BDF8' if is_active else '#334155'
    lw = 1.8 if is_active else 0.8
    tc = '#38BDF8' if is_active else '#94A3B8'
    btn = patches.FancyBboxPatch((0.028, y), 0.074, 0.052, boxstyle='round,pad=0.005,rounding_size=0.01',
                                facecolor=bc, edgecolor=ec, linewidth=lw)
    ax.add_patch(btn)
    ax.text(0.065, y + 0.026, btn_labels[i], color=tc, fontsize=8, fontweight='bold' if is_active else 'normal', ha='center', va='center')

reset_btn = patches.FancyBboxPatch((0.028, 0.08), 0.074, 0.04, boxstyle='round,pad=0.005,rounding_size=0.01',
                                  facecolor='#162032', edgecolor='#334155', linewidth=0.8)
ax.add_patch(reset_btn)
ax.text(0.065, 0.10, 'RESET', color='#94A3B8', fontsize=8, fontweight='bold', ha='center', va='center')

# Header
ax.text(0.13, 0.92, 'JPMorgan Chase & Co.', color='#FFFFFF', fontsize=17, fontweight='bold')
ax.text(0.32, 0.92, '| Statements, Cash Flow Waterfall & Capital Structure', color='#94A3B8', fontsize=15)

# 4 KPI Cards
card_w = 0.20
card_h = 0.14
card_y = 0.73
cards_data = [
    ('TOTAL CUSTOMER DEPOSITS', '$2.78T', '+4.6% Core Reserves', '#60A5FA'),
    ('OPERATING CASH FLOW', '$33.16B', 'High Cash Conversion', '#34D399'),
    ('LOAN-TO-DEPOSIT RATIO', '55.9%', 'Target: 50% - 65% (Optimal)', '#A78BFA'),
    ("SHAREHOLDERS' EQUITY", '$372.4B', '+5.8% Common Equity Tier 1', '#F59E0B')
]

for i, (title, val, sub1, col) in enumerate(cards_data):
    cx = 0.13 + i * 0.215
    card = patches.FancyBboxPatch((cx, card_y), card_w, card_h, boxstyle='round,pad=0.008,rounding_size=0.015',
                                 facecolor='#162032', edgecolor='#334155', linewidth=1)
    ax.add_patch(card)
    ax.text(cx + 0.012, card_y + 0.115, title, color='#94A3B8', fontsize=7.5, fontweight='bold')
    ax.text(cx + 0.012, card_y + 0.065, val, color='#FFFFFF', fontsize=20, fontweight='black')
    ax.text(cx + 0.012, card_y + 0.025, sub1, color=col, fontsize=7.5, fontweight='bold')

# Visual 1 (Left Half): Cash Flow Waterfall Bridge
ax1_box = patches.FancyBboxPatch((0.13, 0.06), 0.44, 0.63, boxstyle='round,pad=0.008,rounding_size=0.015',
                                facecolor='#162032', edgecolor='#334155', linewidth=1)
ax.add_patch(ax1_box)
ax.text(0.145, 0.655, 'Cash Flow & Capital Allocation Waterfall ($ Billions)', color='#FFFFFF', fontsize=11, fontweight='bold')
ax.text(0.145, 0.635, 'Reconciliation: Operating Cash Flow -> Investing -> Dividends -> Buybacks -> Net Cash', color='#94A3B8', fontsize=7.5)

# Render Waterfall Chart on Sub-axes
ax1 = fig.add_axes([0.155, 0.11, 0.39, 0.50], facecolor='#162032')
cats = ['Operating Cash', 'Securities / Inv', 'Dividends Paid', 'Share Buybacks', 'Financing Ops', 'Net Cash Change']
bottoms = [0, 33.16 - 90.1, -56.94 - 4.32, -61.26 - 1.11, -62.37, 0]
heights = [33.16, -90.10, -4.32, -1.11, 72.47, 10.10]
colors = ['#10B981', '#EF4444', '#F59E0B', '#EF4444', '#3B82F6', '#60A5FA']

wx = np.arange(len(cats))
for ci in range(len(cats)):
    if ci == 0:
        ax1.bar(ci, heights[ci], bottom=0, color='#10B981', width=0.55)
    elif ci == 5:
        ax1.bar(ci, heights[ci], bottom=0, color='#60A5FA', width=0.55)
    else:
        b = 33.16 if ci == 1 else (33.16 - 90.1 if ci == 2 else (33.16 - 90.1 - 4.32 if ci == 3 else -62.37))
        ax1.bar(ci, heights[ci], bottom=b, color=colors[ci], width=0.55)

ax1.axhline(0, color='#64748B', linewidth=1)
ax1.set_xticks(wx)
ax1.set_xticklabels(['Operating\nCash Flow\n(+$33.2B)', 'Investing\nSecurities\n(-$90.1B)', 'Dividends\nPaid\n(-$4.3B)', 'Share\nBuybacks\n(-$1.1B)', 'Financing\nInflow\n(+$72.5B)', 'Net Cash\nExpansion\n(+$10.1B)'], color='#94A3B8', fontsize=7)
ax1.tick_params(colors='#94A3B8')
for spine in ax1.spines.values():
    spine.set_color('#334155')
ax1.grid(True, linestyle='--', alpha=0.3, color='#334155')

# Visual 2 (Top Right): Capital Structure Donut Chart
ax2_box = patches.FancyBboxPatch((0.59, 0.39), 0.39, 0.30, boxstyle='round,pad=0.008,rounding_size=0.015',
                                facecolor='#162032', edgecolor='#334155', linewidth=1)
ax.add_patch(ax2_box)
ax.text(0.605, 0.66, 'Balance Sheet Funding Structure ($5.09 Trillion Total)', color='#FFFFFF', fontsize=10.5, fontweight='bold')
ax.text(0.605, 0.64, 'How JPMorgan Funds Its Balance Sheet: Deposits vs. Debt vs. Equity', color='#94A3B8', fontsize=7.5)

ax2 = fig.add_axes([0.62, 0.41, 0.16, 0.22], facecolor='#162032')
donut_sizes = [2781, 1938, 372]
donut_colors = ['#60A5FA', '#64748B', '#F59E0B']
wedges, texts = ax2.pie(donut_sizes, colors=donut_colors, startangle=140, 
                        wedgeprops=dict(width=0.45, edgecolor='#162032', linewidth=2))
ax2.text(0, 0, '$5.09T', color='#FFFFFF', fontsize=11, fontweight='black', ha='center', va='center')

# Legend for Donut
ax.text(0.79, 0.58, 'Customer Deposits: $2.78T (55%)', color='#60A5FA', fontsize=8, fontweight='bold')
ax.text(0.79, 0.53, 'Trading & Borrowings: $1.94T (38%)', color='#94A3B8', fontsize=8)
ax.text(0.79, 0.48, "Shareholders' Equity: $372B (7%)", color='#F59E0B', fontsize=8, fontweight='bold')

# Visual 3 (Bottom Right): Liquidity Target Gauge
ax3_box = patches.FancyBboxPatch((0.59, 0.06), 0.39, 0.30, boxstyle='round,pad=0.008,rounding_size=0.015',
                                facecolor='#162032', edgecolor='#334155', linewidth=1)
ax.add_patch(ax3_box)
ax.text(0.605, 0.33, 'Regulatory Liquidity Meter: Loan-to-Deposit Ratio', color='#FFFFFF', fontsize=10.5, fontweight='bold')
ax.text(0.605, 0.31, 'Current: 55.9% | Optimal Bank Range: 50% - 65% | High Risk: >80%', color='#94A3B8', fontsize=7.5)

# Render Gauge arc
theta = np.linspace(np.pi, 0, 100)
gauge_x = 0.785 + 0.11 * np.cos(theta)
gauge_y = 0.13 + 0.11 * np.sin(theta)
ax.plot(gauge_x, gauge_y, color='#334155', linewidth=14, solid_capstyle='round')

theta_fill = np.linspace(np.pi, np.pi - (np.pi * 0.559), 60)
fill_x = 0.785 + 0.11 * np.cos(theta_fill)
fill_y = 0.13 + 0.11 * np.sin(theta_fill)
ax.plot(fill_x, fill_y, color='#10B981', linewidth=14, solid_capstyle='round')

ax.text(0.785, 0.155, '55.9%', color='#FFFFFF', fontsize=22, fontweight='black', ha='center')
ax.text(0.785, 0.125, 'OPTIMAL LIQUIDITY', color='#34D399', fontsize=8, fontweight='bold', ha='center')
ax.text(0.67, 0.10, '0% (Low Utilization)', color='#64748B', fontsize=7)
ax.text(0.85, 0.10, '100% (High Risk)', color='#EF4444', fontsize=7)

out_path = r'C:\Users\soumi\.gemini\antigravity\scratch\financial-performance-analysis\screenshots\09_jpm_dashboard_page2_new_variety.png'
art_path = r'C:\Users\soumi\.gemini\antigravity\brain\348d2d73-5d0e-4b57-9de6-eec98a33e1d2\jpm_page2_new_variety.png'
plt.savefig(out_path, dpi=200, facecolor='#0B0F19')
plt.savefig(art_path, dpi=200, facecolor='#0B0F19')
plt.close()
print('Generated New Variety Page 2 mockup successfully!')

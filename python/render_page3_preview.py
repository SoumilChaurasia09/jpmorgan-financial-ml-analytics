import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd

# Load ML enriched data
df = pd.read_csv(r'C:\Users\soumi\.gemini\antigravity\scratch\new\jpm_financial_ml_enriched.csv')

fig = plt.figure(figsize=(16, 9), facecolor='#0B0F19')
ax = fig.add_axes([0, 0, 1, 1], facecolor='#0B0F19')
ax.axis('off')

# 1. Sidebar (Dark glassmorphic container)
sidebar = patches.FancyBboxPatch((0.02, 0.04), 0.09, 0.92, boxstyle='round,pad=0.01,rounding_size=0.02', 
                                facecolor='#0A0E17', edgecolor='#1E293B', linewidth=1)
ax.add_patch(sidebar)
ax.text(0.065, 0.91, 'JPM', color='#FFFFFF', fontsize=16, fontweight='black', ha='center')
ax.text(0.065, 0.885, 'NYSE: JPM', color='#94A3B8', fontsize=8, ha='center')

btn_y = [0.80, 0.73, 0.66]
btn_labels = ['Executive\nSummary', 'Statements &\nLiquidity', 'Predictive\nAnalytics']
for i, y in enumerate(btn_y):
    is_active = (i == 2)  # Page 3 is active!
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

# 2. Header
ax.text(0.13, 0.92, 'JPMorgan Chase & Co.', color='#FFFFFF', fontsize=17, fontweight='bold')
ax.text(0.32, 0.92, '| AI / ML Predictive Analytics & Credit Anomaly Risk Engine', color='#94A3B8', fontsize=14)

# 3. 4 KPI Cards across top
card_w = 0.20
card_h = 0.13
card_y = 0.74
cards_data = [
    ('12M FORWARD REVENUE', '$237.5B', '+9.4% Projected YoY Growth', '#60A5FA'),
    ('ML FORECAST ACCURACY', '3.4% MAE', 'R² = 0.941 (Polynomial Ridge)', '#34D399'),
    ('CREDIT LOSS ANOMALIES', '2 Flagged', 'Isolation Forest (Q4-25 Spike)', '#F87171'),
    ('95% CONFIDENCE SPREAD', '±$3.85B', 'Monte Carlo Uncertainty Band', '#A78BFA')
]

for i, (title, val, sub1, col) in enumerate(cards_data):
    cx = 0.13 + i * 0.215
    card = patches.FancyBboxPatch((cx, card_y), card_w, card_h, boxstyle='round,pad=0.008,rounding_size=0.015',
                                 facecolor='#162032', edgecolor='#334155', linewidth=1)
    ax.add_patch(card)
    ax.text(cx + 0.012, card_y + 0.105, title, color='#94A3B8', fontsize=7.5, fontweight='bold')
    ax.text(cx + 0.012, card_y + 0.055, val, color='#FFFFFF', fontsize=20, fontweight='black')
    ax.text(cx + 0.012, card_y + 0.02, sub1, color=col, fontsize=7.5, fontweight='bold')

# 4. Visual 1 (Top-Left): AI Revenue Forecast with 95% Confidence Interval
v1_box = patches.FancyBboxPatch((0.13, 0.38), 0.48, 0.34, boxstyle='round,pad=0.008,rounding_size=0.015',
                               facecolor='#162032', edgecolor='#334155', linewidth=1)
ax.add_patch(v1_box)
ax.text(0.145, 0.69, 'Revenue Actuals vs. Forward ML Ridge Forecast ($ Billions)', color='#FFFFFF', fontsize=10.5, fontweight='bold')
ax.text(0.145, 0.67, '8 Historical Quarters + 4 Forward Quarters with 95% Prediction Interval Band', color='#94A3B8', fontsize=7.5)

# Subplot for Visual 1
ax1 = fig.add_axes([0.155, 0.41, 0.43, 0.24], facecolor='#162032')
quarters = df['Quarter'].tolist()
rev = (df['Total_net_revenue'] / 1000).values
rev_lower = (df['Total_net_revenue_lower_95'] / 1000).values
rev_upper = (df['Total_net_revenue_upper_95'] / 1000).values

x = np.arange(len(quarters))
# Historical actual (0 to 7)
ax1.plot(x[:8], rev[:8], color='#38BDF8', linewidth=2.5, marker='o', markersize=5, label='Actual Revenue ($B)')
# Forecast line (7 to 11)
ax1.plot(x[7:], rev[7:], color='#A78BFA', linewidth=2.5, linestyle='--', marker='s', markersize=5, label='ML Forecast ($B)')
# Shaded 95% CI
ax1.fill_between(x[7:], rev_lower[7:], rev_upper[7:], color='#A78BFA', alpha=0.25, label='95% Confidence Band')

ax1.set_xticks(x)
ax1.set_xticklabels(quarters, color='#94A3B8', fontsize=7, rotation=25)
ax1.tick_params(colors='#94A3B8', labelsize=7)
for spine in ax1.spines.values():
    spine.set_color('#334155')
ax1.grid(True, linestyle='--', alpha=0.3, color='#334155')
ax1.legend(loc='upper left', facecolor='#1E293B', edgecolor='#334155', labelcolor='#FFFFFF', fontsize=7)

# 5. Visual 2 (Top-Right): Credit Loss Isolation Forest Anomaly Detection
v2_box = patches.FancyBboxPatch((0.63, 0.38), 0.34, 0.34, boxstyle='round,pad=0.008,rounding_size=0.015',
                               facecolor='#162032', edgecolor='#334155', linewidth=1)
ax.add_patch(v2_box)
ax.text(0.645, 0.69, 'Credit Risk: Provision for Credit Losses ($B)', color='#FFFFFF', fontsize=10.5, fontweight='bold')
ax.text(0.645, 0.67, 'Isolation Forest Anomaly Detection: Outliers Flagged in Crimson', color='#94A3B8', fontsize=7.5)

# Subplot for Visual 2
ax2 = fig.add_axes([0.655, 0.41, 0.30, 0.24], facecolor='#162032')
provisions = (df['Provision_for_credit_losses'] / 1000).values
bar_colors = []
for i, flag in enumerate(df['ml_anomaly_flag']):
    if 'Anomaly' in str(flag):
        bar_colors.append('#EF4444')  # Red outlier
    elif df['is_forecast'].iloc[i] == 'ML Forecast Period':
        bar_colors.append('#6366F1')  # Forecast purple
    else:
        bar_colors.append('#3B82F6')  # Normal blue

bars = ax2.bar(x, provisions, color=bar_colors, width=0.55, edgecolor='#334155', linewidth=0.5)
# Add annotation for Q4-2025 spike
ax2.annotate('CRE Stress Spike\n$4.65B (Outlier)', xy=(4, 4.65), xytext=(2.2, 4.8),
             arrowprops=dict(facecolor='#EF4444', shrink=0.05, width=1, headwidth=4),
             color='#EF4444', fontsize=6.5, fontweight='bold')

ax2.set_xticks(x)
ax2.set_xticklabels(quarters, color='#94A3B8', fontsize=6.5, rotation=35)
ax2.tick_params(colors='#94A3B8', labelsize=7)
for spine in ax2.spines.values():
    spine.set_color('#334155')
ax2.grid(True, linestyle='--', alpha=0.3, color='#334155')

# 6. Visual 3 (Bottom Half): Model Diagnostics & Anomaly Evaluation Table
v3_box = patches.FancyBboxPatch((0.13, 0.05), 0.84, 0.31, boxstyle='round,pad=0.008,rounding_size=0.015',
                               facecolor='#162032', edgecolor='#334155', linewidth=1)
ax.add_patch(v3_box)
ax.text(0.145, 0.335, 'AI/ML Model Diagnostics & Quarterly Risk Matrix', color='#FFFFFF', fontsize=11, fontweight='bold')
ax.text(0.145, 0.315, 'Evaluating Multi-variate Polynomial Ridge Forecaster & Unsupervised Isolation Forest Decision Scores', color='#94A3B8', fontsize=7.5)

# Render Table Rows
cols = ['Quarter', 'Period Type', 'Actual Rev ($B)', 'Forecast Rev ($B)', '95% CI Lower', '95% CI Upper', 'Credit Prov ($B)', 'Anomaly Decision']
col_x = [0.15, 0.23, 0.33, 0.44, 0.55, 0.64, 0.73, 0.84]

# Table Header
header_y = 0.285
for cx, col_name in zip(col_x, cols):
    ax.text(cx, header_y, col_name, color='#38BDF8', fontsize=7.5, fontweight='bold')

ax.plot([0.145, 0.95], [0.275, 0.275], color='#334155', linewidth=1)

# Display 6 key rows (including anomalies and forward forecast)
sample_indices = [3, 4, 6, 7, 8, 11]  # Q3-25, Q4-25 (Spike), Q2-26 (Surge), Q3-26, Q4-26, Q3-27
row_y = 0.25
for idx in sample_indices:
    row = df.iloc[idx]
    q = row['Quarter']
    ptype = 'Forecast' if row['is_forecast'] == 'ML Forecast Period' else 'Actual'
    act_rev = f"${row['Total_net_revenue']/1000:.2f}" if ptype == 'Actual' else '-'
    fct_rev = f"${row['Total_net_revenue']/1000:.2f}" if ptype == 'Forecast' else '-'
    ci_l = f"${row['Total_net_revenue_lower_95']/1000:.2f}"
    ci_u = f"${row['Total_net_revenue_upper_95']/1000:.2f}"
    prov = f"${row['Provision_for_credit_losses']/1000:.2f}"
    
    is_anomaly = 'Anomaly' in str(row['ml_anomaly_flag'])
    flag_text = 'OUTLIER FLAGGED' if is_anomaly else ('PROJECTED' if ptype == 'Forecast' else 'NORMAL')
    flag_color = '#EF4444' if is_anomaly else ('#A78BFA' if ptype == 'Forecast' else '#34D399')
    
    # Text colors
    tc = '#FFFFFF'
    ax.text(col_x[0], row_y, q, color=tc, fontsize=7.5, fontweight='bold')
    ax.text(col_x[1], row_y, ptype, color='#94A3B8', fontsize=7.5)
    ax.text(col_x[2], row_y, act_rev, color='#38BDF8', fontsize=7.5)
    ax.text(col_x[3], row_y, fct_rev, color='#A78BFA', fontsize=7.5)
    ax.text(col_x[4], row_y, ci_l, color='#94A3B8', fontsize=7.5)
    ax.text(col_x[5], row_y, ci_u, color='#94A3B8', fontsize=7.5)
    ax.text(col_x[6], row_y, prov, color='#F87171' if is_anomaly else '#FFFFFF', fontsize=7.5, fontweight='bold' if is_anomaly else 'normal')
    
    # Badge for flag
    badge = patches.FancyBboxPatch((col_x[7] - 0.005, row_y - 0.008), 0.09, 0.022, boxstyle='round,pad=0.002,rounding_size=0.005',
                                  facecolor='#1E293B', edgecolor=flag_color, linewidth=0.8)
    ax.add_patch(badge)
    ax.text(col_x[7] + 0.04, row_y + 0.002, flag_text, color=flag_color, fontsize=6.5, fontweight='bold', ha='center', va='center')
    
    row_y -= 0.033

out_path = r'C:\Users\soumi\.gemini\antigravity\scratch\financial-performance-analysis\screenshots\10_jpm_dashboard_page3_preview.png'
art_path = r'C:\Users\soumi\.gemini\antigravity\brain\348d2d73-5d0e-4b57-9de6-eec98a33e1d2\jpm_page3_preview.png'
plt.savefig(out_path, dpi=200, facecolor='#0B0F19')
plt.savefig(art_path, dpi=200, facecolor='#0B0F19')
plt.close()
print('Generated Page 3 preview successfully!')

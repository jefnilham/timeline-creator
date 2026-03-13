import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.offsetbox import AnnotationBbox, TextArea, VPacker
import numpy as np
import textwrap
from datetime import datetime

# 1. Load and Clean Data
try:
    df = pd.read_csv('test_data - 5 year.csv')
except FileNotFoundError:
    print("Error: test_data - Copy.csv not found.")
    exit()

df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y', errors='coerce')
df = df.dropna(subset=['Date']).reset_index(drop=True)
df = df.sort_values('Date')

# 3. Setup Figure
fig, ax = plt.subplots(figsize=(24, 12)) # Kept wider for 5-year span

# 4. FY Logic Helpers
def get_fy_info(dt):
    # April start logic
    fy_year = dt.year + 1 if dt.month >= 4 else dt.year
    fy_q = ((dt.month - 4) % 12) // 3 + 1
    return fy_year, fy_q

def get_fy_q_start(dt):
    target_month = ((dt.month - 4) % 12) // 3 * 3 + 4
    year = dt.year if target_month <= dt.month else dt.year - 1
    if target_month > 12:
        target_month -= 12
        year += 1
    return pd.Timestamp(year=year, month=target_month, day=1)

# 5. Background Blocks and Dual-Level Axis Labels
start_date = df['Date'].min() - pd.DateOffset(months=3)
end_date = df['Date'].max() + pd.DateOffset(months=3)
current_q = get_fy_q_start(start_date)
end_q_limit = get_fy_q_start(end_date)

colors = ['#f8f9fa', '#e9ecef']
while current_q <= end_q_limit + pd.DateOffset(months=3):
    next_q = current_q + pd.DateOffset(months=3)
    fy_year, fy_q = get_fy_info(current_q)
    
    # Background Shading
    ax.axvspan(mdates.date2num(current_q), mdates.date2num(next_q), 
               facecolor=colors[0 if (current_q.month // 3) % 2 == 0 else 1], zorder=0)
    
    mid_date = current_q + (next_q - current_q) / 2
    
    # 1. Place the "Q1", "Q2" etc. directly on the axis
    ax.text(mid_date, -0.6, f"Q{fy_q}", ha='center', va='top', 
            color='#495057', fontsize=11, fontweight='bold')
    
    # 2. Place the "FYXX" label only once per year (above the Q labels)
    # We'll center it between Q2 and Q3 (roughly July/Oct period)
    if fy_q == 2:
        # Shift slightly right to be between Q2 and Q3
        fy_mid_pos = current_q + pd.DateOffset(months=3) 
        ax.text(fy_mid_pos, -1.4, f"FY{str(fy_year)[2:]}", ha='center', va='top', 
                color='#212529', fontsize=14, fontweight='black')

    current_q = next_q

# 6. Timeline Center Line
ax.axhline(0, color="#212529", linewidth=2.5, zorder=1)

# 7. Staggered levels
levels = np.tile([6.0, -6.0, 12.0, -12.0, 18.0, -18.0], int(np.ceil(len(df)/6)))[:len(df)]
ax.vlines(df['Date'], 0, levels, color="#adb5bd", linestyle="--", linewidth=1.2)
ax.scatter(df['Date'], [0]*len(df), c='#007bff', s=100, zorder=3, edgecolors='white')

# 8. Build the boxes
for i, (idx, row) in enumerate(df.iterrows()):
    y_pos = levels[i]
    part1 = TextArea(row['Date'].strftime('%d %b %Y'), textprops=dict(color="#333333", fontweight='bold', fontsize=9))
    part2 = TextArea(row['Description'], textprops=dict(color="#007bff", fontweight='bold', fontsize=11))
    wrapped_desc = "\n".join(textwrap.wrap(str(row['Full Description']), width=28))
    part3 = TextArea(wrapped_desc, textprops=dict(color="#555555", fontsize=9))

    texts_vbox = VPacker(children=[part1, part2, part3], align="left", pad=0, sep=4)
    bbox_style = dict(boxstyle='round,pad=0.7,rounding_size=0.2', fc='white', ec='#007bff', alpha=1.0, lw=1.5)
    v_align = 0.0 if y_pos > 0 else 1.0

    ab = AnnotationBbox(texts_vbox, (df['Date'].iloc[i], y_pos), xybox=(0, 0), xycoords='data',
                        boxcoords="offset points", box_alignment=(0.5, v_align), bboxprops=bbox_style)
    ax.add_artist(ab)

# 9. Final Formatting
ax.get_yaxis().set_visible(False)
ax.get_xaxis().set_ticklabels([])
ax.xaxis.set_tick_params(size=0)
ax.set_ylim(-26, 26)

for s in ["left", "top", "right", "bottom"]:
    ax.spines[s].set_visible(False)

plt.title("Strategic Project Roadmap", pad=100, fontsize=24, fontweight='bold')
plt.tight_layout()

# 10. Save
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
filename = f"timeline_fy_grouped_{timestamp}.png"
plt.savefig(filename, dpi=300, bbox_inches='tight')
print(f"Generated: {filename}")
plt.show()


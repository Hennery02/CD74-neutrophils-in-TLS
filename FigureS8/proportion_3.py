import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu
from itertools import combinations
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

GROUP_ORDER = ['nTLS', 'imTLS', 'mTLS']
GROUP_DARK = {'nTLS': '#888787', 'imTLS': '#c89a60', 'mTLS': '#c05a48'}

def pformat_sci(p):
    if p < 0.001:
        exp = int(np.floor(np.log10(p)))
        coef = p / 10**exp
        return f'$P = {coef:.2f} \\times 10^{{{exp}}}$'
    else:
        return f'$P = {p:.3f}$'

plot_df = pd.read_csv('proportion_3_plot_data.csv')
grp_data = {g: plot_df[plot_df['TLS_group'] == g]['Pct'].values for g in GROUP_ORDER}
grp_keys = [g for g in GROUP_ORDER if len(grp_data[g]) >= 3]

vals_all = np.concatenate([grp_data[g] for g in grp_keys])
y_clip = np.percentile(vals_all, 95) * 1.1
y_top = y_clip
y_step = y_top * 0.12

fig, ax = plt.subplots(figsize=(3.2, 3.5))

rng = np.random.default_rng(42)
for i, g in enumerate(grp_keys):
    d = grp_data[g]
    jitter = rng.uniform(-0.20, 0.20, len(d))
    normal = d <= y_clip
    clipped = ~normal
    ax.scatter(i + 1 + jitter[normal], d[normal],
               color=GROUP_DARK[g], s=18, alpha=0.60,
               zorder=2, edgecolors='none')
    if clipped.any():
        ax.scatter(i + 1 + jitter[clipped], np.full(clipped.sum(), y_clip * 0.97),
                   color=GROUP_DARK[g], s=22, alpha=0.80,
                   zorder=2, edgecolors='none', marker='^')

CAP_W = 0.18
for i, g in enumerate(grp_keys):
    d = grp_data[g]
    x = i + 1
    p5 = np.percentile(d, 5)
    p95 = min(np.percentile(d, 95), y_clip)
    med = np.median(d)
    ax.plot([x, x], [p5, p95], color='#444444', linewidth=1.2, zorder=4)
    ax.plot([x - CAP_W, x + CAP_W], [p5, p5], color='#444444', linewidth=1.2, zorder=4)
    ax.plot([x - CAP_W, x + CAP_W], [p95, p95], color='#444444', linewidth=1.2, zorder=4)
    ax.plot([x - CAP_W, x + CAP_W], [med, med], color='black', linewidth=2.5, zorder=5)

pair_list = list(combinations(range(len(grp_keys)), 2))
for idx, (i, j) in enumerate(pair_list):
    g1, g2 = grp_keys[i], grp_keys[j]
    _, p = mannwhitneyu(grp_data[g1], grp_data[g2], alternative='two-sided')
    y_line = y_top + y_step * idx
    tick_h = y_step * 0.07
    ax.plot([i + 1, i + 1, j + 1, j + 1],
            [y_line, y_line + tick_h, y_line + tick_h, y_line],
            color='black', linewidth=0.9, clip_on=False)
    pstr = pformat_sci(p)
    ax.text((i + j) / 2 + 1, y_line + tick_h * 1.3, pstr,
            ha='center', va='bottom', fontsize=7.5, color='black')

ax.set_xticks(range(1, len(grp_keys) + 1))
ax.set_xticklabels(grp_keys, fontsize=9, rotation=45, ha='right')
ax.set_ylabel('Proportion of total cells (%)', fontsize=9)
ax.set_ylim(0, y_top + y_step * (len(pair_list) + 0.8))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

for i, g in enumerate(grp_keys):
    ax.text(i + 1, -y_top * 0.12, f'n={len(grp_data[g])}',
            ha='center', va='top', fontsize=7.5, color='#555555',
            transform=ax.transData)

ymax_val = ax.get_ylim()[1]
if ymax_val < 0.5:
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))
elif ymax_val < 2:
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
elif ymax_val < 10:
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))
else:
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.0f'))

plt.tight_layout()
plt.savefig('proportion_3.pdf', bbox_inches='tight')

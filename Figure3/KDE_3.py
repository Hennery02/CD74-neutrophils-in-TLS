import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde, mannwhitneyu, kruskal
from itertools import combinations
import matplotlib.pyplot as plt

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

GROUP_COLORS = {'nTLS': '#cecdcd', 'imTLS': '#edd2ad', 'mTLS': '#e6a499'}
LINE_COLORS = {'nTLS': '#999898', 'imTLS': '#c89a60', 'mTLS': '#c05a48'}
WINDOW_RADIUS = 300
plot_order = ['nTLS', 'imTLS', 'mTLS']

raw = pd.read_csv('KDE_3_plot_data.csv')

x_grid = np.linspace(0, WINDOW_RADIUS, 500)

grp_data = {}
grp_y = {}
n_cores_map = {}

for grp in plot_order:
    sub = raw[raw['TLS_group'] == grp]
    if len(sub) == 0:
        continue
    d = sub['nn_distance_um'].values
    w = sub['weight'].values
    n_cores_map[grp] = int(sub['n_cores'].iloc[0])
    grp_data[grp] = d

    kde_fn = gaussian_kde(d, bw_method=0.20, weights=w / w.sum())
    y_density = kde_fn(x_grid)
    scale = w.sum()
    grp_y[grp] = y_density * scale

fig, ax = plt.subplots(figsize=(5, 5))

legend_handles = []
for grp in plot_order:
    if grp not in grp_data:
        continue
    d = grp_data[grp]
    y = grp_y[grp]
    med = np.median(d)

    ax.fill_between(x_grid, y, alpha=0.40, color=GROUP_COLORS[grp])
    line, = ax.plot(x_grid, y, color=LINE_COLORS[grp], linewidth=2.0)
    ax.axvline(med, color=LINE_COLORS[grp], linestyle='--', linewidth=1.3)
    legend_handles.append((line, f'{grp}  Median: {med:.1f} µm  (n={n_cores_map[grp]})'))

ax.legend([h for h, _ in legend_handles],
          [lb for _, lb in legend_handles],
          fontsize=8, frameon=False, loc='upper left',
          handlelength=1.2, labelspacing=0.4)

stat_grps = [g for g in plot_order if g in grp_data]
vals = [grp_data[g] for g in stat_grps]
if len(vals) >= 2:
    _, p_kw = kruskal(*vals)
    stat_lines = [f'KW p = {p_kw:.4f}']
    for g1, g2 in combinations(stat_grps, 2):
        _, p1 = mannwhitneyu(grp_data[g1], grp_data[g2], alternative='two-sided')
        pstr = 'p < 0.001' if p1 < 0.001 else f'p = {p1:.3f}'
        stat_lines.append(f'{g1} vs {g2}: {pstr}')
    ax.text(0.97, 0.05, '\n'.join(stat_lines),
            transform=ax.transAxes, ha='right', va='bottom', fontsize=8,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                      alpha=0.85, edgecolor='#cccccc', linewidth=0.8))

ax.set_xlim(0, WINDOW_RADIUS)
ax.set_ylim(bottom=0)
ax.set_xlabel('Distance (µm)', fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylabel('Frequency per million total cells', fontsize=9)

plt.tight_layout()
plt.savefig('KDE_3.pdf', bbox_inches='tight')

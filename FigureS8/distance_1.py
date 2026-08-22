import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu
from itertools import combinations
import matplotlib.pyplot as plt

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

GROUP_ORDER = ['nTLS', 'imTLS', 'mTLS']
GROUP_COLORS = {'nTLS': '#cecdcd', 'imTLS': '#edd2ad', 'mTLS': '#e6a499'}
GROUP_DARK = {'nTLS': '#888787', 'imTLS': '#b8852a', 'mTLS': '#b84030'}

df = pd.read_csv('distance_1_plot_data.csv')
n_cores = pd.read_csv('distance_1_n_cores.csv').set_index('TLS_group')['n_cores'].to_dict()

grp_data = {g: df[df['TLS_group'] == g]['nn_distance_um'].values for g in GROUP_ORDER}
grp_keys = [g for g in GROUP_ORDER if len(grp_data[g]) >= 3]

fig, ax = plt.subplots(figsize=(4.5, 5))

x_pos = list(range(len(grp_keys)))
medians = [np.median(grp_data[g]) for g in grp_keys]
iqr_lo = [np.percentile(grp_data[g], 25) for g in grp_keys]
iqr_hi = [np.percentile(grp_data[g], 75) for g in grp_keys]
yerr_lo = [medians[i] - iqr_lo[i] for i in range(len(grp_keys))]
yerr_hi = [iqr_hi[i] - medians[i] for i in range(len(grp_keys))]

ax.bar(x_pos, medians, yerr=[yerr_lo, yerr_hi],
       color=[GROUP_COLORS[g] for g in grp_keys],
       edgecolor='black', linewidth=0.8, alpha=0.85,
       width=0.55, capsize=4, error_kw={'linewidth': 1.2})

rng = np.random.default_rng(0)
for i, grp in enumerate(grp_keys):
    d = grp_data[grp]
    idx = rng.choice(len(d), min(500, len(d)), replace=False)
    jitter = rng.uniform(-0.18, 0.18, len(idx))
    ax.scatter(i + jitter, d[idx],
               color=GROUP_DARK[grp], s=6, alpha=0.35, zorder=3, edgecolors='none')

y_max = max(np.percentile(grp_data[g], 95) for g in grp_keys)
y_step = y_max * 0.14
for idx2, (i, j) in enumerate(combinations(range(len(grp_keys)), 2)):
    g1, g2 = grp_keys[i], grp_keys[j]
    _, p1 = mannwhitneyu(grp_data[g1], grp_data[g2], alternative='two-sided')
    y_line = y_max + y_step * (idx2 + 1)
    ax.plot([i, j], [y_line, y_line], color='black', linewidth=0.9)
    pstr = 'p<0.001' if p1 < 0.001 else f'p={p1:.3f}'
    ax.text((i + j) / 2, y_line + y_step * 0.1, pstr,
            ha='center', va='bottom', fontsize=7.5,
            color='#c0392b' if p1 < 0.05 else '#888888')

n_labels = [f'{g}\n(n={n_cores[g]} cores)' for g in grp_keys]
ax.set_xticks(x_pos)
ax.set_xticklabels(n_labels, fontsize=9)
ax.set_ylabel('Median nearest-neighbor distance (µm)', fontsize=9)
ax.set_ylim(0, y_max + y_step * (len(list(combinations(grp_keys, 2))) + 2))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('distance_1.pdf', bbox_inches='tight')

import numpy as np
import pandas as pd
from itertools import combinations
import matplotlib as mpl
import matplotlib.pyplot as plt

POINTS_CSV = 'distance_1_points.csv'
SUMMARY_CSV = 'distance_1_summary.csv'
PAIRS_CSV = 'distance_1_dunn_holm.csv'
OUT_PDF = 'distance_1.pdf'

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

GROUP_COLORS = {'nTLS': '#cecdcd', 'imTLS': '#edd2ad', 'mTLS': '#e6a499'}
GROUP_DARK = {'nTLS': '#888787', 'imTLS': '#b8852a', 'mTLS': '#b84030'}
ORDER = ['nTLS', 'imTLS', 'mTLS']


def draw_bar(points, summary, pairs, out):
    fig, ax = plt.subplots(figsize=(4.7, 5))
    grp_keys = [g for g in ORDER if g in set(summary['TLS_group'])]
    x_pos = list(range(len(grp_keys)))
    s = summary.set_index('TLS_group')
    medians = [s.loc[g, 'median'] for g in grp_keys]
    yerr_lo = [s.loc[g, 'median'] - s.loc[g, 'q25'] for g in grp_keys]
    yerr_hi = [s.loc[g, 'q75'] - s.loc[g, 'median'] for g in grp_keys]
    ax.bar(x_pos, medians, yerr=[yerr_lo, yerr_hi], color=[GROUP_COLORS[g] for g in grp_keys],
           edgecolor='black', linewidth=0.8, alpha=0.85, width=0.55, capsize=4, error_kw={'linewidth': 1.2})
    rng = np.random.default_rng(0)
    for i, grp in enumerate(grp_keys):
        v = points.loc[points['TLS_group'] == grp, 'median_nn_distance_um'].values
        idx = rng.choice(len(v), min(500, len(v)), replace=False)
        jitter = rng.uniform(-0.18, 0.18, len(idx))
        ax.scatter(i + jitter, v[idx], color=GROUP_DARK[grp], s=6, alpha=0.35, zorder=3, edgecolors='none')
    y_max = points['median_nn_distance_um'].max()
    y_step = y_max * 0.075
    for k, (a, b) in enumerate(combinations(range(len(grp_keys)), 2)):
        g1, g2 = grp_keys[a], grp_keys[b]
        p1 = pairs[(pairs['group1'] == g1) & (pairs['group2'] == g2)]['p'].iloc[0]
        y_line = y_max + y_step * (k + 1)
        ax.plot([a, b], [y_line, y_line], color='black', linewidth=0.9)
        ax.text((a + b) / 2, y_line + y_step * 0.1, 'p<0.001' if p1 < 0.001 else f'p={p1:.3f}',
                ha='center', va='bottom', fontsize=7.5, color='#c0392b' if p1 < 0.05 else '#888888')
    ax.set_xticks(x_pos)
    ax.set_xticklabels([f"{g}\n(n={int(s.loc[g, 'n_cores'])} cores)" for g in grp_keys], fontsize=9)
    ax.set_ylabel('Median nearest-neighbor distance per core (\u00b5m)', fontsize=9)
    ax.set_ylim(0, y_max + y_step * (len(list(combinations(grp_keys, 2))) + 1.8))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    fig.savefig(out, bbox_inches='tight')

points = pd.read_csv(POINTS_CSV)
summary = pd.read_csv(SUMMARY_CSV)
pairs = pd.read_csv(PAIRS_CSV)
draw_bar(points, summary, pairs, OUT_PDF)

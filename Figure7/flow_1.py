import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

DATA_CSV = 'flow_1_plot_data.csv'
STATS_CSV = 'flow_1_stats.csv'
OUT_PDF = 'flow_1.pdf'
ITEMS = [('item_1', 'CellType_D in Lineage_C (%)')]

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

PALETTE = {'group1': '#7C9CB4', 'group2': '#C97B8A', 'group3': '#B3BB81', 'group4': '#8A81BB',
           'group5': '#8FA888', 'group6': '#C9A27B', 'group7': '#81BB99', 'group8': '#BB81BB'}
ORDER = ['group1', 'group2', 'group3', 'group4', 'group5', 'group6', 'group7', 'group8']


def fmt_p(p):
    return 'P < 0.0001' if p < 0.0001 else f'P = {p:.4f}'


def draw_panel(ax, df, st, ylabel):
    groups = [g for g in ORDER if g in set(df['trt'])]
    rng = np.random.default_rng(0)
    for i, g in enumerate(groups):
        v = df.loc[df['trt'] == g, 'Group1'].values
        ax.scatter(i + rng.uniform(-0.12, 0.12, len(v)), v, s=60, color=PALETTE[g], alpha=0.85, linewidths=0, zorder=3)
        m, se = v.mean(), v.std(ddof=1) / np.sqrt(len(v))
        ax.errorbar(i, m, yerr=se, color='black', capsize=3, linewidth=1.3, zorder=4)
        ax.plot([i - 0.18, i + 0.18], [m, m], color='black', linewidth=1.8, zorder=4)
    ymax = df['Group1'].max()
    sig = st[st['p_adj'] < 0.05].reset_index(drop=True)
    step = ymax * 0.10
    for k, r in sig.iterrows():
        a, b = groups.index(r['group1']), groups.index(r['group2'])
        y = ymax + step * (k + 1)
        ax.plot([a, a, b, b], [y - step * 0.2, y, y, y - step * 0.2], color='black', linewidth=1)
        ax.text((a + b) / 2, y, fmt_p(r['p_adj']), ha='center', va='bottom', fontsize=8)
    ax.set_xticks(range(len(groups)))
    ax.set_xticklabels([''] * len(groups))
    for i, g in enumerate(groups):
        ax.scatter(i, -0.05, s=70, color=PALETTE[g], transform=ax.get_xaxis_transform(), clip_on=False)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.set_ylim(bottom=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


data = pd.read_csv(DATA_CSV)
stt = pd.read_csv(STATS_CSV)
fig, axes = plt.subplots(1, 1, figsize=(4.5, 4.5))
axes = np.atleast_1d(axes)
for ax, (name, ylabel) in zip(axes, ITEMS):
    draw_panel(ax, data[data['panel'] == name], stt[stt['panel'] == name], ylabel)
plt.tight_layout()
plt.savefig(OUT_PDF, bbox_inches='tight')

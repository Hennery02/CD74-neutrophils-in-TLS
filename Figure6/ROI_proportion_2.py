import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

DATA_CSV = 'ROI_proportion_2_plot_data.csv'
STATS_CSV = 'ROI_proportion_2_stats.csv'
OUT_PDF = 'ROI_proportion_2.pdf'
ITEMS = [('item_1', 'LTβ⁺ Lineage_D in ROI (%)'), ('item_2', 'LTβ⁺ Lineage_B in ROI (%)')]

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

GROUPS = ['group1', 'group2', 'group3', 'group4']
COLORS = {'group1': '#7C9CB4', 'group2': '#8FA888', 'group3': '#C97B8A', 'group4': '#C9A27B'}


def fmt_p(p):
    if p < 0.0001:
        return 'P < 0.0001'
    return f'P = {p:.4f}'.rstrip('0') if p < 0.001 else f'P = {p:.4f}'


def draw_panel(ax, df, st, ylabel):
    rng = np.random.default_rng(0)
    for i, g in enumerate(GROUPS):
        v = df.loc[df['trt'] == g, 'Group1'].values
        ax.scatter(i + rng.uniform(-0.12, 0.12, len(v)), v, s=70, color=COLORS[g], alpha=0.8, linewidths=0, zorder=3)
        m, se = v.mean(), v.std(ddof=1) / np.sqrt(len(v))
        ax.errorbar(i, m, yerr=se, color='black', capsize=4, linewidth=1.5, zorder=4)
        ax.plot([i - 0.18, i + 0.18], [m, m], color='black', linewidth=2, zorder=4)
    ymax = df['Group1'].max()
    sig = st[st['p_adj'] < 0.05].reset_index(drop=True)
    step = ymax * 0.12
    for k, r in sig.iterrows():
        a, b = GROUPS.index(r['group1']), GROUPS.index(r['group2'])
        y = ymax + step * (k + 1)
        ax.plot([a, a, b, b], [y - step * 0.2, y, y, y - step * 0.2], color='black', linewidth=1)
        ax.text((a + b) / 2, y, fmt_p(r['p_adj']), ha='center', va='bottom', fontsize=9)
    ax.set_xticks(range(len(GROUPS)))
    ax.set_xticklabels([''] * len(GROUPS))
    for i, g in enumerate(GROUPS):
        ax.scatter(i, -0.07, s=90, color=COLORS[g], transform=ax.get_xaxis_transform(), clip_on=False)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_ylim(bottom=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


data = pd.read_csv(DATA_CSV)
stt = pd.read_csv(STATS_CSV)
fig, axes = plt.subplots(1, 2, figsize=(9, 4.5))
for ax, (name, ylabel) in zip(axes, ITEMS):
    draw_panel(ax, data[data['panel'] == name], stt[stt['panel'] == name], ylabel)
plt.tight_layout()
plt.savefig(OUT_PDF, bbox_inches='tight')

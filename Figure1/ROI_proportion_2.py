import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

DATA_CSV = 'ROI_proportion_2_plot_data.csv'
STATS_CSV = 'ROI_proportion_2_stats.csv'
OUT_PDF = 'ROI_proportion_2.pdf'
YLABEL = 'Proportion of cells in ROI (%)'

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

PALETTE = {'mTLS': '#e6a499', 'imTLS': '#edd2ad', 'nTLS': '#cecdcd'}
ORDER = ['mTLS', 'imTLS', 'nTLS']


def fmt_p(p):
    return 'P < 0.0001' if p < 0.0001 else f'P = {p:.4f}'


def draw_panel(ax, df, st, ylabel):
    rng = np.random.default_rng(0)
    for i, g in enumerate(ORDER):
        v = df.loc[df['trt'] == g, 'Group1'].values
        ax.scatter(i + rng.uniform(-0.12, 0.12, len(v)), v, s=70, color=PALETTE[g], edgecolor='#555555',
                   linewidths=0.5, alpha=0.95, zorder=3)
        m, se = v.mean(), v.std(ddof=1) / np.sqrt(len(v))
        ax.errorbar(i, m, yerr=se, color='black', capsize=4, linewidth=1.3, zorder=4)
        ax.plot([i - 0.18, i + 0.18], [m, m], color='black', linewidth=1.8, zorder=4)
    ymax = df['Group1'].max()
    sig = st[st['p_adj'] < 0.05].reset_index(drop=True)
    step = ymax * 0.12
    for k, r in sig.iterrows():
        a, b = ORDER.index(r['group1']), ORDER.index(r['group2'])
        y = ymax + step * (k + 1)
        ax.plot([a, a, b, b], [y - step * 0.2, y, y, y - step * 0.2], color='black', linewidth=1)
        ax.text((a + b) / 2, y, fmt_p(r['p_adj']), ha='center', va='bottom', fontsize=9)
    ax.set_xticks(range(len(ORDER)))
    ax.set_xticklabels(ORDER, rotation=45, ha='right')
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_ylim(bottom=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

df = pd.read_csv(DATA_CSV)
st = pd.read_csv(STATS_CSV)
fig, ax = plt.subplots(figsize=(3.6, 4.6))
draw_panel(ax, df, st, YLABEL)
plt.tight_layout()
plt.savefig(OUT_PDF, bbox_inches='tight')

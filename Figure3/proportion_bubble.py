import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import LinearSegmentedColormap

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

plot_df = pd.read_csv("proportion_bubble_plot_data.csv")

PAIRS_LABELS = ['imTLS vs nTLS', 'mTLS vs nTLS', 'mTLS vs imTLS']
CELL_LABELS = plot_df.drop_duplicates('cell_type')['label'].tolist()

n_rows = len(PAIRS_LABELS)
n_cols = len(CELL_LABELS)

lor_mat = np.zeros((n_rows, n_cols))
logp_mat = np.zeros((n_rows, n_cols))
p_mat = np.ones((n_rows, n_cols))

for i, pair_label in enumerate(PAIRS_LABELS):
    for j, label in enumerate(CELL_LABELS):
        row = plot_df[(plot_df.comparison == pair_label) & (plot_df.label == label)]
        if len(row):
            lor_mat[i, j] = row['log2_odds_ratio'].values[0]
            p_mat[i, j] = row['p_value'].values[0]
            logp_mat[i, j] = row['neglog10_p'].values[0]

max_logp = max(logp_mat.max(), 1)
SIZE_MAX = 800
size_mat = (logp_mat / max(max_logp, 1)) * SIZE_MAX
size_mat = np.clip(size_mat, 60, SIZE_MAX)

lor_clip = np.clip(lor_mat, 0, 6)

fig, ax = plt.subplots(figsize=(7.5, 3.5))

cmap = LinearSegmentedColormap.from_list('OrRd_custom', [
    (0 / 6, '#fdd49e'),
    (1.5 / 6, '#e34a33'),
    (2 / 6, '#b30000'),
    (4 / 6, '#7f0000'),
    (6 / 6, '#4a0000'),
])
norm = plt.Normalize(vmin=0, vmax=6)

for i in range(n_rows):
    for j in range(n_cols):
        color = cmap(norm(lor_clip[i, j]))
        ax.scatter(j, n_rows - 1 - i, s=size_mat[i, j], color=color,
                   alpha=0.9, edgecolors='white', linewidth=0.8, zorder=3)

ax.set_xlim(-0.6, n_cols - 0.4)
ax.set_ylim(-0.6, n_rows - 0.4)
ax.set_xticks(range(n_cols))
ax.set_xticklabels(CELL_LABELS, fontsize=10, rotation=30, ha='right')
ax.set_yticks(range(n_rows))
ax.set_yticklabels(PAIRS_LABELS[::-1], fontsize=10)
ax.set_facecolor('#f9f9f9')
ax.grid(True, color='white', linewidth=1.5, zorder=0)
ax.spines[:].set_visible(False)
ax.tick_params(length=0)

sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, fraction=0.025, pad=0.02, aspect=15)
cbar.set_label('log₂(odds ratio)', fontsize=9)
cbar.set_ticks([0, 1, 2, 3, 4, 5, 6])
cbar.ax.tick_params(labelsize=8)

legend_vals = [1, 10, 30]
legend_handles = []
for lv in legend_vals:
    sz = (lv / max(max_logp, 1)) * SIZE_MAX
    sz = np.clip(sz, 10, SIZE_MAX)
    h = Line2D([0], [0], marker='o', color='w', markerfacecolor='#888888',
               markersize=np.sqrt(sz / np.pi) * 1.5, label=f'{lv}', alpha=0.85)
    legend_handles.append(h)
ax.legend(handles=legend_handles, title='-log₁₀(P)', title_fontsize=8, fontsize=8, frameon=False,
          bbox_to_anchor=(1.28, 0.55), loc='center left', handletextpad=0.5, labelspacing=0.8)

plt.tight_layout()
plt.savefig('proportion_bubble.pdf', bbox_inches='tight')

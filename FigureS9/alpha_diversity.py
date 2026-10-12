import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DATA_CSV = 'alpha_diversity_plot_data.csv'
STATS_CSV = 'alpha_diversity_stats.csv'
OUT_PDF = 'alpha_diversity.pdf'

plt.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
    "font.family": "DejaVu Sans", "font.size": 12,
    "axes.spines.top": True, "axes.spines.right": True, "axes.spines.left": True, "axes.spines.bottom": True,
    "axes.linewidth": 1.0, "axes.edgecolor": "black", "axes.facecolor": "white", "figure.facecolor": "white",
    "xtick.direction": "out", "ytick.direction": "out", "xtick.color": "black", "ytick.color": "black",
    "legend.frameon": False, "legend.title_fontsize": 12,
})

GROUP_ORDER = ["none", "immature", "mature"]
GROUP_COLORS = {"none": "#cecdcd", "immature": "#edd2ad", "mature": "#e6a499"}

METRICS = ["Observed", "Chao1", "Shannon", "Simpson"]


def draw_alpha(df, pvals, out):
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.8))
    for ax, metric in zip(axes, METRICS):
        for pos, g in enumerate(GROUP_ORDER):
            vals = df.loc[df["group"] == g, metric].values
            if len(vals) == 0:
                continue
            rng = np.random.default_rng(0)
            jitter = rng.uniform(-0.08, 0.08, size=len(vals))
            ax.scatter(np.full(len(vals), pos) + jitter, vals, color=GROUP_COLORS[g],
                       edgecolor="black", linewidth=0.5, s=45, zorder=3)
            ax.hlines(np.mean(vals), pos - 0.2, pos + 0.2, color="black", linewidth=1.5, zorder=4)
        ax.set_xticks(range(len(GROUP_ORDER)))
        ax.set_xticklabels(GROUP_ORDER, fontsize=9)
        ax.set_title(f"P = {pvals[metric]:.4f}", fontsize=9)
        ax.set_ylabel(metric)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")


df = pd.read_csv(DATA_CSV, index_col=0)
pvals = pd.read_csv(STATS_CSV, index_col=0)["kruskal_p"].to_dict()
draw_alpha(df, pvals, OUT_PDF)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DATA_CSV = 'gram_stain_plot_data.csv'
STATS_CSV = 'gram_stain_stats.csv'
OUT_PDF = 'gram_stain.pdf'

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

BINARY_ORDER = ["rest", "mature"]
BINARY_COLORS = {"rest": "#cecdcd", "mature": GROUP_COLORS["mature"]}


def style_axes_grid(ax, axis="y"):
    ax.grid(axis=axis, color="grey", linestyle="--", linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)

ROWS = ["Gram_negative_total", "Gram_positive_total"]
LABELS = ["Gram-negative", "Gram-positive"]


def draw_gram(long_df, pvals, out):
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 5))
    for ax, row, label in zip(axes, ROWS, LABELS):
        for pos, bg in enumerate(BINARY_ORDER):
            d = long_df[(long_df["metric"] == row) & (long_df["binary_group"] == bg)]["value"].values
            rng = np.random.default_rng(0)
            jitter = rng.uniform(-0.08, 0.08, size=len(d))
            ax.scatter(np.full(len(d), pos) + jitter, d, color=BINARY_COLORS[bg],
                       edgecolor="black", linewidth=0.6, s=65, zorder=3)
            ax.hlines(np.mean(d), pos - 0.2, pos + 0.2, color="black", linewidth=1.5, zorder=4)
        ax.set_xticks(range(len(BINARY_ORDER)))
        ax.set_xticklabels(BINARY_ORDER, fontsize=10)
        ax.set_title(f"{label}\nP = {pvals[row]:.4f}", fontsize=9)
        ax.set_ylabel("Summed relative abundance (%)")
        style_axes_grid(ax, axis="y")
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")


long_df = pd.read_csv(DATA_CSV)
pvals = pd.read_csv(STATS_CSV, index_col=0)["pvalue"].to_dict()
draw_gram(long_df, pvals, OUT_PDF)

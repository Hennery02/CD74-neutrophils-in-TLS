import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

DATA_CSV = 'beta_diversity_plot_data.csv'
STATS_CSV = 'beta_diversity_stats.csv'
OUT_PDF = 'beta_diversity.pdf'

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


def confidence_ellipse(ax, x, y, n_std=2.4477, edgecolor="black", facecolor="none", **kwargs):
    if len(x) < 3:
        return None
    cov = np.cov(x, y)
    eigvals, eigvecs = np.linalg.eigh(cov)
    order = eigvals.argsort()[::-1]
    eigvals, eigvecs = eigvals[order], eigvecs[:, order]
    angle = np.degrees(np.arctan2(eigvecs[1, 0], eigvecs[0, 0]))
    width, height = 2 * n_std * np.sqrt(np.clip(eigvals, 0, None))
    ell = Ellipse((np.mean(x), np.mean(y)), width, height, angle=angle,
                  edgecolor=edgecolor, facecolor=facecolor, **kwargs)
    ax.add_patch(ell)
    return ell


def draw_beta(coords, var_exp, r2, p, out):
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    for bg in BINARY_ORDER:
        sub = coords[coords["binary_group"] == bg]
        confidence_ellipse(ax, sub["PCo1"].values, sub["PCo2"].values,
                           edgecolor=BINARY_COLORS[bg], facecolor=BINARY_COLORS[bg], alpha=0.12,
                           linewidth=1.6, linestyle="--", zorder=1)
    for g in GROUP_ORDER:
        sub = coords[coords["group"] == g]
        ax.scatter(sub["PCo1"], sub["PCo2"], color=GROUP_COLORS[g], edgecolor="black", linewidth=0.6,
                   s=90, label=g, zorder=3)
    ax.set_xlabel(f"PCo1 ({var_exp[0]*100:.1f}%)")
    ax.set_ylabel(f"PCo2 ({var_exp[1]*100:.1f}%)")
    ax.set_title(f"R\u00b2 = {r2:.3f}, P = {p:.4f}", fontsize=10.5)
    ax.legend(frameon=False, loc="best")
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")


coords = pd.read_csv(DATA_CSV, index_col=0)
st = pd.read_csv(STATS_CSV).iloc[0]
draw_beta(coords, [st["var_PCo1"], st["var_PCo2"]], st["R2"], st["p_value"], OUT_PDF)

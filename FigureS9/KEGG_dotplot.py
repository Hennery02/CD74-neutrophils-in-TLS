import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

DATA_CSV = 'KEGG_dotplot_plot_data.csv'
OUT_PDF = 'KEGG_dotplot.pdf'

plt.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
    "font.family": "DejaVu Sans", "font.size": 12,
    "axes.spines.top": True, "axes.spines.right": True, "axes.spines.left": True, "axes.spines.bottom": True,
    "axes.linewidth": 1.0, "axes.edgecolor": "black", "axes.facecolor": "white", "figure.facecolor": "white",
    "xtick.direction": "out", "ytick.direction": "out", "xtick.color": "black", "ytick.color": "black",
    "legend.frameon": False, "legend.title_fontsize": 12,
})


def style_axes_grid(ax, axis="y"):
    ax.grid(axis=axis, color="grey", linestyle="--", linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)


def style_legend(ax, title, **kwargs):
    kwargs.setdefault("loc", "upper left")
    kwargs.setdefault("bbox_to_anchor", (1.02, 1))
    kwargs.setdefault("frameon", False)
    leg = ax.legend(title=title, **kwargs)
    if leg is not None and leg.get_title() is not None:
        leg.get_title().set_ha("left")
    return leg


def draw_dotplot(res, out):
    res = res.sort_values("log2fc")
    fig = plt.figure(figsize=(10, 6.5))
    ax = fig.add_axes([0.34, 0.12, 0.42, 0.78])
    size_min, size_max = 40, 500
    log_abund = np.log10(res["mean_overall"])
    sizes = size_min + (size_max - size_min) * (log_abund - log_abund.min()) / (log_abund.max() - log_abund.min())
    cmap = plt.get_cmap("Reds")
    norm = plt.Normalize(vmin=0, vmax=res["neglog10p"].max() * 1.05)
    y = np.arange(len(res))
    ax.axvline(0, color="black", linewidth=0.8, zorder=2)
    sc = ax.scatter(res["log2fc"], y, s=sizes, c=res["neglog10p"], cmap=cmap, norm=norm,
                    edgecolor="black", linewidth=0.8, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(res["nice_name"], fontsize=9.5)
    ax.set_xlabel(r"$\log_2$(mature / rest)")
    ax.set_ylim(-0.8, len(res) - 0.2)
    style_axes_grid(ax, axis="x")
    cax = fig.add_axes([0.79, 0.55, 0.025, 0.35])
    cbar = fig.colorbar(sc, cax=cax)
    cbar.set_label(r"$-\log_{10}(p)$, Mann-Whitney U", fontsize=8.5)
    raw_vals = [res["mean_overall"].min(), res["mean_overall"].median(), res["mean_overall"].max()]
    legend_vals = [round(v / 500) * 500 for v in raw_vals]
    legend_sizes = size_min + (size_max - size_min) * (np.log10(legend_vals) - log_abund.min()) / \
        (log_abund.max() - log_abund.min())
    legend_sizes = np.clip(legend_sizes, size_min * 0.3, None)
    handles = [Line2D([0], [0], marker="o", color="w", markerfacecolor="grey", markeredgecolor="black",
                      markersize=np.sqrt(s / np.pi) * 0.9, label=f"{v:,.0f}")
               for v, s in zip(legend_vals, legend_sizes)]
    legend_ax = fig.add_axes([0.79, 0.12, 0.2, 0.3])
    legend_ax.axis("off")
    style_legend(legend_ax, "Mean normalized\nabundance", handles=handles, loc="upper left",
                 bbox_to_anchor=None, fontsize=8, title_fontsize=8.5, labelspacing=1.6, borderpad=1.2)
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


res = pd.read_csv(DATA_CSV, index_col=0)
draw_dotplot(res, OUT_PDF)

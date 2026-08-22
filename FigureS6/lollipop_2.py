import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
plt.rcParams.update({"font.family": "sans-serif", "font.size": 9})

LABEL_MAP = {
    "RawLabel_06": "Subcluster_7",
    "RawLabel_00": "Subcluster_1",
    "RawLabel_01": "Subcluster_2",
    "RawLabel_02": "Subcluster_3",
    "RawLabel_03": "Subcluster_4",
    "RawLabel_04": "Subcluster_5",
    "RawLabel_05": "Subcluster_6",
}
FIXED_ORDER = sorted(LABEL_MAP.values())
MIN_S, MAX_S = 120, 900


def p_to_size(p):
    nlp = -np.log10(np.clip(p, 1e-6, 1.0))
    nlp_clip = np.clip(nlp, 0, 3)
    return MIN_S + (nlp_clip / 3) * (MAX_S - MIN_S)


R = pd.read_csv("lollipop_correlation_data.csv")
sub = R[R.cell_subtype == "Lineage_A_Subtype_2"].copy()

cmap = plt.get_cmap("RdYlBu_r")
norm = plt.Normalize(-1, 1)

sub["label"] = sub.raw_subtype.map(LABEL_MAP).fillna(sub.raw_subtype)
sub["label"] = pd.Categorical(sub["label"], categories=FIXED_ORDER, ordered=True)
sub = sub.sort_values("label").reset_index(drop=True)

x = np.arange(len(sub))
rho = sub.rho.values
pval = sub.p.values
sizes = p_to_size(pval)
colors = cmap(norm(rho))

fig_w = 0.62 * len(sub) + 1.0
fig, ax = plt.subplots(figsize=(fig_w, 3.2), constrained_layout=True)
ax.vlines(x, 0, rho, color="grey", linewidth=1.4, zorder=1, alpha=0.6)
ax.scatter(x, rho, s=sizes, c=[colors[i] for i in range(len(sub))],
           edgecolors="black", linewidths=1.0, zorder=3)

for i in range(len(sub)):
    r, p, s = rho[i], pval[i], sizes[i]
    sig = "*" if p < 0.05 else ""
    if s >= 500:
        ax.text(x[i], r, f"{r:.2f}{sig}", ha="center", va="center", fontsize=7.5,
                fontweight="bold", color="black", zorder=4)
    else:
        offset = 0.09 if r >= 0 else -0.09
        va = "bottom" if r >= 0 else "top"
        ax.text(x[i], r + offset, f"{r:.2f}{sig}", ha="center", va=va, fontsize=7.5,
                fontweight="bold", color="black", zorder=4)

ax.axhline(0, color="grey", linewidth=0.8, linestyle="--", zorder=0)
ax.set_xticks(x)
ax.set_xticklabels(sub.label, rotation=45, ha="right", fontsize=8.5)
ax.set_xlim(-0.55, len(sub) - 0.45)
ax.set_ylabel("Spearman rho", fontsize=9)
ax.set_ylim(-0.95, 0.95)
for sp in ["top", "right"]:
    ax.spines[sp].set_visible(False)

legend_p = [0.5, 0.05, 0.001]
legend_sizes = [p_to_size(p) for p in legend_p]
legend_ax = ax.inset_axes([1.06, 0.42, 0.34, 0.58])
legend_ax.set_xlim(0, 1)
legend_ax.set_ylim(0, 1)
legend_ax.axis("off")
legend_ax.set_title("p-value", fontsize=7.5, loc="left", pad=2)

max_r = np.sqrt(max(legend_sizes))
y_positions = []
y_cursor = 0.90
for s in legend_sizes:
    r_norm = np.sqrt(s) / max_r
    y_positions.append(y_cursor - r_norm * 0.16)
    y_cursor -= (r_norm * 0.16) * 2 + 0.14
for p, s, y in zip(legend_p, legend_sizes, y_positions):
    legend_ax.scatter([0.28], [y], s=s, c="white", edgecolors="black", linewidths=1.0,
                      transform=legend_ax.transAxes, clip_on=False)
    legend_ax.text(0.62, y, f"p={p}", ha="left", va="center", fontsize=7.5,
                   transform=legend_ax.transAxes)

cbar_ax = ax.inset_axes([1.06, 0.06, 0.10, 0.26])
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cb = fig.colorbar(sm, cax=cbar_ax)
cb.set_label("Spearman rho", fontsize=7.5)
cb.set_ticks([-1, -0.5, 0, 0.5, 1])
cb.ax.tick_params(labelsize=6.5)

fig.savefig("lollipop_2.pdf", bbox_inches="tight")

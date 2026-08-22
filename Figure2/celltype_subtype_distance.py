import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42

OUT_DIR = "."
IN_CSV = "panelE_celltype_subtype_bin_mean.csv"

MATURITY_ORDER = ["immature", "mature"]

LINEAGE_FACTORS = {
    "Lineage_A": [
        "Lineage_A_Subtype_1", "Lineage_A_Subtype_2", "Lineage_A_Subtype_3",
        "Lineage_A_Subtype_4",
    ],
    "Lineage_B": [
        "Lineage_B_Subtype_1", "Lineage_B_Subtype_2", "Lineage_B_Subtype_3",
        "Lineage_B_Subtype_4", "Lineage_B_Subtype_5", "Lineage_B_Subtype_6", "Lineage_B_Subtype_7",
        "Lineage_B_Subtype_8", "Lineage_B_Subtype_9",
    ],
    "Lineage_C": [
        "Subcluster_7", "Subcluster_2", "Subcluster_1",
        "Subcluster_6", "Subcluster_4", "Subcluster_5", "Subcluster_3",
    ],
    "Lineage_D": [
        "Lineage_D_Subtype_1", "Lineage_D_Subtype_2", "Lineage_D_Subtype_3", "Lineage_D_Subtype_4",
        "Lineage_D_Subtype_5", "Lineage_D_Subtype_6", "Lineage_D_Subtype_7", "Lineage_D_Subtype_8",
    ],
}

LINEAGE_DISPLAY_NAMES = {name: name.replace("_", " ") for group in LINEAGE_FACTORS.values() for name in group}

bin_mean = pd.read_csv(IN_CSV)

for lineage, factors in LINEAGE_FACTORS.items():
    lineage_colors = plt.cm.tab20(np.linspace(0, 1, len(factors)))

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
    for ax, mat in zip(axes, MATURITY_ORDER):
        sub = bin_mean[(bin_mean.maturity == mat) & (bin_mean.norm_bin != ">1.0")].sort_values("bin_mid")
        for f, color in zip(factors, lineage_colors):
            vals = sub[f].values
            std = vals.std()
            z = (vals - vals.mean()) / std if std > 0 else vals - vals.mean()
            ax.plot(sub.bin_mid, z, lw=2, marker="o", markersize=3, color=color,
                     label=LINEAGE_DISPLAY_NAMES.get(f, f))
        ax.set_xlabel("Normalized distance to niche anchor\n(0=anchor, 1=niche edge)", fontsize=9)
        ax.axhline(0, color="grey", lw=0.8, ls="--", alpha=0.6)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    axes[0].set_ylabel("Relative abundance (z-scored)", fontsize=10)
    handles, labels_lg = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels_lg, loc="center right", bbox_to_anchor=(1.30, 0.5), fontsize=9, title="Subtype")
    plt.tight_layout(rect=[0, 0, 0.82, 1])

    out = f"{lineage}_distance_gradient"
    fig.savefig(f"{OUT_DIR}/{out}.pdf", dpi=180, bbox_inches="tight")
    fig.savefig(f"{OUT_DIR}/{out}.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}.*")

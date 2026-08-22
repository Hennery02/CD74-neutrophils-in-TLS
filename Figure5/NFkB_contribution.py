import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams["pdf.fonttype"] = 42

SUBTYPES = [
    "Subcluster_1", "Subcluster_2", "Subcluster_3",
    "Subcluster_4", "Subcluster_5", "Subcluster_6",
]
GENES_USE = ["RELB", "NFKB2"]

result_df = pd.read_csv("NFkB_contribution_plot_data.csv")

pivot = result_df.pivot(index="group", columns="gene", values="score")
nwith = result_df.pivot(index="group", columns="gene", values="n_with")
row_order = ["CellType_D"] + SUBTYPES
pivot = pivot.reindex(index=row_order, columns=GENES_USE)
nwith = nwith.reindex(index=row_order, columns=GENES_USE)

short_names = {name: name for name in row_order}
pivot.index = [short_names[r] for r in pivot.index]
nwith.index = pivot.index

annot = pd.DataFrame(index=pivot.index, columns=pivot.columns, dtype=object)
for r in pivot.index:
    for g in pivot.columns:
        v, n = pivot.loc[r, g], nwith.loc[r, g]
        annot.loc[r, g] = f"{v:.4f}\n(n={int(n)})" if not pd.isna(v) else "N/A"

fig, ax = plt.subplots(figsize=(4.5, 6.5))
sns.heatmap(pivot, annot=annot, fmt="", cmap="Reds", linewidths=1.5, linecolor="white", ax=ax,
            annot_kws={"size": 9, "linespacing": 1.4}, cbar_kws={"label": "Contribution score", "shrink": 0.55})
ax.add_patch(plt.Rectangle((0, 0), 2, 1, fill=False, edgecolor="#E74C3C", lw=2.5, clip_on=False))
ax.set_xlabel("Non-canonical NF-κB genes", fontsize=12)
ax.set_ylabel("")
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=12)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=11)
plt.tight_layout()
plt.savefig("NFkB_subtype_contribution_heatmap.pdf", bbox_inches="tight")

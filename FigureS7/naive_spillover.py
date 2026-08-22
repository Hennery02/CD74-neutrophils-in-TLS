import pandas as pd
import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

axis_feat = pd.read_csv("naive_effector_axis_sharing_data.csv")

x = axis_feat["cd74_positive_fraction"].values
y = axis_feat["frac_naive_shared"].values
rho, p = spearmanr(x, y)

fig, ax = plt.subplots(figsize=(4.0, 3.6))
ax.scatter(x, y, s=70, color="#4c72b0", edgecolors="black", linewidths=0.6, zorder=3)
if len(x) >= 3 and np.std(x) > 0:
    k, b = np.polyfit(x, y, 1)
    xs = np.linspace(x.min(), x.max(), 100)
    ax.plot(xs, np.polyval([k, b], xs), color="#c44e52", linewidth=1.5, zorder=2)
sig_mark = "*" if p < 0.05 else ""
ax.text(0.05, 0.95, f"rho={rho:.2f}, p={p:.3f}{sig_mark}\nn={len(x)}",
        transform=ax.transAxes, va="top", ha="left", fontsize=9)
ax.set_xlabel("CellType_D fraction", fontsize=8)
ax.set_ylabel("naive spillover fraction", fontsize=8)
plt.tight_layout()
plt.savefig("naive_spillover_fraction.pdf", bbox_inches="tight")

import pandas as pd
import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

df = pd.read_csv("correlation_1_plot_data.csv")
subtype = 'Lineage_B_Subtype_3'
x = df[subtype]
y = df['CellType_D_pct']

rho, p = spearmanr(x, y)

fig, ax = plt.subplots(figsize=(4, 3.6))
ax.scatter(x, y, s=70, color='#4c72b0', edgecolors='black', linewidths=0.6, zorder=3)
coef = np.polyfit(x, y, 1)
xs = np.linspace(x.min(), x.max(), 100)
ax.plot(xs, np.polyval(coef, xs), color='#c44e52', linewidth=1.5, zorder=2)
sig_mark = '*' if p < 0.05 else ''
ax.text(0.05, 0.95, f'rho={rho:.2f}, p={p:.3f}{sig_mark}\nn={len(x)}',
        transform=ax.transAxes, va='top', ha='left', fontsize=9)
ax.set_xlabel(f'{subtype} (%)', fontsize=9)
ax.set_ylabel('CellType_D (%)', fontsize=9)
plt.tight_layout()
plt.savefig('correlation_1.pdf', bbox_inches='tight')

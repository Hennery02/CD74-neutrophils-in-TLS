import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

df = pd.read_csv("umap_TLS_state_plot_data.csv", index_col=0)

color_map = {'immature': '#9b82bc', 'mature': '#ffb1a4', 'none': '#53b385'}

fig, ax = plt.subplots(figsize=(4, 4))
for cat, color in color_map.items():
    sub = df[df['group'] == cat]
    ax.scatter(sub['UMAP1'], sub['UMAP2'], c=color, s=3, label=cat, rasterized=True)
ax.set_xlabel('UMAP1')
ax.set_ylabel('UMAP2')
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8)
plt.tight_layout()
plt.savefig('_UMAP_TLS_state.pdf', format='pdf', dpi=300, bbox_inches='tight')

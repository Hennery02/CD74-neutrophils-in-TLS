import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

df = pd.read_csv("UMAP_sample_marker_plot_data_deidentified.csv", index_col=0)

categories = sorted(df['sample_marker'].unique())
cmap = cm.get_cmap('tab20', len(categories))
color_map = {cat: cmap(i) for i, cat in enumerate(categories)}

fig, ax = plt.subplots(figsize=(5, 4))
for cat in categories:
    sub = df[df['sample_marker'] == cat]
    ax.scatter(sub['UMAP1'], sub['UMAP2'], c=[color_map[cat]], s=3, label=cat, rasterized=True)
ax.set_xlabel('UMAP1')
ax.set_ylabel('UMAP2')
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=5, ncol=1)
plt.tight_layout()
plt.savefig('UMAP_sample_marker.pdf', format='pdf', dpi=300, bbox_inches='tight')

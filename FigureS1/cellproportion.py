import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

df = pd.read_csv("cell_proportion_plot_data.csv", index_col=0)

custom_colors = ['#845C75', '#D6B16C', '#AD6559', '#72704C', '#8B795D', '#546983', '#8E3B17', '#9A9D5F', '#635277', '#68855C']
color_map = dict(zip(df.columns, custom_colors))

fig, ax = plt.subplots(figsize=(4, 4))
bottom = pd.Series(0, index=df.index)
for ct in df.columns:
    ax.bar(df.index, df[ct], bottom=bottom, label=ct, color=color_map[ct])
    bottom += df[ct]

ax.set_xlabel('sample')
ax.set_ylabel('Cells per Stage')
ax.set_xticklabels(df.index, rotation=90)
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8)
plt.tight_layout()
plt.savefig('cell_proportion.pdf', format='pdf', dpi=300, bbox_inches='tight')

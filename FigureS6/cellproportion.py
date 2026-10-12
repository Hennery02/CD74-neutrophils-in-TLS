import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

df = pd.read_csv("cell_proportion_plot_data.csv", index_col=0)

color_map = {
    'Lineage_A_Subtype_3': '#66c2a5', 'Lineage_A_Subtype_2': '#8da0cb',
    'Lineage_A_Subtype_4': '#ffd92f', 'Lineage_A_Subtype_1': '#b3b3b3',
}
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

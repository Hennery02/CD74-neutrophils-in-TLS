import pandas as pd
import scanpy as sc
import matplotlib
import matplotlib.pyplot as plt

DATA_CSV = 'Lineage_C_gene_trends_plot_data.csv'
OUT_PDF_1 = 'gene_trends_1.pdf'
OUT_PDF_2 = 'gene_trends_2.pdf'
OUT_PDF_3 = 'gene_trends_3.pdf'

sc.settings.set_figure_params(dpi=80, dpi_save=500, facecolor='white')

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['axes.spines.top'] = False
matplotlib.rcParams['axes.spines.right'] = False

df = pd.read_csv(DATA_CSV)

branches = list(df['branch'].unique())
colors = [matplotlib.colors.rgb2hex(c) for c in matplotlib.colormaps['Set2'](range(len(branches)))]


def plot_gene_trends(genes, outfile):
    fig = plt.figure(figsize=[7, 3 * len(genes)])
    for i, gene in enumerate(genes):
        ax = fig.add_subplot(len(genes), 1, i + 1)
        for branch, color in zip(branches, colors):
            sub = df[(df['gene'] == gene) & (df['branch'] == branch)].sort_values('pseudotime')
            ax.plot(sub['pseudotime'], sub['trend'], color=color, label=branch)
            ax.set_xticks([0, 1])
            ax.set_title(gene)
        if i == 0:
            ax.legend()
    plt.savefig(outfile)
    plt.close(fig)


plot_gene_trends(["ISG15", "IFIT1", "MX1", "IFITM3"], OUT_PDF_1)
plot_gene_trends(["IL7R", "CXCR1", "CTSZ", "SELL", "CXCR2", "FOS", "MPO", "IL17A",
                  "CCL3", "CCL4", "HLA-DRA", "CD74", "CSF3R", "FCGR3B"], OUT_PDF_2)
plot_gene_trends(["ICAM1", "LDHA", "VEGFA", "PLAU", "LGALS3", "HIF1A", "NLRP3", "APOE"], OUT_PDF_3)

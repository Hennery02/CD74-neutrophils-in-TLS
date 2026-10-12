import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42


def plot_matrix(csv_path, out_pdf):
    mean_expr = pd.read_csv(csv_path, index_col=0)
    genes = list(mean_expr.columns)
    cell_types = list(mean_expr.index)

    scaled = (mean_expr - mean_expr.min()) / (mean_expr.max() - mean_expr.min())

    fig, ax = plt.subplots(figsize=(0.5 * len(genes) + 2, 0.35 * len(cell_types) + 2))
    im = ax.imshow(scaled.values, cmap='Blues', vmin=0, vmax=1, aspect='auto')

    ax.set_xticks(range(len(genes)))
    ax.set_xticklabels(genes, rotation=90, fontsize=9)
    ax.set_yticks(range(len(cell_types)))
    ax.set_yticklabels(cell_types, fontsize=8)

    for spine in ax.spines.values():
        spine.set_visible(True)
    ax.set_xticks(np.arange(-0.5, len(genes), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(cell_types), 1), minor=True)
    ax.grid(which='minor', color='#dddddd', linewidth=0.5)
    ax.tick_params(which='minor', length=0)

    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label('mean expression', fontsize=9)

    plt.tight_layout()
    plt.savefig(out_pdf, bbox_inches='tight')
    plt.close(fig)


plot_matrix("ligand_matrixplot_plot_data_1.csv", "LR_matrixplot_ligand_1.pdf")
plot_matrix("receptor_matrixplot_plot_data_1.csv", "LR_matrixplot_receptor_1.pdf")
plot_matrix("ligand_matrixplot_plot_data_2.csv", "LR_matrixplot_ligand_2.pdf")
plot_matrix("receptor_matrixplot_plot_data_2.csv", "LR_matrixplot_receptor_2.pdf")

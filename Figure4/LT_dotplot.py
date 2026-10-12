import pandas as pd
import numpy as np
import anndata as ad
import omicverse as ov
import matplotlib
import matplotlib.pyplot as plt

ov.plot_set(font_path='Arial')
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

plot_data = pd.read_csv("dotplot_LTB_plot_data.csv", index_col=0)
marker_genes = [c[:-len("_mean")] for c in plot_data.columns if c.endswith("_mean")]
cell_types = list(plot_data.index)

N = 10000
X_rows = []
obs_cell_type = []
for ct in cell_types:
    block = np.zeros((N, len(marker_genes)))
    for j, gene in enumerate(marker_genes):
        target_mean = plot_data.loc[ct, f"{gene}_mean"]
        frac = plot_data.loc[ct, f"{gene}_fraction"]
        n_pos = int(round(frac * N))
        n_pos = min(max(n_pos, 0), N)
        n_neg = N - n_pos
        if n_pos == 0:
            v_pos, v_neg = 0.0, target_mean
        elif n_neg == 0:
            v_pos, v_neg = target_mean, 0.0
        else:
            # solve: n_pos*v_pos + n_neg*v_neg = N*target_mean, v_pos>0, v_neg<=0
            v_pos = 1.0
            v_neg = (N * target_mean - n_pos * v_pos) / n_neg
            if v_neg > 0:
                v_neg = 0.0
                v_pos = N * target_mean / n_pos
        col = np.concatenate([np.full(n_pos, v_pos), np.full(n_neg, v_neg)])
        block[:, j] = col
    X_rows.append(block)
    obs_cell_type.extend([ct] * N)

X = np.vstack(X_rows)
adata = ad.AnnData(X=X, var=pd.DataFrame(index=marker_genes))
adata.obs['cell_type'] = pd.Categorical(obs_cell_type, categories=cell_types)

ov.pl.dotplot(
    adata, marker_genes, groupby='cell_type', cmap='RdBu_r',
    standard_scale='var', show=False,
)
plt.savefig('dotplot_LTB.pdf', dpi=300, bbox_inches='tight')

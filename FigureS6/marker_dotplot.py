import scanpy as sc
import anndata as ad
import pandas as pd
import matplotlib.pyplot as plt

mean_df = pd.read_csv("dotplot_celltype_mean_expression.csv", index_col=0)
frac_df = pd.read_csv("dotplot_celltype_fraction.csv", index_col=0)

marks_gene = {
    'Lineage_A_Subtype_1': ["CCR7", "IL7R", "TCF7"],
    'Lineage_A_Subtype_2': ["GZMK", "EOMES", "CST7"],
    'Lineage_A_Subtype_4': ["CXCL13", "HAVCR2", "CTLA4"],
    'Lineage_A_Subtype_3': ["GZMH", "ZNF683", "NKG7"],
}

adata_dummy = ad.AnnData(pd.DataFrame(0, index=mean_df.index, columns=mean_df.columns))
adata_dummy.obs['cell_type'] = mean_df.index.values
adata_dummy.obs.index = adata_dummy.obs.index.astype(str)
adata_dummy.obs.index.name = None

dp = sc.pl.DotPlot(
    adata_dummy, marks_gene, groupby='cell_type',
    dot_color_df=mean_df, dot_size_df=frac_df,
    cmap='RdBu_r', standard_scale='var',
    categories_order=list(marks_gene.keys()),
)
dp.savefig('dotplot_celltype.pdf', dpi=300, bbox_inches='tight')

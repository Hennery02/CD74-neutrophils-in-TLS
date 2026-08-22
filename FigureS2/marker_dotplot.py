import scanpy as sc
import anndata as ad
import pandas as pd
import matplotlib.pyplot as plt

mean_df = pd.read_csv("dotplot_celltype_mean_expression.csv", index_col=0)
frac_df = pd.read_csv("dotplot_celltype_fraction.csv", index_col=0)

marks_gene = {
    'MajorType_2': ["CD79A", "MS4A1", "BANK1"],
    'MajorType_10': ["KRT6A", "KRT14", "KRT17"],
    'MajorType_7': ["VWF", "PECAM1", "PLVAP"],
    'MajorType_8': ["DCN", "COL1A1", "COL3A1"],
    'MajorType_6': ["TPSB2", "TPSAB1", "CPA3"],
    'MajorType_4': ["CD14", "LYZ", "CD163"],
    'MajorType_5': ["S100A8", "CXCL8", "FCGR3B"],
    'MajorType_9': ["SOD3", "ACTA2", "RGS5"],
    'MajorType_3': ["MZB1", "IGKC", "IGHG1"],
    'MajorType_1': ["CD3D", "CCL5", "GZMA"]
}

adata_dummy = ad.AnnData(pd.DataFrame(0, index=mean_df.index, columns=mean_df.columns))
adata_dummy.obs['cell_type'] = mean_df.index

dp = sc.pl.DotPlot(
    adata_dummy, marks_gene, groupby='cell_type',
    dot_color_df=mean_df, dot_size_df=frac_df,
    cmap='RdBu_r', standard_scale='var',
)
dp.savefig('dotplot_celltype.pdf', dpi=300, bbox_inches='tight')

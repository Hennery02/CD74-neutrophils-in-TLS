import scanpy as sc
import anndata as ad
import pandas as pd
import matplotlib.pyplot as plt

mean_df = pd.read_csv("dotplot_celltype_mean_expression.csv", index_col=0)
frac_df = pd.read_csv("dotplot_celltype_fraction.csv", index_col=0)

marks_gene = {
    'TNKSubtype_1': ["ISG15", "MX1", "IFIT3"],
    'TNKSubtype_2': ["SELL", "LEF1", "CCR7"],
    'TNKSubtype_3': ["CXCL13", "KLRB1", "NR3C1"],
    'TNKSubtype_4': ["CXCL13", "PDCD1", "KLRB1"],
    'TNKSubtype_5': ["CCR7", "SELL", "TCF7"],
    'TNKSubtype_6': ["IL7R", "CCR7", "ANXA1"],
    'TNKSubtype_7': ["FOS", "CD69", "JUNB"],
    'TNKSubtype_8': ["FOXP3", "IL32", "BATF"],
    'TNKSubtype_9': ["FOXP3", "TNFRSF18", "IL2RA"],
    'TNKSubtype_10': ["TNFRSF4", "TNFRSF18", "CCR8"],
    'TNKSubtype_11': ["ISG15", "MX1", "FOXP3"],
    'TNKSubtype_12': ["ISG15", "IFIT3", "LAG3"],
    'TNKSubtype_13': ["GZMB", "GZMH", "ZNF683"],
    'TNKSubtype_14': ["GZMK", "EOMES", "CRTAM"],
    'TNKSubtype_15': ["CXCL13", "PDCD1", "HAVCR2"],
    'TNKSubtype_16': ["GZMK", "CXCR4", "CD69"],
    'TNKSubtype_17': ["MKI67", "TOP2A", "STMN1"],
    'TNKSubtype_18': ["MKI67", "GZMB", "STMN1"],
    'TNKSubtype_19': ["MKI67", "GNLY", "KLRC1"],
    'TNKSubtype_20': ["AREG", "KLRF1", "TYROBP"],
    'TNKSubtype_21': ["XCL1", "XCL2", "ZNF683"],
    'TNKSubtype_22': ["FGFBP2", "S1PR5", "FCGR3A"],
    'TNKSubtype_23': ["FCGR3A", "KLRF1", "FGFBP2"],
    'TNKSubtype_24': ["XCL1", "KIR2DL4", "SH2D1B"],
    'TNKSubtype_25': ["KRT81", "KRT86", "ADGRG3"],
    'TNKSubtype_26': ["KIR2DL3", "KIR3DL2", "TRGC2"],
}

adata_dummy = ad.AnnData(pd.DataFrame(0, index=mean_df.index, columns=mean_df.columns))
adata_dummy.obs['cluster_1_named'] = mean_df.index.values
adata_dummy.obs.index = adata_dummy.obs.index.astype(str)
adata_dummy.obs.index.name = None

dp = sc.pl.DotPlot(
    adata_dummy, marks_gene, groupby='cluster_1_named',
    dot_color_df=mean_df, dot_size_df=frac_df,
    cmap='RdBu_r', standard_scale='var',
    categories_order=list(marks_gene.keys()),
)
dp.savefig('dotplot_celltype.pdf', dpi=300, bbox_inches='tight')

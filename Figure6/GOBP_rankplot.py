import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import Normalize

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

df_geneset_all = pd.read_csv('panelF_GOBP_rankplot_plot_data.csv')


def plot_enrichment_rank(df_all, group_name, groupby_col='group', n_label=6, padj_cap=300,
                          figsize=(4, 6), label_formatter=None, highlight_terms=None,
                          direction='up', cmap='Reds', ascending_rank=False):
    sub = df_all[df_all[groupby_col] == group_name].copy()
    if direction == 'up':
        sub = sub[sub['stat'] > 0].sort_values('stat', ascending=False).reset_index(drop=True)
    else:
        sub = sub[sub['stat'] < 0].sort_values('stat', ascending=True).reset_index(drop=True)
    sub['rank'] = np.arange(1, len(sub) + 1)
    sub['neglogpadj'] = -np.log10(sub['padj'].clip(lower=10 ** (-padj_cap)))
    if ascending_rank:
        sub['plot_rank'] = len(sub) + 1 - sub['rank']
    else:
        sub['plot_rank'] = sub['rank']

    fig, ax = plt.subplots(figsize=figsize)
    vmax = sub['neglogpadj'].max()
    norm = Normalize(vmin=0, vmax=vmax)
    sc_plot = ax.scatter(
        sub['plot_rank'], sub['neglogpadj'],
        c=sub['neglogpadj'], cmap=cmap, norm=norm,
        s=8, linewidths=0,
    )
    ax.set_xlabel('Rank')
    ax.set_ylabel(r'-log$_{10}$($P$.adj)')

    def _label(name):
        if label_formatter is not None:
            return label_formatter(name)
        return name.replace('GOBP_', '').replace('_', ' ').title()

    if highlight_terms is not None:
        top = sub[sub['name'].isin(highlight_terms)].sort_values('rank').head(n_label)
    else:
        top = sub.head(n_label)

    y_top = sub['neglogpadj'].max()
    y_bottom = sub['neglogpadj'].min()
    y_span = max(y_top - y_bottom, 1.0)
    x_max = sub['plot_rank'].max()
    x_text = x_max * (0.72 if ascending_rank else 0.28)
    ha = 'right' if ascending_rank else 'left'
    for i, (_, row) in enumerate(top.iterrows()):
        y_text = y_top - i * (y_span * 0.09)
        ax.annotate(
            _label(row['name']),
            xy=(row['plot_rank'], row['neglogpadj']),
            xytext=(x_text, y_text),
            fontsize=6, va='center', ha=ha,
            arrowprops=dict(arrowstyle='-', color='black', lw=0.5, shrinkA=0, shrinkB=2),
        )

    cbar = fig.colorbar(sc_plot, ax=ax, shrink=0.5)
    cbar.set_label(r'-log$_{10}$($P$.adj)')
    fig.tight_layout()
    return fig


tls_terms = [
    'GOBP_LYMPHOCYTE_ACTIVATION',
    'GOBP_B_CELL_MEDIATED_IMMUNITY',
    'GOBP_T_CELL_ACTIVATION',
    'GOBP_LEUKOCYTE_MIGRATION',
    'GOBP_ANTIGEN_PROCESSING_AND_PRESENTATION',
    'GOBP_B_CELL_ACTIVATION',
]

fig = plot_enrichment_rank(
    df_geneset_all, 'TLS_vs_nonTLS',
    figsize=(4, 6),
    highlight_terms=tls_terms,
)
fig.savefig('rankplot_up.pdf', bbox_inches='tight')

fig_dn = plot_enrichment_rank(
    df_geneset_all, 'TLS_vs_nonTLS',
    figsize=(4, 6),
    direction='down', cmap='Blues',
    ascending_rank=True,
)
fig_dn.axes[0].invert_yaxis()
fig_dn.savefig('rankplot_down.pdf', bbox_inches='tight')

print('Done.')

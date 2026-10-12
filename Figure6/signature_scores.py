import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

MICRONS_PER_PIXEL = 0.5028673941838965
SCALEBAR_LENGTH_UM = 1000
SCALEBAR_LOC = 'lower right'
SCALEBAR_COLOR = 'black'
SCALEBAR_FONTSIZE = 10


def add_scalebar(ax, length_um=SCALEBAR_LENGTH_UM, loc=SCALEBAR_LOC,
                  color=SCALEBAR_COLOR, fontsize=SCALEBAR_FONTSIZE,
                  microns_per_pixel=MICRONS_PER_PIXEL):
    length_px = length_um / microns_per_pixel
    xlim = ax.get_xlim(); ylim = ax.get_ylim()
    pad_x = abs(xlim[1] - xlim[0]) * 0.04
    pad_y = abs(ylim[1] - ylim[0]) * 0.04

    if 'right' in loc:
        x1 = max(xlim) - pad_x
        x0 = x1 - length_px
    else:
        x0 = min(xlim) + pad_x
        x1 = x0 + length_px
    if 'lower' in loc:
        y0 = max(ylim) - pad_y
    else:
        y0 = min(ylim) + pad_y

    ax.plot([x0, x1], [y0, y0], color=color, linewidth=3, solid_capstyle='butt')
    label = f'{length_um} um' if length_um < 1000 else f'{length_um/1000:.1f} mm'
    ax.text((x0 + x1) / 2, y0, label, color=color, fontsize=fontsize,
            ha='center', va='bottom' if 'lower' in loc else 'top')


def plot_score_spatial(x, y, vals, score_col, vmin, vmax, cmap, outpath, point_size=2):
    order = np.argsort(vals)
    fig, ax = plt.subplots(figsize=(9, 9))
    sca = ax.scatter(x[order], y[order], c=vals[order], s=point_size, cmap=cmap, vmin=vmin, vmax=vmax, rasterized=True)
    plt.colorbar(sca, ax=ax, label=score_col, shrink=0.75)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect('equal')
    ax.invert_yaxis()
    add_scalebar(ax)
    plt.tight_layout()
    plt.savefig(outpath + '.pdf', bbox_inches='tight')
    plt.close(fig)


df = pd.read_csv('panelD_signature_scores_plot_data.csv')
x = df['x'].values
y = df['y'].values

VMIN_tls = 0.06
VMAX_tls = np.percentile(df['TLS_marker22_score'], 99.2)
plot_score_spatial(x, y, df['TLS_marker22_score'].values, 'TLS_marker22_score',
                    VMIN_tls, VMAX_tls, 'viridis', 'TLS_marker22_score')

VMIN_d = 0.2
VMAX_d = np.percentile(df['CellType_D_clean_score'], 99.5)
plot_score_spatial(x, y, df['CellType_D_clean_score'].values, 'CellType_D_clean_score',
                    VMIN_d, VMAX_d, 'viridis', 'CellType_D_clean_score')

VMIN_a = np.percentile(df['CellType_A_score'], 0)
VMAX_a = np.percentile(df['CellType_A_score'], 99.2)
plot_score_spatial(x, y, df['CellType_A_score'].values, 'CellType_A_score',
                    VMIN_a, VMAX_a, 'viridis', 'CellType_A_score')

VMIN_b = np.percentile(df['CellType_B_score'], 80)
VMAX_b = np.percentile(df['CellType_B_score'], 98)
plot_score_spatial(x, y, df['CellType_B_score'].values, 'CellType_B_score',
                    VMIN_b, VMAX_b, 'viridis', 'CellType_B_score')

print('Done.')

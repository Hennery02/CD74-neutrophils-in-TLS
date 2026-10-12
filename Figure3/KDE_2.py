import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

CURVE_CSV = 'KDE_2_curve.csv'
SUMMARY_CSV = 'KDE_2_summary.csv'
STATS_CSV = 'KDE_2_stats.csv'
OUT_PDF = 'KDE_2.pdf'

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

GROUP_COLORS = {'nTLS': '#cecdcd', 'imTLS': '#edd2ad', 'mTLS': '#e6a499'}
LINE_COLORS = {'nTLS': '#999898', 'imTLS': '#c89a60', 'mTLS': '#c05a48'}
WINDOW_RADIUS = 300
ORDER = ['nTLS', 'imTLS', 'mTLS']


def draw_kde(curve, summary, stats_df, out):
    fig, ax = plt.subplots(figsize=(5, 5))
    handles = []
    for grp in ORDER:
        c = curve[curve['TLS_group'] == grp]
        if len(c) == 0:
            continue
        s = summary[summary['TLS_group'] == grp].iloc[0]
        ax.fill_between(c['x'], c['y'], alpha=0.40, color=GROUP_COLORS[grp])
        line, = ax.plot(c['x'], c['y'], color=LINE_COLORS[grp], linewidth=2.0)
        ax.axvline(s['median_um'], color=LINE_COLORS[grp], linestyle='--', linewidth=1.3)
        handles.append((line, f"{grp}  Median: {s['median_um']:.1f} \u00b5m  (n={int(s['n_cores'])})"))
    ax.legend([h for h, _ in handles], [l for _, l in handles], fontsize=8, frameon=False,
              loc='upper left', handlelength=1.2, labelspacing=0.4)
    lines = []
    kw = stats_df[stats_df['test'] == 'KW'].iloc[0]['p']
    lines.append('KW $P$ < 0.001' if kw < 0.001 else f'KW $P$ = {kw:.3f}')
    for _, r in stats_df[stats_df['test'] == 'Dunn_Holm'].iterrows():
        p1 = r['p']
        lines.append(f"{r['group1']} vs {r['group2']}: " + ('$P$ < 0.001' if p1 < 0.001 else f'$P$ = {p1:.3f}'))
    ax.text(0.97, 0.05, '\n'.join(lines), transform=ax.transAxes, ha='right', va='bottom', fontsize=8,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.85, edgecolor='#cccccc', linewidth=0.8))
    ax.set_xlim(0, WINDOW_RADIUS)
    ax.set_ylim(bottom=0)
    ax.set_xlabel('Distance (\u00b5m)', fontsize=10)
    ax.set_ylabel('Frequency per million total cells', fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    fig.savefig(out, bbox_inches='tight')

curve = pd.read_csv(CURVE_CSV)
summary = pd.read_csv(SUMMARY_CSV)
stats_df = pd.read_csv(STATS_CSV).fillna('')
draw_kde(curve, summary, stats_df, OUT_PDF)

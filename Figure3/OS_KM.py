import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

pat = pd.read_csv('OS_KM_plot_data.csv')

hi = pat[pat['group'] == 'CellType_D present']
lo = pat[pat['group'] == 'CellType_D absent']

results = logrank_test(hi['time'], lo['time'],
                       event_observed_A=hi['event'],
                       event_observed_B=lo['event'])
p = results.p_value

fig, ax = plt.subplots(figsize=(5.5, 5))
COLOR_HI = '#c05a48'
COLOR_LO = '#888787'

legend_handles = []
for grp, color, label in [
    ('CellType_D present', COLOR_HI, f'CellType_D present (n={len(hi)})'),
    ('CellType_D absent', COLOR_LO, f'CellType_D absent  (n={len(lo)})'),
]:
    sub = pat[pat['group'] == grp]
    kmf = KaplanMeierFitter()
    kmf.fit(sub['time'], sub['event'], label=label)
    kmf.plot_survival_function(ax=ax, ci_show=True, color=color,
                                linewidth=2, ci_alpha=0.15, legend=False)
    legend_handles.append(Line2D([0], [0], color=color, linewidth=2, label=label))

if p < 0.0001:
    pstr = 'Log-rank $P < 0.0001$'
elif p < 0.001:
    pstr = 'Log-rank $P < 0.001$'
elif p < 0.05:
    exp = int(np.floor(np.log10(p)))
    coef = p / 10**exp
    pstr = f'Log-rank $P = {coef:.2f} \\times 10^{{{exp}}}$'
else:
    pstr = f'Log-rank $P = {p:.3f}$'

ax.text(0.97, 0.97, pstr, transform=ax.transAxes,
        ha='right', va='top', fontsize=10,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                  edgecolor='#cccccc', alpha=0.9))

ax.set_xlabel('Time (months)', fontsize=11)
ax.set_ylabel('Overall survival probability', fontsize=11)
ax.set_ylim(0, 1.05)
ax.set_xlim(0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(handles=legend_handles, fontsize=9, frameon=False, loc='lower left')

plt.tight_layout()
plt.savefig('OS_KM.pdf', bbox_inches='tight')

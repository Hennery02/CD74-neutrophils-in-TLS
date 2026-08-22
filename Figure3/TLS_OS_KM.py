import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from lifelines import KaplanMeierFitter
from lifelines.statistics import multivariate_logrank_test

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

GROUP_ORDER = ['nTLS', 'imTLS', 'mTLS']
COLORS = {'nTLS': '#888787', 'imTLS': '#c89a60', 'mTLS': '#c05a48'}

pat = pd.read_csv('TLS_OS_KM_plot_data.csv')

overall = multivariate_logrank_test(pat['time'], pat['TLS_group'], pat['event'])
p_overall = overall.p_value

fig, ax = plt.subplots(figsize=(5.5, 5))

handles = []
for grp in GROUP_ORDER:
    sub = pat[pat['TLS_group'] == grp]
    kmf = KaplanMeierFitter()
    kmf.fit(sub['time'], sub['event'])
    kmf.plot_survival_function(ax=ax, ci_show=True,
                               color=COLORS[grp], linewidth=2,
                               ci_alpha=0.15, legend=False)
    handles.append(Line2D([0], [0], color=COLORS[grp], linewidth=2,
                          label=f'{grp} (n={len(sub)})'))

pstr = 'Log-rank $P < 0.001$' if p_overall < 0.001 else f'Log-rank $P = {p_overall:.3f}$'

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
ax.legend(handles=handles, fontsize=9, frameon=False, loc='lower left')

plt.tight_layout()
plt.savefig('TLS_OS_KM.pdf', bbox_inches='tight')

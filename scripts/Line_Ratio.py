import pyneb as pn
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

den = np.logspace(0, 6, 50)
tem = 10e3

s2 = pn.Atom('S', 2)
e6731 = s2.getEmissivity(den=den, tem=tem, wave=6731)
e6716 = s2.getEmissivity(den=den, tem=tem, wave=6716)


colors = ['dodgerblue', 'orange', 'black']
lines  = ['-.', '--', '-']
lw = 1.75

plt.rc('font', family='serif')
plt.rc('text', usetex=True)
fig, ax = plt.subplots(1, 1, figsize=(6.5,6))
ax.plot(den, e6716/1e-20, label=r'$\epsilon_{\lambda 6716}$', color=colors[0], ls=lines[0], lw=lw)
ax.plot(den, e6731/1e-20, label=r'$\epsilon_{\lambda 6731}$', color=colors[1], ls=lines[1], lw=lw)
leg = ax.legend(loc='best', fontsize=17, frameon=False)
for legobj in leg.legendHandles:
    legobj.set_linewidth(2.3)
ax.set_ylabel(r'$\epsilon_{\lambda} \; \left(10^{-20} \, \mathrm{erg} \, \mathrm{cm}^{3} \, \mathrm{s}^{-1}\right)$', fontsize=25)
ax.set_xlabel(r'$n_{e} \; \left(\rm cm^{-3}\right)$', fontsize=25)
ax.set_xscale('log')
ax.set_xlim(1e0, 1e6)
ax.set_ylim(-1.5, 3.5)
ax.set_yticks([0, 1, 2, 3])
ax.tick_params(axis='both', which='major', size=0, labelsize=15, pad=7)

ax2 = ax.twinx()
ax2.plot(den, e6716 / e6731, color=colors[2], ls=lines[2])
ax2.set_ylim(0.25, 2.75)
ax2.set_yticks([ 0.5, 1, 1.5])
ax2.set_ylabel(r'$\epsilon_{\lambda 6716} \, / \, \epsilon_{\lambda 6731}$', rotation=270, fontsize=25, labelpad=30)
ax2.tick_params(axis='both', which='major', size=0, labelsize=15)

fig.tight_layout()
fig.savefig('../paper/figure/misc/line_ratio.pdf', dpi=300)
plt.close(fig)
#fig.show()

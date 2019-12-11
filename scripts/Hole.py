import sys; sys.path.append('..')
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')
plt.rc('font', family='serif')
plt.rc('text', usetex=True)
title = r"$\mathrm{Exponential \, Distribution}$" + "\n" + r"$\bar{n}_{e} \approx 1000 \, \mathrm{cm}^{-3}$"
xlabel = r"$n_{e} \, \rm\left(cm^{-3}\right) \, [EM]$"
ylabel = r"$n_{e} \, \rm\left(cm^{-3}\right) \, [S \, \textsc{ii}]$"



from nebulous.geom import sphere
from nebulous.cel  import cel_den_dict
from nebulous.pdf  import pdfs
from nebulous.em    import getEM, getSkyDenEM
from nebulous.utils import getDepth

dim = (30,)

fig, ax = plt.subplots(figsize=(6.5, 6))
for inrad, c in zip([0., 0.3, 0.6], ['orange', 'dodgerblue', 'forestgreen']):
    loc = sphere(dim=dim, inRad=inrad)
    depth = getDepth(dim=dim, loc=loc) * 1.
    los = depth > 5

    tem = 10e3
    n_e = pdfs['exponential'](dim=dim, loc=loc, mean=1e3)

    s2 = cel_den_dict['SII']
    s2.getEmissivity(tem=tem, n_e=n_e, loc=loc)
    s2.getSkyEmiss()
    s2.getSkyDen()

    em = getEM(n_e=n_e)
    denEM = getSkyDenEM(em, depth)

    #fig, ax = plt.subplots()
    ax.scatter(denEM[los], s2.skyDen[los], color=c, s=20, label=r'$r_{i} / r_{o} = ' + '{:.2f}$'.format(inrad / 0.9), alpha=0.3)

ax.set_title(title, fontsize=22)
ax.set_xlabel(xlabel, fontsize=20)
ax.set_ylabel(ylabel, fontsize=20)
ax.legend(loc='best', frameon=False, fontsize=17)
fig.tight_layout()
fig.show()

import sys; sys.path.append('..')
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')
import numpy as np
from nebulous.geom  import sphere
from nebulous.pdf   import exponential
from nebulous.cel   import SII_den as SII
from nebulous.em    import getEM, getSkyDenEM
from nebulous.utils import getDepth

x = np.linspace(0, 3000)

dim = (30,30,30)
loc = sphere(dim=dim, inRad=0.3, outRad=0.9)
depth = getDepth(dim=dim, loc=loc)
los = depth > 5

tem = 10e3
n_e = exponential(loc=loc, dim=dim, mean=1000)

s2 = SII()
s2.getEmissivity(tem=tem, n_e=n_e, loc=loc)
s2.getSkyEmiss()
s2.getSkyDen()

em = getEM(n_e=n_e)
denEM = getSkyDenEM(em, depth)

title = r"$\mathrm{Exponential \, Distribution}$" + "\n" + r"$\bar{n}_{e} \approx 1000 \, \mathrm{cm}^{-3}$"
xlabel = r"$n_{e} \, \rm\left(cm^{-3}\right) \, [EM]$"
ylabel = r"$n_{e} \, \rm\left(cm^{-3}\right) \, [S \, \textsc{ii}]$"


plt.figure(figsize=(6,6.5))
fontsize=22
plt.rcParams['xtick.labelsize'] = 15
plt.rcParams['ytick.labelsize'] = 15
plt.rcParams['legend.fontsize'] = 15
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.plot(x,x, 'k-')
plt.scatter(denEM[los], s2.skyDen[los], color='dodgerblue', s=20)
plt.ylim(1500, 3e3)
plt.yticks(np.arange(1500, 3001, 250))
plt.xlim(900, 2000)
plt.xticks(np.arange(1000, 2001, 250))
plt.ylabel(ylabel, fontsize=fontsize)
plt.xlabel(xlabel, fontsize=fontsize)
#plt.title(title, fontsize=fontsize)
plt.tight_layout()
plt.savefig('../paper/figure/misc/scat_denExp.pdf', dpi=300)
plt.close()

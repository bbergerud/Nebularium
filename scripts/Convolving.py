import sys; sys.path.append('..')
import matplotlib.pyplot as plt
plt.rc('font', family='serif')
plt.rc('text', usetex=True)

from nebulous.geom import sphere
from nebulous.cel  import cel_den_dict
from nebulous.pdf  import pdfs
from copy import copy

dim = (60,)
loc = sphere(dim=dim)

tem = 10e3
n_e = pdfs['exponential'](dim=dim, loc=loc, mean=1e3)

neb = cel_den_dict['SII']
neb.getEmissivity(n_e=n_e, tem=tem, loc=loc)
neb.getSkyEmiss(convl=False)

img1 = copy(neb.skyEmiss[0])
img1 /= img1.max()

neb.getSkyEmiss(convl=True)
img2 = copy(neb.skyEmiss[0])
img2 /= img2.max()


fig, (ax1, ax2) = plt.subplots(figsize=(6.5, 10), nrows=2)
f1 = ax1.pcolormesh(img1, cmap=plt.cm.jet, linewidth=0)
f2 = ax2.pcolormesh(img2, cmap=plt.cm.jet, linewidth=0)
cbar = [fig.colorbar(f1, ax=ax1), fig.colorbar(f2, ax=ax2)]
for c in cbar:
    c.set_label(
        r'$I_{\lambda 6716} \; / \; I_\mathrm{max}$',
        rotation=270,
        labelpad=30,
        fontsize=20,
    )
    c.ax.tick_params(length=0, width=0, labelsize=15)
    c.outline.set_visible(False)

for ax in [ax1, ax2]:
    ax.tick_params(length=0, width=0, labelsize=15)
fig.tight_layout()
fig.savefig('convolution.pdf', dpi=300)
plt.close(fig)

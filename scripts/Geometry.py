import sys; sys.path.append('../')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
sns.set_style('dark')
plt.rc('font', family='serif')
plt.rc('text', usetex=True)

from nebulous.geom  import sphere
from nebulous.utils import getDepth

dim = (30,)
loc = sphere(dim=dim, inRad=0.3, outRad=0.9)
depth = getDepth(dim=dim, loc=loc) * 1.
depth[depth == 0] = np.nan

fig, ax = plt.subplots(figsize=(6.5,5.5))
cs = ax.pcolormesh(depth, cmap=plt.cm.Blues, linewidth=0)
cbar = fig.colorbar(cs)
cbar.ax.tick_params(length=0, width=0, labelsize=15)
ax.tick_params('both', labelsize=15)
fig.tight_layout()
#fig.show()

fig.savefig('geometry.pdf', dpi=300)
plt.close(fig)

import sys; sys.path.append('..')
import matplotlib.pyplot as plt
import numpy             as np
from nebulous.geom  import sphere
from nebulous.cel   import cel_den_dict, cel_tem_dict
from nebulous.orl   import orl_dict
from nebulous.misc  import den_dict, fix_params, mkdir
from nebulous.pdf   import pdfs
from nebulous.utils import getDepth

# ==================================================
# Set the nebula parameters
# ==================================================
dim   = (30,)
loc   = sphere(dim=dim, inRad=0.0, outRad=0.9)
los   = getDepth(loc=loc, dim=dim) > 5
convl = False
kernel = 2
den_mean = 1000
tem_mean = 10e3
p   = {'sigma': 0.8}
pdf = 'lognormal'
cel_tem = None
cel_den = 'OIII'
orl     = 'OII'

# ==================================================
# ==================================================
n_e = pdfs[pdf](dim=dim, loc=loc, mean=den_mean, **p)
tem = tem_mean



# ==================================================
# Grab the appropriate ion diagnostics
# ==================================================
cel_tem = cel_tem_dict[cel_tem] if cel_tem else None
cel_den = cel_den_dict[cel_den]
orl = orl_dict[orl]
h1  = orl_dict['HI']

# ==============================================
# Generate the H-beta intensities
# ==============================================
h1.getEmissivity(tem=tem, n_e=n_e)
h1.getSkyEmiss(convl=convl, kernel=kernel)

# ==============================================
# Generate the CEL emission to get the density
# estimate.
# ==============================================
cel_den.getEmissivity(tem=tem, n_e=n_e, loc=loc)
cel_den.getSkyEmiss(convl=convl, kernel=kernel)
cel_den.getSkyDen(skyTem=tem)

# ==============================================
# Get the abundance estimate; if a temperature
# sensitive line set is passed, then use this
# set to get the ion abundance estimate
# ==============================================
if cel_tem:
    cel_tem.getEmissivity(tem=tem, n_e=n_e, loc=loc)
    cel_tem.getSkyEmiss(convl=convl, kernel=kernel)
    cel_tem.getIonAbundance(skyTem=tem, skyDen=cel_den.skyDen, Hbeta=h1.skyBeta, los=los)
    cel_abd = cel_tem.ionAbundance[0][los]
else:
    cel_den.getIonAbundance(skyTem=tem, skyDen=cel_den.skyDen, Hbeta=h1.skyBeta, los=los)
    cel_abd = cel_den.ionAbundance[0][los]

# ==============================================
# Generate the ORL emission and estimate the
# abundance
# ==============================================
orl.getEmissivity(tem=tem, n_e=n_e)
orl.getSkyEmiss(convl=convl, kernel=kernel)
orl.getIonAbundance(skyTem=tem, skyDen=cel_den.skyDen, Hbeta=h1.skyBeta, los=los)
adf = orl.ionAbundance[0][los] / cel_abd

adfSkyMap = np.zeros_like(h1.skyBeta)
adfSkyMap[los] = adf



fig, (ax1, ax2) = plt.subplots(ncols=2)
f1 = ax1.imshow(adfSkyMap)
f2 = ax2.imshow(cel_den.skyDen)
cbar = [fig.colorbar(f1, ax=ax1), fig.colorbar(f2, ax=ax2)]

#cbar = fig.colorbar(cs)
fig.show()

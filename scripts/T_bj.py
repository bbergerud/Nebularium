import sys, os; sys.path.append('..')
import numpy  as np
import pandas as pd

from nebulous.geom  import sphere
from nebulous.cel   import cel_tem_dict
from nebulous.orl   import orl_dict
from nebulous.pdf   import pdfs
from nebulous.misc  import fix_params, mkdir
from nebulous.utils import getDepth

# ==================================================
# Set the nebula parameters
# ==================================================
dim   = (30,30,30)
loc   = sphere(dim=dim, inRad=0.3, outRad=0.9)
los   = getDepth(loc=loc, dim=dim) > 5
convl = True
pdf   = 'normal'
n_e   = 1e3
kernel = 1

x = 7500
p = fix_params(params={'sigma': 0.2}, pdf=pdf, x=x)
tem = pdfs[pdf](dim=dim, loc=loc, mean=x, **p)

ion_tem = orl_dict['BJ']
ion_tem.getEmissivity(tem=tem, n_e=n_e, loc=loc)
ion_tem.getSkyEmiss(convl=convl, kernel=kernel)
ion_tem.getSkyTem(skyDen=n_e)

fig, ax = plt.subplots()
ax.imshow(ion_tem.skyTem - x)
fig.show()

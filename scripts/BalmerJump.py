import sys, os; sys.path.append('..')
import pyneb as pn
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_style('darkgrid')

from nebulous.orl import orl_dict

#n_e = 1e3
#tem = np.linspace(5e3, 15e3, 25)
tem = 10e3
n_e = np.logspace(-2, 6, 100)

H = orl_dict['HI'].atom
H11 = H.getEmissivity(den=n_e, tem=tem, product=True, label="11_2")
#BJ   = tem**(-3/2)

H11 /= H11.max()
#BJ  /= BJ.max()

#DrainApprox = tem**(-0.7)
#DrainApprox /= DrainApprox.max()

fig, ax = plt.subplots()
ax.plot(n_e, H11, label='H11')
#ax.plot(tem, BJ, label='BJ')
#ax.plot(tem, BJ/H11, label='BJ/H11')
#ax.plot(tem, DrainApprox, label='Approx (Drain, 2010)')
ax.legend(loc='best')
ax.set_ylabel('Emissivity')
ax.set_xlabel('Density')
ax.set_xscale('log')
fig.show()

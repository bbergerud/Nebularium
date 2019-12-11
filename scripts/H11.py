import sys, os; sys.path.append('..')
import pyneb as pn
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_style('darkgrid')

from nebulous.orl import orl_dict

tem = [10e3, np.linspace(5e3, 15e3, 100)]
den = [np.logspace(1, 5, 100), 1000]

H = orl_dict['HI'].atom

H11 = []
for i, (t, d) in enumerate(zip(tem, den)):
    j = H.getEmissivity(den=d, tem=t, product=True, label="11_2")
    H11.append(j)

fig, ax = plt.subplots(ncols=2, figsize=(18,9))
ax[0].plot(den[0], H11[0])
ax[0].set_xscale('log')
ax[0].set_xlabel('$n_{e} \; (\mathrm{cm}^{-3})$', fontsize=20)
ax[0].set_ylabel('$\epsilon_{\lambda} \; (\mathrm{erg} \, \mathrm{cm}^{3} \, \mathrm{s}^{-1})$', fontsize=20)
ax[0].set_title('$T = 10^{4} \; \mathrm{K}$', fontsize=20)
ax[1].plot(tem[1], H11[1])
ax[1].set_xlabel('$T \; (\mathrm{K})$', fontsize=20)
ax[1].set_ylabel('$\epsilon_{\lambda} \; (\mathrm{erg} \, \mathrm{cm}^{3} \, \mathrm{s}^{-1})$', fontsize=20)
ax[1].set_title('$n_{e} = 1000 \; \mathrm{cm}^{-3}$', fontsize=20)
fig.show()





from scipy.interpolate import interp1d

tems = np.logspace(np.log10(500), np.log10(30e3), 100)
j_H  = H.getEmissivity(tem=tems, den=1e3, label='11_2')
j_BJ = tems**(-1.5)
ratio = j_BJ / j_H

fig, ax = plt.subplots(figsize=(9,9))
ax.plot(tems, ratio)
ax.set_xlabel('$T \; (\mathrm{K})$', fontsize=20)
ax.set_ylabel('$j_\mathrm{BJ} / j_\mathrm{H11}$', fontsize=20)
ax.set_title('$n_{e} = 1000 \; \mathrm{cm}^{-3}$', fontsize=20)
fig.show()



# ===================================================
# Perform an interpolation of the ratio and temperature
# to create a function that will compute the temperature
# given a ratio.
# ===================================================
tem_func = interp1d(ratio, tems)




"""
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
"""

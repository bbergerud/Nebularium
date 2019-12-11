import sys, os; sys.path.append('..')
import pyneb as pn
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_style('darkgrid')

from nebulous.cel import cel_tem_dict

n_e = 1e3
tem = np.linspace(5e3, 15e3, 25)

ions = {}
waves = {}
for ion in ['NII', 'OIII', 'NeIII', 'SIII']:
    ions[ion] = cel_tem_dict[ion].atom
    waves[ion] = cel_tem_dict[ion].wave

emiss = {}
for ion in ions.keys():
    for wave in waves[ion]:
        emiss[(ion,wave)] = ions[ion].getEmissivity(den=n_e, tem=tem, wave=wave, product=True)


fig, ax = plt.subplots()
for ion in ions.keys():
    ratio = np.sum([emiss[ion, waves[ion][i]] for i in range(2)])
    ratio /= emiss[ion, waves[ion][2]]
    ratio /= ratio.max()
    ax.plot(tem, ratio, label=ion)
ax.legend(loc='best')
ax.set_yscale('log')
ax.set_ylabel('Normalized Ratio: (I1 + I2) / I3')
ax.set_xlabel('Temperature (K)')
fig.show()

import sys; sys.path.append('..')
import matplotlib.pyplot as plt
import numpy as np

from nebulous.cel import cel_den_dict

den = np.logspace(-2, 8, 1000)
tem = 10e3


ion = cel_den_dict['OIII']

j1 = ion.atom.getEmissivity(den=den, tem=tem, wave=ion.wave[0])
j2 = ion.atom.getEmissivity(den=den, tem=tem, wave=ion.wave[1])
lineRatio = j1 / j2

turnover = 0.5 * (max(lineRatio) + min(lineRatio))
difference = abs(lineRatio - turnover)
print(den[difference == min(difference)])


fig, ax = plt.subplots(figsize=(6,6))
ax.plot(den, lineRatio)
ax.set_xscale('log')
fig.show()

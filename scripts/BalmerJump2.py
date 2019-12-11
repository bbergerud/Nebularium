import pyneb as pn
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.stats import lognorm, norm

H1 = pn.RecAtom('H', 1)
μ = 1000

def bjtem(lineratio, kind='slinear'):
    tem = np.linspace(500, 30e3, 1000)
    j11 = H1.getEmissivity(den=μ, tem=tem, label='11_2', method='linear')
    jbj = tem**(-1.5)
    lr  = jbj / j11
    f = interp1d(lr, tem, kind=kind, fill_value="extrapolate")
    return f(lineratio)

"""
T = np.linspace(5e3, 15e3, 100)
T_bj = []
LR   = []
for t in T:
    tems = np.random.normal(loc=t, scale=0.2, size=50)
    jbj  = tems**(-1.5)
    j11 = H1.getEmissivity(den=μ, tem=tems, label='11_2')
    lr = jbj.sum() / j11.sum()
    tbj = bjtem(lr)

    T_bj.append(tbj)
    LR.append(lr)
T_bj = np.asarray(T_bj)
LR   = np.asarray(LR)

fig, ax = plt.subplots(ncols=2)
ax[0].plot(T, T_bj - T)
ax[1].plot(LR, T)
ax[1].plot(LR, T_bj)
fig.show()

"""
"""
T = np.linspace(5e3, 35e3, 100)
for kind in ['slinear', 'quadratic', 'cubic']:
    T_bj = []
    for t in T:
        j11 = H1.getEmissivity(den=μ, tem=t, label='11_2')
        jbj = t**(-1.5)
        tem_est = bjtem(jbj / j11, kind=kind)
        T_bj.append(tem_est)

    fig, ax = plt.subplots()
    ax.plot(T, T - T_bj)
    fig.show()
"""

T = np.linspace(4e3, 15e3, 200)
for kind in ['slinear', 'quadratic', 'cubic']:
    j11 = H1.getEmissivity(den=μ, tem=T, label='11_2', method='linear')
    jbj = T**(-1.5)
    lr  = jbj / j11
    T_bj = bjtem(lr, kind=kind)

    """
    fig, ax = plt.subplots()
    ax.plot(lr, T_bj)
    ax.plot(lr, T)
    fig.show()
    """
    fig, ax = plt.subplots()
    ax.plot(T, T_bj - T)
    fig.show()

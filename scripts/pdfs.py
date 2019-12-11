from scipy.stats import expon, lognorm, powerlognorm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rc('font', family='serif')
plt.rc('text', usetex=True)
sns.set_style('darkgrid')

def scale_lognorm(μ, σ):
    return μ * np.exp(-0.5 * σ**2)

den = np.logspace(1, 4, 1000)
den = np.geomspace(1e-2, 1e4, 10000)
zeros = np.zeros_like(den)
tem = 10e3
μ = 1000

fig, ax = plt.subplots(figsize=(6.5,5))
for σ in [0.3, 0.8]:
    p = lognorm.pdf(den, σ, scale=scale_lognorm(μ, σ))
    ax.fill_between(den, p, alpha=0.3, label=r"$\sigma = %0.1f$" % σ)

ax.set_xlabel(r"$x$", fontsize=25)
ax.set_ylabel(r"$p(x | \bar{x} = 1000)$", fontsize=25)
ax.set_xlim(0, 3000)
ax.set_ylim(bottom=0, top=1.6e-3)
ax.set_yticks(np.linspace(0, 1.6e-3, 5))
ax.tick_params(axis='both', which='both', labelsize=15)
ax.legend(loc='best', frameon=False, fontsize=17, borderaxespad=None)
fig.tight_layout()
#fig.show()
fig.savefig('pdf_lognormal.pdf')
plt.close(fig)


x = np.geomspace(1e-2, 10000, 10000)
fig, ax = plt.subplots(figsize=(6.5,5))
for s in [0.3]:
    for c in [0.5, 0.1]:
        label  = '$\sigma = {:.1f}, c = {:0.1f}$'.format(s, c)
        p      = powerlognorm.pdf(x=x, c=c, s=s)
        x_mean = np.sum(x * p) / np.sum(p)
        ratio  = 1000 / x_mean
        xval   = x * ratio
        ax.fill_between(xval, p / ratio, alpha=0.3, label=label)
        #ax.plot(xval, p/ratio, ls=line.pop(0), lw=3)#, label=label)

        if False:
            p_avg = 0.5 * (p[1:] + p[:-1]) / ratio
            Δxval  = xval[1:] - xval[:-1]
            print(np.sum(p_avg * Δxval))

ax.set_xlim(0, 5000)
ax.set_ylim(bottom=0, top=1.2e-3)
ax.set_yticks(np.linspace(0, 1.2e-3, 5))
ax.set_xlabel(r"$x$", fontsize=25)
ax.set_ylabel(r"$p(x | \bar{x} = 1000)$", fontsize=25)
ax.tick_params(axis='both', which='both', labelsize=15)
ax.legend(loc='best', frameon=False, fontsize=17, borderaxespad=None)
fig.tight_layout()
#fig.show()
fig.savefig('pdf_pareto.pdf')
plt.close(fig)

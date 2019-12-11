from adf_base  import *
from itertools import product
import sys

def base_script(**args):

    # =======================================================
    # Generate the data for the density-dependent lines
    # =======================================================
    simul(cel_den='OIII', cel_tem=None, orl='OII', **args)
    simul(cel_den='OII' , cel_tem=None, orl='OII', **args)

    # =======================================================
    # Generate the data for the temperature-dependent lines
    # =======================================================
    simul(cel_den='OII', cel_tem='OIII', orl='OII', **args)


def exponential(**args):
    base_script(params=None, pdf='exponential', **args)

def lognormal(sigmas=[0.3, 0.5, 0.8, 1.2], **args):
    for sigma in sigmas:
        params = {'sigma': sigma}
        base_script(params=params, pdf='lognormal', **args)

def mlp(sigmas=[0.3, 0.8], alphas=[1.5, 2.5, 4.0], **args):
    combos = list(product(sigmas, alphas))
    for sigma, alpha in combos:
        params = {'sigma': sigma, 'alpha': alpha}
        base_script(params=params, pdf='mlp', **args)

def pareto(sigmas=[0.3, 0.8], cvals=[0.1, 0.5], **args):
    combos = list(product(sigmas, cvals))
    for sigma, c in combos:
        params = {'sigma': sigma, 'c': c}
        base_script(params=params, pdf='pareto', **args)

funcs = {
    'exponential': exponential,
    'lognormal'  : lognormal,
    'mlp'        : mlp,
    'pareto'     : pareto
}

if __name__ == '__main__':
    types = sys.argv[1:]
    for pdf in types:
        print('PDF = {:s}'.format(pdf))
        funcs[pdf]()

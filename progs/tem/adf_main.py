from adf_base import *
import sys

def base_script(**args):
    # =======================================================
    # Generate the data for the density-dependent lines
    # =======================================================
    simul(cel_den='OIII', cel_tem='OIII', orl='OII', **args)

    # =======================================================
    # Generate the data for the temperature-dependent lines
    # =======================================================
    simul(cel_den=None, cel_tem='OIII', orl='OII', **args)

def lognormal(sigmas=[0.1, 0.2, 0.3], **args):
    for sigma in sigmas:
        params = {'sigma': sigma}
        base_script(params=params, pdf='lognormal', **args)

def normal(sigmas=[0.1, 0.2, 0.3], **args):
    for sigma in sigmas:
        params = {'sigma': sigma}
        base_script(params=params, pdf='normal', **args)

funcs = {
    'lognormal': lognormal,
    'normal'   : normal
}


if __name__ == '__main__':
    types = sys.argv[1:]
    for pdf in types:
        print('PDF = {:s}'.format(pdf))
        funcs[pdf]()

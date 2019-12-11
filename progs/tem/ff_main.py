from ff_base import *
from itertools import product
import sys

def base_script(**args):

    cel_den_tem = [
        ('NI'  , 'NII'),
        ('SII' , 'SIII')
    ]

    cel_dens = list(cel_den_dict.keys())
    for cel_den, cel_tem in cel_den_tem:
        cel_dens.remove(cel_den)

    for ion_den, ion_tem in cel_den_tem:
        simul(cel_den=ion_den, cel_tem=ion_tem, **args)

    for ion_den in cel_dens:
        simul(cel_den=ion_den, cel_tem='OIII', **args)

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

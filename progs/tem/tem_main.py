from tem_base import *
from tqdm import tqdm
import sys

def base_script(**args):
    simul(ion='BJ', grid=200, **args)
    #for diag in cel_tem_dict.keys():
    #    simul(ion=diag, **args)

def lognormal(sigmas=[0.1, 0.2, 0.3]):
    for sigma in sigmas:
        params = {'sigma': sigma}
        base_script(params=params, pdf='lognormal')

def normal(sigmas=[0.1, 0.2, 0.3]):
    for sigma in sigmas:
        params = {'sigma': sigma}
        base_script(params=params, pdf='normal')


funcs = {
    'lognormal': lognormal,
    'normal'   : normal
}

if __name__ == '__main__':
    types = sys.argv[1:]
    for pdf in tqdm(types):
        #print('PDF = {:s}'.format(pdf))
        funcs[pdf]()

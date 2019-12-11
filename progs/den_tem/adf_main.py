from adf_base  import *
from itertools import product

def base_script(**args):
    tem_means = [6e3, 8e3, 10e3]
    den_means = [100, 1000]
    for tem_mean, den_mean in product(tem_means, den_means):
        simul(cel_den='OIII', den_mean=den_mean, orl='OII',
              cel_tem='OIII', tem_mean=tem_mean, **args)

def lognormal(sigmas = [0.3, 0.5, 0.8], **args):
    for sigma in sigmas:
        params = {'sigma': sigma}
        base_script(params=params, pdf='lognormal', **args)

funcs = {
    'lognormal': lognormal
}



if __name__ == '__main__':
    types = sys.argv[1:]
    for pdf in types:
        print('PDF = {:s}'.format(pdf))
        funcs[pdf]()

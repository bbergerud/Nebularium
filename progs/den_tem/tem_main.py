from tem_base  import *
from itertools import product

def base_script(**args):
    den_means = [100, 1000]
    tem_means = [6e3, 8e3, 10e3]
    for tem_mean, den_mean in product(tem_means, den_means):
        simul(ion='BJ', grid=200, tem_mean=tem_mean, den_mean=den_mean, **args)
        for ion in cel_tem_dict.keys():
            simul(ion=ion, tem_mean=tem_mean, den_mean=den_mean, **args)

def lognormal(sigmas=[0.3, 0.5, 0.8]):
    for sigma in sigmas:
        params = {'sigma': sigma}
        base_script(params=params, pdf='lognormal')


funcs = {
    'lognormal': lognormal
}


if __name__ == '__main__':
    types = sys.argv[1:]
    for pdf in types:
        print('PDF = {:s}'.format(pdf))
        funcs[pdf]()

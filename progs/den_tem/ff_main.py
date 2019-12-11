from ff_base import *
from itertools import product

def basic_script(**args):

    cel_den_tem = [
        ('NI'  , 'NII'),
        ('SII' , 'SIII'),
    ]

    cel_dens = list(cel_den_dict.keys())
    for cel_den, cel_tem in cel_den_tem:
        cel_dens.remove(cel_den)

    den_means = [100, 1000]
    tem_means = [6e3, 8e3, 10e3]
    for tem_mean, den_mean in product(tem_means, den_means):

        for ion_den, ion_tem in cel_den_tem:
            simul(cel_den=ion_den, cel_tem=ion_tem,
                  tem_mean=tem_mean, den_mean=den_mean, **args)

        for ion_den in cel_dens:
            simul(cel_den=ion_den, cel_tem='OIII',
                  tem_mean=tem_mean, den_mean=den_mean, **args)

def lognormal(sigmas=[0.3, 0.5, 0.8], **args):
    pdf = 'lognormal'
    for sigma in sigmas:
        params = {'sigma': sigma}
        basic_script(params=params, pdf=pdf, **args)

funcs = {
    'lognormal': lognormal
}


if __name__ == '__main__':
    types = sys.argv[1:]
    for pdf in types:
        print('PDF = {:s}'.format(pdf))
        funcs[pdf]()

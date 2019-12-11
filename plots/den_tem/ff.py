import os, sys; sys.path.append('..'); sys.path.append(os.path.join('..', '..'))
import numpy as np
from base         import *
from itertools    import product
from nebulous.cel import cel_den_dict

def paper_plots():
    den = 1e3
    tem = 8e3
    pdf = 'lognormal'
    params = {'sigma': [0.3, 0.5, 0.8]}
    plot(
        ion = 'SII', type='den', diagnostic='ff', tem = tem, den = den,
        orl = None, iter_func = iter_params, csv_func = csv_params,
        get_legend = get_legend_params, params=params, pdf=pdf,
        ylim = (0.25, 1.75), yticks = np.arange(0.25, 1.76, 0.25),
        xticks = np.arange(0, 2.1, 0.5),
        save = True, img_dir = '../../paper/figure/den_tem/ff/',
        img_filename = 'lognormal_SII.pdf'
    )

def base_plot(**args):
    dens = [100, 1000]
    tems = [6e3, 8e3, 10e3]
    for tem, den in product(tems, dens):
        for ion in ['SII', 'OII']:
            plot(ion = ion, type='den', diagnostic='ff', tem = tem, den = den,
                 orl = None, iter_func = iter_params, csv_func = csv_params,
                 get_legend = get_legend_params, **args)

def lognormal(**args):
    params = {'sigma': [0.3, 0.5, 0.8]}
    base_plot(params=params, pdf='lognormal', **args)


funcs = {
    'lognormal'  : lognormal,
}

if __name__ == '__main__':
    types = sys.argv[1:]
    for pdf in types:
        print('PDF = {:s}'.format(pdf))
        funcs[pdf](save=True)

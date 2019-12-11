import os, sys; sys.path.append('..'); sys.path.append(os.path.join('..', '..'))
from base      import *
from itertools import product
from numpy import arange

def paper_plots():
    den = 1e3
    tem = 8e3
    pdf = 'lognormal'
    ylims = [(1, 5.25), (1, 3)]
    yticks = [arange(1, 5.1, 1), arange(1, 3.1, 0.5)]
    params = {'sigma': [0.3, 0.5, 0.8]}
    for type, ylim, yticks in zip(['tem', 'den'], ylims, yticks):
        plot(ion = 'OIII', type=type, diagnostic='adf', tem = tem, den = den,
             orl = 'OII', iter_func = iter_params, csv_func = csv_params,
             get_legend = get_legend_params,
             ylim=ylim, yticks=yticks, xticks = arange(0, 2.1, 0.5),
             pdf=pdf, params=params,
             reverse_legend=True, leg_loc='upper right',
             save=True, img_dir = '../../paper/figure/den_tem/adf',
             img_filename = 'OIII_{:s}_{:s}.pdf'.format(type, pdf)
        )

def base_plot(**args):
    dens = [100, 1000]
    tems = [6e3, 8e3, 10e3]
    for tem, den in product(tems, dens):
        for type in ['den', 'tem']:
            plot(ion = 'OIII', type=type, diagnostic='adf', tem = tem, den = den,
                 orl = 'OII', iter_func = iter_params, csv_func = csv_params,
                 get_legend = get_legend_params, ylim=(1, 5), **args)

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

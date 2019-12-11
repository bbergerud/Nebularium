import os, sys; sys.path.append('..'); sys.path.append(os.path.join('..', '..'))
from base import *
import numpy as np

def paper_plots():
    pdf_params = [
        ('lognormal', {'sigma': [0.3, 0.5, 0.8, 1.2]}),
        ('pareto',    {'sigma': [0.3, 0.8], 'c': [0.5, 0.1]})
    ]

    yticks = [np.linspace(1,3,5), np.linspace(1,9,5)]
    ylims  = [(min(y), max(y)) for y in yticks]

    args = {'tick_labelsize': 17}

    for ylim, yticks, (pdf, params) in zip(ylims, yticks, pdf_params):
        plot(ion='OIII', type='den', diagnostic='adf', tem=10e3, den=None,
             orl='OII',  iter_func=iter_params, csv_func=csv_params,
             get_legend=get_legend_params, pdf=pdf, params=params,
             ylim = ylim, yticks=yticks,
             reverse_legend=True, reverse_ls=True, reverse_color=False,
             save=True, img_dir = '../../paper/figure/den/adf',
             img_filename='OIII_den_{:s}.pdf'.format(pdf),
             **args
         )


def base_plot(**args):
    ion_types = [
        ('OIII', 'den'),
        ('OIII', 'tem'),
        #('OII',  'den')
    ]

    for ion, type in ion_types:
        plot(ion = ion, type=type, diagnostic='adf', tem = 10e3, den = None,
             orl = 'OII', iter_func = iter_params, csv_func = csv_params,
             get_legend = get_legend_params, **args)

def exponential(**args):
    params = {}
    base_plot(params=params, pdf='exponential', **args)

def lognormal(**args):
    params = {'sigma': [0.3, 0.5, 0.8, 1.2]}
    base_plot(params=params, pdf='lognormal', **args)

def mlp(**args):
    for sigma in [0.3, 0.8]:
        params = {'sigma': [sigma], 'alpha': [1.5, 2.5, 4.0]}
        base_plot(params=params, pdf='mlp', **args)

def pareto(**args):
    params = {'sigma': [0.3, 0.8], 'c': [0.5, 0.1]}
    base_plot(params=params, pdf='pareto', **args)

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
        funcs[pdf](save=True)

import os, sys; sys.path.append('..'); sys.path.append(os.path.join('..', '..'))
from base import *
from nebulous.cel import cel_den_dict

def paper_plots():
    pdf_params = [
        ('lognormal', {'sigma': [0.3, 0.5, 0.8, 1.2]}),
        ('pareto',    {'sigma': [0.3, 0.8], 'c': [0.5, 0.1]})
    ]

    ylim = [(0.2, 1.2), (0, 1.2)]

    args = {'tick_labelsize': 17}

    for ylim, (pdf, params) in zip(ylim, pdf_params):
        plot(ion='SII', type='den', diagnostic='ff', tem=10e3, den=None,
             orl=None,  iter_func=iter_params, csv_func=csv_params,
             get_legend=get_legend_params, pdf=pdf, params=params,
             ylim = ylim, fig_size = (7,7),
             reverse_legend=False, reverse_ls=True, reverse_color=False,
             save=True, img_dir = '../../paper/figure/den/ff/',
             img_filename='SII_den_{:s}.pdf'.format(pdf),
             **args
        )


def base_plot(**args):
    for ion in cel_den_dict.keys():
        plot(ion = ion, type='den', diagnostic='ff', tem = 10e3, den = None,
             orl = None, iter_func = iter_params, csv_func = csv_params,
             get_legend=get_legend_params, **args)

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

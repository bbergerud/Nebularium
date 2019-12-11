import os, sys; sys.path.append('..'); sys.path.append(os.path.join('..', '..'))
from base import *

def paper_plots():
    params = {'sigma': [0.1, 0.2, 0.3]}
    pdf    = 'lognormal'
    ylims  = [(1, 1.6), (1, 6)]
    for type, ylim in zip(['den', 'tem'], ylims):
        plot(ion = 'OIII', type=type, diagnostic='adf', tem = None, den = 1e3,
             orl = 'OII', iter_func = iter_params, csv_func = csv_params,
             get_legend=get_legend_params, leg_loc='upper right',
             reverse_ls = True, reverse_color=False, reverse_legend=True,
             save=True, img_dir = '../../paper/figure/tem/adf',
             img_filename = 'OIII_{:s}_{:s}.pdf'.format(type, pdf),
             pdf = pdf, params = params, figsize=(6.5,6),
             ylim = ylim
         )

def base_plot(**args):
    #for ion in cel_den_dict.keys():
    for type in ['den', 'tem']:
        plot(ion = 'OIII', type=type, diagnostic='adf', tem = None, den = 1e3,
             orl = 'OII', iter_func = iter_params, csv_func = csv_params,
             get_legend=get_legend_params, leg_loc='upper right',
             reverse_ls = True, reverse_color=False, reverse_legend=True, **args)

def lognormal(**args):
    params = {'sigma': [0.1, 0.2, 0.3]}
    base_plot(params=params, pdf='lognormal', **args)

def normal(**args):
    params = {'sigma': [0.1, 0.2, 0.3]}
    base_plot(params=params, pdf='normal', **args)


funcs = {
    'lognormal'  : lognormal,
    'normal'     : normal,
}

if __name__ == '__main__':
    types = sys.argv[1:]
    for pdf in types:
        print('PDF = {:s}'.format(pdf))
        funcs[pdf](save=True)

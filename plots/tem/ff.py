import os, sys; sys.path.append('..'); sys.path.append(os.path.join('..', '..'))
from base import *
from nebulous.cel import cel_den_dict

def base_plot(**args):
    for ion in cel_den_dict.keys():
        plot(ion = ion, type='den', diagnostic='ff', tem = None, den = 1e3,
             orl = None, iter_func = iter_params, csv_func = csv_params,
             get_legend=get_legend_params, leg_loc='best',
             reverse_ls = True, reverse_legend=True, **args)

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

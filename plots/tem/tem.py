import os, sys; sys.path.append('..'); sys.path.append(os.path.join('..', '..'))
from base import *

def paper_plots():
    ions   = ['NeIII', 'OIII', 'NII', 'SIII', 'BJ']
    ylims  = [(-1800, 1600), (-3000, 4000)]
    pdfs   = ['normal', 'lognormal']
    sigmas = [0.2, 0.3]
    for ylim, pdf, sigma in zip(ylims, pdfs, sigmas):
        params = {'sigma': [sigma]}
        plot(ion = ions, type='tem', diagnostic='tem', tem = None, den = 1e3,
             orl = None, iter_func = iter_ions, csv_func = csv_ions,
             get_legend=get_legend_ions, leg_loc='lower left',
             reverse_color=False, reverse_ls = False, reverse_legend=False,
             ylim=ylim, figsize = (6.5,8),
             leg_col=3, leg_fontsize=15,
             params = params, pdf=pdf, leg_ncol=3,
             save=True, img_dir = '../../paper/figure/tem/tem/',
             img_filename = '{:s}_sigma_{:s}.pdf'.format(pdf, str(sigma).replace('.',''))
        )

def base_plot(**args):
    ions = ['NeIII', 'OIII', 'NII', 'SIII', 'BJ']
    plot(ion = ions, type='tem', diagnostic='tem', tem = None, den = 1e3,
         orl = None, iter_func = iter_ions, csv_func = csv_ions,
         get_legend=get_legend_ions, leg_loc='lower left',
         reverse_color=False, reverse_ls = False, reverse_legend=False,
         leg_col=3, **args)

def lognormal(**args):
    for sigma in [0.1, 0.2, 0.3]:
        params = {'sigma': [sigma]}
        base_plot(params=params, pdf='lognormal', **args)

def normal(**args):
    for sigma in [0.1, 0.2, 0.3]:
        params = {'sigma': [sigma]}
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

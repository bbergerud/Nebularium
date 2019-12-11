import os, sys; sys.path.append('..'); sys.path.append(os.path.join('..', '..'))
from base         import *
from itertools    import product
from nebulous.cel import cel_den_dict

def paper_plots():
    ions = ['NeIII', 'OIII', 'NII', 'SIII', 'BJ']
    pdf = 'lognormal'
    for sigma in [0.3]:
        params = {'sigma': [sigma]}
        plot(
            ion = ions, type='tem', diagnostic='tem', tem=8e3, den=1e3,
            orl  = None, iter_func = iter_ions, csv_func = csv_ions,
            get_legend = get_legend_ions, params = params,
            leg_loc = 'upper center', leg_ncol=1, pdf=pdf,
            ylim = (6e3, 12e3),
            save=True, img_dir = '../../paper/figure/den_tem/tem',
            img_filename = '{:s}_sigma_{:s}.pdf'.format(pdf, str(sigma).replace('.', ''))
        )

def base_plot(**args):
    ions = ['NeIII', 'OIII', 'NII', 'SIII', 'BJ']
    dens = [100, 1000]
    tems = [6e3, 8e3, 10e3]
    for tem, den in product(tems, dens):
        for sigma in [0.3, 0.5, 0.8]:
            params = {'sigma': [sigma]}
            plot(ion = ions, type='tem', diagnostic='tem', tem = tem, den = den,
                 orl = None, iter_func = iter_ions, csv_func = csv_ions,
                 get_legend = get_legend_ions, params = params,
                 leg_loc='upper center', **args)

def lognormal(**args):
    base_plot(pdf='lognormal', **args)


funcs = {
    'lognormal'  : lognormal,
}

if __name__ == '__main__':
    types = sys.argv[1:]
    for pdf in types:
        print('PDF = {:s}'.format(pdf))
        funcs[pdf](save=True)

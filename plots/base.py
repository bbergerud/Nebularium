import os, sys; sys.path.append('..');
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_style('darkgrid')
plt.rc('font', family='serif')
plt.rc('text', usetex=True)

from axis      import *
from dirs      import *
from palettes  import *
from copy      import copy
from itertools import product
from nebulous.orl  import orl_dict
from nebulous.misc import mkdir
from mpltools.special import errorfill



def get_den_tem(den, tem):
    if den and not tem:   return 'tem'
    elif tem and not den: return 'den'
    elif den and tem:     return 'den_tem'
    else:
        print('den, tem are both null')
        sys.exit(1)


def fix_plot_args(args):
    if isinstance(args['color'], (str, type(None))):
        args['color'] = colors[args['color']]
        if args['reverse_color']:
            if args['color_size']:
                args['color'] = args['color'][:args['color_size']]
            args['color'] = args['color'][::-1]
    if isinstance(args['ls'], (str, type(None))):
        args['ls'] = linestyles[args['ls']]
        if args['reverse_ls']:
            args['ls'] = args['ls'][::-1]
    return args

base_plot_args = {
    'α_fill'        : 0.25,
    'borderaxespad' : None,
    'ax_fontsize'   : 25,
    'ax_xscale'     : lambda den_tem: 'log' if den_tem == 'den' else 'linear',
    'color'         : None,
    'color_size'    : None,
    'dpi'           : 300,
    'figsize'       : (6.5, 7),
    'img_type'      : 'png',
    'img_dir'       : None,
    'img_filename'  : None,
    'leg_fontsize'  : 16,
    'leg_linewidth' : 2.3,
    'leg_loc'       : 'best',
    'leg_ncol'      : 1,
    'ls'            : None,
    'lw'            : 1.75,
    'reverse_color' : False,
    'reverse_ls'    : False,
    'save'          : False,
    'tick_labelsize': 15,
    'tick_pad'      : 8,
    'xticks'        : None,
    'yticks'        : None,
}

def iter_params(args):
    for vals in args['param_sets']:
        yield vals

def iter_ions(args):
    for ion in args['ion']:
        yield ion





def plot(ion, type, den, tem, pdf, params, iter_func, csv_func,
        get_legend, diagnostic, orl = None, wave=0,
        get_x = get_x, get_y = get_y, ylim=None,
        get_ylabel=get_ylabel, ylim_func=get_ylim,
        reverse_legend=False, **args):

    # ====================================================
    # Generate the den_tem value; get the parameter sets
    # ====================================================
    den_tem = get_den_tem(den,tem)
    param_sets = list(product(*[v for i, v in params.items()]))
    keys = params.keys()

    # ====================================================
    # Create the plot_args dictionary
    # ====================================================
    global base_plot_args
    plot_args = copy(base_plot_args)
    for key, value in args.items():
        plot_args[key] = value
    plot_args['color_size'] = len(list(iter_func(locals())))
    plot_args = fix_plot_args(plot_args)

    # ====================================================
    # Check if an ORL should be loaded
    # ====================================================
    try: ion_orl = str(orl_dict[orl].wave[wave])[:4]
    except: pass

    # ====================================================
    # Set up the figure
    # ====================================================
    fig, ax = plt.subplots(figsize=plot_args['figsize'])

    # ====================================================
    # Iterate through the custom generator
    # ====================================================
    for i, item in enumerate(iter_func(locals())):
        df = csv_func(locals())

        legend_label = get_legend(locals())

        # ================================================
        # Add the density ratios to the plot
        # ================================================
        errorfill(
            x     = get_x(locals()),
            y     = get_y(locals()),
            yerr  = get_y(locals(), yerr=True),
            color = plot_args['color'][i],
            ls    = plot_args['ls'][i % len(plot_args['ls'])],
            lw    = plot_args['lw'],
            label = legend_label,
            alpha_fill = plot_args['α_fill']
        )

    # ====================================================
    # Add the labels
    # ====================================================
    ax.set_xlabel(get_xlabel(den_tem), fontsize=plot_args['ax_fontsize'])
    ax.set_ylabel(get_ylabel(locals()), fontsize=plot_args['ax_fontsize'])

    # ====================================================
    # Set the scales
    # ====================================================
    ax.set_xscale(plot_args['ax_xscale'](den_tem))
    ax.set_xlim(get_xlim(locals()))
    ax.set_ylim(ylim)
    ax.tick_params(
        axis='both', which='major', size=0,
        labelsize=plot_args['tick_labelsize'],
        pad=plot_args['tick_pad']
    )

    if plot_args['yticks'] is not None:
        ax.set_yticks(plot_args['yticks'])

    if plot_args['xticks'] is not None:
        ax.set_xticks(plot_args['xticks'])


    # ====================================================
    # Create the legend
    # ====================================================
    if legend_label:
        if reverse_legend:
            handles, labels = ax.get_legend_handles_labels()
            leg = ax.legend(handles[::-1], labels[::-1],
                loc=plot_args['leg_loc'],
                fontsize=plot_args['leg_fontsize'],
                frameon=False,
                ncol = plot_args['leg_ncol'],
                borderaxespad = plot_args['borderaxespad']
            )

        else:
            leg = ax.legend(
                loc=plot_args['leg_loc'],
                fontsize=plot_args['leg_fontsize'],
                frameon=False,
                ncol = plot_args['leg_ncol'],
                borderaxespad = plot_args['borderaxespad']
            )

        for legobj in leg.legendHandles:
            legobj.set_linewidth(plot_args['leg_linewidth'])

    fig.tight_layout()


    # ====================================================
    # Save or display image
    # ====================================================
    if plot_args['save']:
        if plot_args['img_dir']:
            directory = plot_args['img_dir']
        else:
            directory = get_img_directory(locals())

        if plot_args['img_filename']:
            filename = plot_args['img_filename']
        else:
            filename  = get_img_filename(locals())

        mkdir(directory)

        filename  = os.path.join(directory, filename)

        fig.savefig(filename)
        plt.close(fig)

    else:
        fig.show()

if __name__ == '__main__':
    """
    params = {'sigma': [0.3]}
    plot(
        ion = ['NeIII', 'OIII', 'NII', 'SIII', 'BJ'],
        type = 'den_tem',
        den  = 1e3,
        tem  = 8000,
        params = params,
        iter_func = iter_ions,
        csv_func = csv_ions,
        diagnostic = 'tem',
        pdf = 'lognormal'
    )

    params = {'sigma': [0.3, 0.5, 0.8]}
    plot(
        ion = 'SII', type='den_tem', den=1e3, tem=8e3,
        params = params, iter_func = iter_params,
        csv_func = csv_params, diagnostic='ff',
        pdf = 'lognormal'
    )

    params = {'sigma': [0.3, 0.5, 0.8]}
    plot(
        ion = 'OIII', type='den_tem', den=1e3, tem=8e3,
        params = params, iter_func=iter_params,
        csv_func = csv_params, diagnostic = 'adf',
        pdf = 'lognormal', orl = 'OII',
        ylim = None
    )

    params = {'sigma': [0.1, 0.2, 0.3]}
    plot(ion='OIII', type='tem', den=1e3, tem=None,
        params=params, iter_func=iter_params,
        csv_func = csv_params, diagnostic='tem', pdf='lognormal'
    )

    params = {'sigma': [0.2]}
    plot(ion=['NeIII', 'OIII', 'NII', 'SIII', 'BJ'], type='tem', den=1e3, tem=None,
        params=params, iter_func=iter_ions,
        csv_func = csv_ions, diagnostic='tem', pdf='normal'
    )

    params = {'sigma': [0.3, 0.5, 0.8, 1.2]}
    plot(ion='OIII', orl='OII', type='den', den=None, tem=10e3,
        params = params, iter_func=iter_params,
            csv_func = csv_params, diagnostic='adf', pdf='lognormal')

    plot(ion='SII', type='den', den=None, tem=10e3,
            params=params, iter_func=iter_params,
            csv_func = csv_params, diagnostic='ff', pdf='lognormal')

    params = {'sigma': [0.8]}
    plot(ion=['SII', 'OII'], type='den', den=None, tem=10e3,
            params=params, iter_func=iter_ions,
            csv_func = csv_ions, diagnostic='ff', pdf='lognormal')

    params = {'sigma': [0.3]}
    plot(ion='SII', type='den', den=1e3, tem=None,
            params=params, iter_func=iter_params,
            csv_func = csv_params, diagnostic='ff', pdf='lognormal')

    params = {'sigma': [0.3, 0.5, 0.8]}
    plot(ion='SII', type='den_tem', den=1e3, tem=10e3,
            params=params, iter_func=iter_params,
            csv_func = csv_params, diagnostic='ff', pdf='lognormal')
    """

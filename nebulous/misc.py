from collections import defaultdict
from copy        import copy
import numpy as np
import os

def mkdir(directory):
    os.makedirs(directory, exist_ok=True)

def fix_params(params, pdf, x):
    p = copy(params)
    if pdf == 'normal':
        p['sigma'] = p['sigma'] * x
    return p

# ===================================================
# Dictionaries containing the density ranges for
# the various ions along wit a function that will
# return the (min,max) values.
# ===================================================
den_dict = defaultdict(lambda: np.logspace(1,5,25))
key_val_pairs = [
    ['ArIV' , np.logspace(2, 6, 25)],
    ['CIII' , np.logspace(3, 7, 25)],
    ['ClIII', np.logspace(2, 5, 25)],
    ['KV'   , np.logspace(3, 7, 25)],
    ['NeIV' , np.logspace(2, 6, 25)],
    ['NI'   , np.logspace(1, 4, 25)],
    ['OII'  , np.logspace(1, 4, 25)],
    ['OIII' , np.logspace(1, 4, 25)],
    ['SII'  , np.logspace(1, 4, 25)],
    ['SiIII', np.logspace(2, 6, 25)]
]
for key, val in key_val_pairs:
    den_dict[key] = val

def den_limits(ion):
    den_range = den_dict[ion]
    return (den_range[0], den_range[-1])

# ===================================================
# Dictionaries containing labeling information for
# plotting
# ===================================================
def get_label(ion, l, delim='\,', forbid=True):
    label = r'$\mathrm{'
    if forbid:
        label += '['
    ion = "{:s}{:s}{:s}]".format(ion[:l], delim, ion[l:])
    ion += r'}$'
    return label + ion

ion_labels = {
    'ArIV'  : get_label(ion='ArIV', l=2),
    'CIII'  : get_label(ion='CIII', l=1, forbid=False),
    'ClIII' : get_label(ion='ClIII', l=2),
    'KV'    : get_label(ion='KV', l=1),
    'NI'    : get_label(ion='NI', l=1),
    'NII'   : get_label(ion='NII', l=1),
    'NIII'  : get_label(ion='NIII', l=1),
    'NeIII' : get_label(ion='NeIII', l=2),
    'NeIV'  : get_label(ion='NeIV', l=2),
    'OII'   : get_label(ion='OII', l=1),
    'OIII'  : get_label(ion='OIII', l=1),
    'SII'   : get_label(ion='SII', l=1),
    'SIII'  : get_label(ion='SIII', l=1),
    'BJ'    : r'$\mathrm{BJ}$'
}



def get_label(ion, l, delim='\,', forbid=True):
    label = r'$\langle n_{e} \; \mathrm{'
    ion = "[{:s}{:s}{:s}]".format(ion[:l], delim, ion[l:])
    ion += r'}\rangle \, / \, \bar{n}_{e}$'
    return label + ion

den_ratio_labels = {
    'ArIV'  : get_label(ion='ArIV', l=2),
    'CIII'  : get_label(ion='CIII', l=1, forbid=False),
    'ClIII' : get_label(ion='ClIII', l=2),
    'KV'    : get_label(ion='KV', l=1),
    'NI'    : get_label(ion='NI', l=1),
    'OII'   : get_label(ion='OII', l=1),
    'OIII'  : get_label(ion='OIII', l=1),
    'SII'   : get_label(ion='SII', l=1)
}


def get_label(ion, cel, orl):
    def base(ion, symbol):
        return r'\mathrm{' + ion + r'}^{' + symbol + r'}'
    def label(ion, symbol):
        symbol = base(ion, symbol)
        numen = r'$\langle n(' + symbol + r')'
        denom = r'n_{*}\left(' + symbol + r'\right) \rangle$'
        return numen + r'\; / \;' + denom
    orl = label(ion, orl)
    cel = label(ion, cel)
    return cel, orl

abundance_labels = {
    ('OII', 'OII') :  get_label('O', '+',  '+2'),
    ('OIII','OII') :  get_label('O', '+2', '+2')
}

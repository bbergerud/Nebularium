
roman_to_int = {
    'I'  : 1,
    'II' : 2,
    'III': 3,
    'IV' : 4,
    'V'  : 5,
    'VI' : 6,
}




# ===================================================
# Axis values
# ===================================================
def get_x(args):
    column = {
        'den': 'den',
        'tem': 'tem',
        'den_tem': 'gamma',
    }[args['den_tem']]
    df = args['df']
    return df[column]

def get_y(args, yerr=False):
    if (args['den_tem'] != 'den_tem') or (args['diagnostic'] != 'adf'):
        column = {
            'adf': lambda yerr, args: 'ADF_{:s}_{:s}'.format('std' if yerr else 'avg', args['ion_orl']),
            'ff' : lambda yerr, args: 'ratio_{:s}'.format('std' if yerr else 'avg'),
            'tem': lambda yerr, args: 'tem_{:s}'.format('std' if yerr else 'avg'),
        }[args['diagnostic']](yerr, args)
    else:
        column = 'ADF_{:s}_{:s}_{:s}'.format(
            args['type'], 'std' if yerr else 'avg', args['ion_orl']
        )

    df = args['df']
    if (args['diagnostic'] == 'tem') and (args['den_tem'] == 'tem') and (not yerr):
        return df[column] - df['tem']
    else:
        return df[column]

# ===================================================
# Axis limits
# ===================================================
def get_xlim(args):
    xvals = get_x(args)
    return (min(xvals), max(xvals))

def get_ylim(args):
    try:
        return args['ylim']
    except:
        return None

# ===================================================
# Axis labels
# ===================================================
def get_xlabel(den_tem):
    return {
        'den': r'$\bar{n}_{e} \; \left(\mathrm{cm}^{-3}\right)$',
        'tem': r'$\overline{T} \; \left(\mathrm{K}\right)$',
        'den_tem': r'$\mathrm{Polytropic \; Index}, \; \gamma$',
    }[den_tem]

def get_ylabel(args):
    diagnostic = args['diagnostic']
    return {
        'adf': get_adf_label,
        'ff' : get_ff_label,
        'tem': get_tem_label,
    }[diagnostic](args)

# ===================================================
# Legend labels
# ===================================================
def get_legend_ions(args):
    ion = args['item']
    label = get_ion_label(ion, latex=True)

    if ion == 'BJ':
        return label
    else:
        return '[' + label + ']'

def get_legend_params(args):
    # Might need "sigma/T" for the normal distribution
    # could have pdf='normal' argument

    label = ''
    params = args['param_sets'][args['i']]
    for j, key in enumerate(args['keys']):

        # Extract value from (key,value)
        value = params[j]

        # Generate legend label
        if key in ['alpha', 'sigma']:
            key = '\{:s}'.format(key)
        label += '{:s} = {:.1f}, \,'.format(key, value)

    label = "${}$".format(label[:-4]) if label else None
    return label


# ===================================================
# Ion Labels
# ===================================================


def get_ion_label(ion, latex=True, delim='\;'):
    if ion == 'BJ':
        if latex: return r'$\mathrm{' + ion + '}$'
        else: return 'BJ'
    else:
        # Find the split
        if ion[1].islower():
            element = ion[:2]
            ionization = ion[2:]
        else:
            element = ion[0]
            ionization = ion[1:]

        if latex:
            return r'$\mathrm{' + element + r'}' + delim \
                  +r'\textsc{' + ionization.lower() + r'}$'
        else:
            return element + delim + ionization

def get_adf_label(args, delim='\;'):
    cel, cion = get_ion_label(args['ion'], delim=' ', latex=False).split()
    orl, oion = get_ion_label(args['orl'], delim=' ', latex=False).split()

    cion = roman_to_int[cion]-1
    oion = roman_to_int[oion]

    cion = '^{+%d}' % cion if cion > 1 else '^{+}'
    oion = '^{+%d}' % oion if oion > 1 else '^{+}'

    def foo(elem, ioniz, line):
        return 'n(\mathrm{%s}%s)_\mathrm{%s}' % (elem, ioniz, line)

    def foo(elem, ioniz, line):
        return 'X(\mathrm{%s}%s)_\mathrm{%s}' % (elem, ioniz, line)

    label = foo(orl, oion, 'ORL') + delim + '/' + delim + foo(cel, cion, 'CEL')
    return r'$\langle ' + label + r'\rangle$'

def get_ff_label(args, delim='\,', latex=True):
    ion = args['ion']
    if isinstance(ion, list):
        return r'$\langle n_{e} \; [\mathrm{EM}] \, / \, n_{e} \; [\mathrm{CEL}]\rangle$'
    else:
        return r'$\langle n_{e} \; [\mathrm{EM}] \, / \, n_{e} \; [$' \
                + get_ion_label(ion, delim=delim, latex=True) \
                + r'$]\rangle$'

def get_tem_label(args, diff=False):
    if args['den_tem'] != 'den_tem':
        return r'$\langle T \rangle - \overline{T} \; \left(\mathrm{K}\right)$'
    else:
        return r'$\langle T \rangle \; \left(\mathrm{K}\right)$'

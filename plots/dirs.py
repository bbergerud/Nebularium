import os
import pandas as pd

# ====================================================
# Temperature/Density Folder
# ====================================================
def get_den_tem_dir(den, tem):
    s = ''
    if den: s += 'N_{:d}_'.format(int(den))
    if tem: s += 'T_{:d}_'.format(int(tem))
    return s[:-1]

def get_directory(args):
    dir     = args['dir']
    den     = args['den']
    tem     = args['tem']
    pdf     = args['pdf']
    den_tem = args['den_tem']
    diagnostic = args['diagnostic']

    return os.path.join(
        '..', '..', dir, den_tem, diagnostic,
        pdf, get_den_tem_dir(den,tem)
    )


# ====================================================
# CSV files
# ====================================================

def get_csv_filename(args):
    ion     = args['ion']
    type    = args['type']
    den_tem = args['den_tem']
    values  = args['values']
    keys    = args['keys']

    filename = '{:s}_{:s}'.format(ion, type) if den_tem != 'den_tem' else ion
    for key, value in zip(keys, values):
        filename += '_{:s}_{:s}'.format(key, str(value).replace('.', ''))
    return filename + '.csv'


def csv_ions(args):
    dir     = 'data'
    index   = args['i']
    den     = args['den']
    tem     = args['tem']
    ion     = args['ion'][index]
    den_tem = args['den_tem']
    type    = args['type']
    keys    = args['keys']
    values  = args['param_sets'][0]
    pdf     = args['pdf']
    diagnostic = args['diagnostic']

    directory = get_directory(locals())
    filename  = get_csv_filename(locals())
    return pd.read_csv(os.path.join(directory, filename))

def csv_params(args):
    # Extract the appropriate variables
    dir     = 'data'
    den     = args['den']
    tem     = args['tem']
    den_tem = args['den_tem']
    ion     = args['ion']
    type    = args['type']
    keys    = args['keys']
    values  = args['param_sets'][args['i']]
    pdf     = args['pdf']
    diagnostic = args['diagnostic']

    directory = get_directory(locals())
    filename  = get_csv_filename(locals())
    return pd.read_csv(os.path.join(directory, filename))


# ====================================================
# Images
# ====================================================
def get_img_filename(args):
    ion    = args['ion']
    type   = args['type']
    params = args['params']
    img_type = args['plot_args']['img_type']

    if isinstance(ion, list):
        filename = ''
        for key, value in params.items():
            filename += '{:s}_{:s}_'.format(key, str(value[0]).replace('.', ''))
        return filename[:-1] + '.{:s}'.format(img_type)

    else:
        filename = '{:s}_{:s}'.format(ion, type)
        for key, value in params.items():
            if len(value) == 1:
                filename += '_{:s}_{:s}'.format(key, str(value[0]).replace('.', ''))
        return filename + '.{:s}'.format(img_type)

def get_img_directory(args):
    # Extract variables for directory
    dir     = 'figure'
    den     = args['den']
    tem     = args['tem']
    pdf     = args['pdf']
    den_tem = args['den_tem']
    diagnostic = args['diagnostic']

    directory = get_directory(locals())
    return directory

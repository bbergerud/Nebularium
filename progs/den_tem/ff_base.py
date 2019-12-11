"""

"""

import sys, os; sys.path.append(os.path.join('..', '..'))
import numpy  as np
import pandas as pd

from nebulous.geom  import sphere
from nebulous.em    import getEM, getSkyDenEM
from nebulous.cel   import cel_den_dict, cel_tem_dict
from nebulous.orl   import orl_dict
from nebulous.pdf   import pdfs
from nebulous.utils import getDepth
from nebulous.misc  import fix_params, mkdir

# ==================================================
# set the nebula parameters
# ==================================================
dim = (30,30,30)
loc = sphere(dim=dim, inRad=0.3, outRad=0.9)
depth = getDepth(loc=loc, dim=dim)
los = depth > 5

# ==================================================
# Function that runs the simulation
# ==================================================
def simul(cel_den, cel_tem, pdf, params, tem_mean, den_mean,
    convl=True, kernel=1, grid=25):

    # ==================================================
    # Copy the density ion for saving
    # ==================================================
    ion = cel_den

    # ==================================================
    # Set params to an empty dictionary if no values are passed
    # ==================================================
    if params is None:
        params = {}

    # ==================================================
    # Grab the appropriate ion diagnostics
    # ==================================================
    cel_den = cel_den_dict[cel_den]
    cel_tem = cel_tem_dict[cel_tem]
    bj = orl_dict['BJ']

    # ==================================================
    # Create the grid over the index space
    # ==================================================
    gammas = np.linspace(0, 2, grid)

    # ==================================================
    # Create a data frame to hold the values
    # ==================================================
    df = pd.DataFrame()

    # ==================================================
    # If there is a normal distribution of densities,
    # then use <sigma> * <x> for the standard deviation.
    # ==================================================
    p = fix_params(params=params, pdf=pdf, x=den_mean)

    # ==================================================
    # Generate the electron density distribution
    # ==================================================
    n_e = pdfs[pdf](dim=dim, loc=loc, mean=den_mean, **p)

    # ==================================================
    # Iterate through each value in the index grid
    # ==================================================
    print("PDF = {:s}, Ion = {:s}, Params = {}".format(pdf, ion, params))
    for index in gammas:

        # ==================================================
        # Generate the temperature distribution
        # ==================================================
        tem = pdfs['polytrope'](cube=n_e, index=index, mean=tem_mean, geom=False, loc=loc)

        # ==============================================
        # Get the temperature estimate from the CELs
        # ==============================================
        cel_tem.getEmissivity(tem=tem, n_e=n_e, loc=loc)
        cel_tem.getSkyEmiss(convl=convl, kernel=kernel)
        cel_tem.getSkyTem(skyDen=den_mean)

        # ==============================================
        # Get the density from the CELs
        # ==============================================
        cel_den.getEmissivity(tem=tem, n_e=n_e, loc=loc)
        cel_den.getSkyEmiss(convl=convl, kernel=kernel)
        cel_den.getSkyDen(skyTem=cel_tem.skyTem)

        # ==============================================
        # Get the temperature estimate from the BJ
        # ==============================================
        bj.getEmissivity(tem=tem, n_e=n_e, loc=loc)
        bj.getSkyEmiss(convl=convl, kernel=kernel)
        bj.getSkyTem(skyDen=den_mean)

        # ==================================================
        # Get the density estimate from the emission measure.
        # ==================================================
        EM = getEM(tem=tem, n_e=n_e,
            convl=convl, kernel=kernel,
            depth=depth, skyTem=bj.skyTem)
        skyDenEM = getSkyDenEM(EM=EM, depth=depth)

        # ==================================================
        # Compute the ratio of density estimates and store
        # the values.
        # ==================================================
        ff = skyDenEM[los] / cel_den.skyDen[los]

        data = {
            'BJ_tem_avg'  : np.nanmean(bj.skyTem[los]),
            'BJ_tem_std'  : np.nanstd(bj.skyTem[los], ddof=1),
            'CEL_den_avg' : np.nanmean(cel_den.skyDen[los]),
            'CEL_den_std' : np.nanstd(cel_den.skyDen[los], ddof=1),
            'CEL_tem_avg' : np.nanmean(cel_tem.skyTem[los]),
            'CEL_tem_std' : np.nanstd(cel_tem.skyTem[los], ddof=1),
            'EM_den_avg'  : np.nanmean(skyDenEM[los]),
            'EM_den_std'  : np.nanstd(skyDenEM[los], ddof=1),
            'ratio_avg'   : np.nanmean(ff),
            'ratio_std'   : np.nanstd(ff, ddof=1)
        }

        df = df.append(data, ignore_index=True)

    # ==================================================
    # Add the indecies
    # ==================================================
    df['gamma'] = gammas

    # ==================================================
    # Set the path for saving the file
    # ==================================================
    path = os.path.join(
        '..', '..', 'data', 'den_tem', 'ff', pdf,
        'N_{:d}_T_{:d}'.format(int(den_mean), int(tem_mean))
    )
    mkdir(path)

    # ==================================================
    # Save the data as a csv file
    # ==================================================
    if params:
        for key, value in params.items():
            value = str(value)
            ion += '_{:s}_{:s}'.format(key, value.replace('.', ''))

    ion += '.csv'
    df.to_csv(os.path.join(path, ion), index=False)

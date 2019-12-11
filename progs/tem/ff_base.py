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
from nebulous.misc  import fix_params, mkdir
from nebulous.utils import getDepth

# ==================================================
# set the nebula parameters
# ==================================================
dim   = (30,30,30)
loc   = sphere(dim=dim, inRad=0.3, outRad=0.9)
depth = getDepth(loc=loc, dim=dim)
los   = depth > 5

# ==================================================
# Function that runs the simulation
# ==================================================
def simul(cel_den, cel_tem, pdf, params, den=1e3, convl=True, kernel=1, grid=25):

    # ==================================================
    # Set params to an empty dictionary if None
    # ==================================================
    if params is None:
        params = {}

    # ==================================================
    # Get the ion type for saving the file
    # ==================================================
    ion = cel_den

    # ==================================================
    # Create the grid over the temperature space
    # ==================================================
    tems = np.linspace(5e3, 15e3, grid)

    # ==================================================
    # Grab the appropriate ion diagnostics
    # ==================================================
    cel_tem = cel_tem_dict[cel_tem]
    cel_den = cel_den_dict[cel_den]
    bj = orl_dict['BJ']

    # ==================================================
    # Create a data frame to hold the values
    # ==================================================
    df = pd.DataFrame()

    # ==================================================
    # Iterate through each value in the density grid
    # ==================================================
    for x in tems:

        # ==================================================
        # Print out the current status
        # ==================================================
        print("PDF = {:s}, Ion = {:s}, Mean = {:.0f}".format(pdf, ion, x))

        # ==================================================
        # If there is a normal distribution of temperatures,
        # then use <sigma> * <x> for the standard deviation.
        # ==================================================
        p = fix_params(params=params, pdf=pdf, x=x)

        # ==================================================
        # Generate the temperature distribution
        # ==================================================
        tem = pdfs[pdf](dim=dim, loc=loc, mean=x, **p)

        # ==============================================
        # Get the temperature estimate from the CELs
        # ==============================================
        cel_tem.getEmissivity(tem=tem, n_e=den, loc=loc)
        cel_tem.getSkyEmiss(convl=convl, kernel=kernel)
        cel_tem.getSkyTem(skyDen=den)

        # ==================================================
        # Get the density estimate from the line ratio.
        # ==================================================
        cel_den.getEmissivity(tem=tem, n_e=den, loc=loc)
        cel_den.getSkyEmiss(convl=convl, kernel=kernel)
        cel_den.getSkyDen(skyTem=cel_tem.skyTem)

        # ==================================================
        # Get the temperature estimate from the Balmer Jump,
        # which better matches the radio temperature
        # ==================================================
        bj.getEmissivity(tem=tem, n_e=den, loc=loc)
        bj.getSkyEmiss(convl=convl, kernel=kernel)
        bj.getSkyTem(skyDen=den)

        # ==================================================
        # Get the density estimate from the emission measure.
        # ==================================================
        EM = getEM(tem=tem, n_e=den, convl=convl, kernel=kernel,
                   depth=depth, skyTem=bj.skyTem)
        skyDenEM = getSkyDenEM(EM=EM, depth=depth)

        # ==================================================
        # Compute the ratio of density estimates and store
        # ==================================================
        ff = skyDenEM[los] / cel_den.skyDen[los]

        data = {
            'CEL_den_avg' : np.nanmean(cel_den.skyDen[los]),
            'CEL_den_std' : np.nanstd(cel_den.skyDen[los], ddof=1),
            'EM_den_avg'  : np.nanmean(skyDenEM[los]),
            'EM_den_std'  : np.nanstd(skyDenEM[los], ddof=1),
            'ratio_avg'   : np.nanmean(ff),
            'ratio_std'   : np.nanstd(ff, ddof=1),
            'CEL_tem_avg' : np.nanmean(cel_tem.skyTem[los]),
            'CEL_tem_std' : np.nanstd(cel_tem.skyTem[los], ddof=1),
            'BJ_tem_avg'  : np.nanmean(bj.skyTem[los]),
            'BJ_tem_std'  : np.nanstd(bj.skyTem[los], ddof=1)
        }

        df = df.append(data, ignore_index=True)

    # ==================================================
    # Add the temperature values to the data frame
    # ==================================================
    df['tem'] = tems

    # ==================================================
    # Set the path for saving the file
    # ==================================================
    path = os.path.join(
        '..', '..', 'data', 'tem', 'ff', pdf,
        'N_{:d}'.format(int(den))
    )
    mkdir(path)

    # ==================================================
    # Save the data as a csv file
    # ==================================================
    ion += '_den'

    if params:
        for key, value in params.items():
            value = str(value)
            ion += '_{:s}_{:s}'.format(key, value.replace('.', ''))

    ion += '.csv'
    df.to_csv(os.path.join(path, ion), index=False)

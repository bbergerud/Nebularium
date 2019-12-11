"""
Instance:
    Tem:    Constant
    Den:    Variable

Iterates over a range of mean electron densities and estimates the
density from the observed emission using a CEL and the emission measure.

The density estimates are then used to construct a measure of the filling
factor (in actuality, the ratio of density estimates is taken, or the
square-root of the filling factor).
"""

import os, sys; sys.path.append(os.path.join('..', '..'))
import numpy  as np
import pandas as pd

from nebulous.em    import getEM, getSkyDenEM
from nebulous.geom  import sphere
from nebulous.cel   import cel_den_dict, cel_tem_dict
from nebulous.orl   import orl_dict
from nebulous.misc  import den_dict, fix_params, mkdir
from nebulous.pdf   import pdfs
from nebulous.utils import getDepth


# ==================================================
# set the nebula parameters
# ==================================================
dim   = (30,30,30)
loc   = sphere(dim=dim, inRad=0.3, outRad=0.9)
depth = getDepth(loc=loc, dim=dim)
los   = depth > 5
convl = True

# ==================================================
# Function that runs the simulation
# ==================================================
def simul(cel_den, pdf, params, tem=10e3, kernel=1):

    # ==================================================
    # Set params to an empty dictionary if None
    # ==================================================
    if params is None:
        params = {}

    # ==================================================
    # Create the grid over the density space
    # ==================================================
    dens = den_dict[cel_den]

    # ==================================================
    # Grab the indicated ion diagnostic
    # ==================================================
    cel = cel_den_dict[cel_den]

    # ==================================================
    # Create a data frame to hold the values
    # ==================================================
    df = pd.DataFrame()

    # ==================================================
    # Iterate through each value in the density grid
    # ==================================================
    for x in dens:

        # ==================================================
        # Print out the current status
        # ==================================================
        print("PDF = {:s}, Ion = {:s}, Mean = {:.0f}".format(pdf, cel_den, x))

        # ==================================================
        # If there is a normal distribution of densities,
        # then use <sigma> * <x> for the standard deviation.
        # ==================================================
        p = fix_params(params=params, pdf=pdf, x=x)

        # ==============================================
        # Generate the electron densities
        # ==============================================
        n_e = pdfs[pdf](dim=dim, loc=loc, mean=x, **p)

        # ==================================================
        # Get the density estimate from the emission measure.
        # ==================================================
        EM       = getEM(n_e=n_e, convl=convl, kernel=kernel)
        skyDenEM = getSkyDenEM(EM=EM, depth=depth)

        # ==================================================
        # Get the density estimate from the line ratio.
        # ==================================================
        cel.getEmissivity(tem=tem, n_e=n_e, loc=loc)
        cel.getSkyEmiss(convl=convl, kernel=kernel)
        cel.getSkyDen(skyTem=tem)

        # ==================================================
        # Extract some diagnostical information
        # ==================================================
        ff = skyDenEM[los] / cel.skyDen[los]

        data = {
            'CEL_den_avg' : np.nanmean(cel.skyDen[los]),
            'CEL_den_std' : np.nanstd(cel.skyDen[los], ddof=1),
            'EM_den_avg'  : np.nanmean(skyDenEM[los]),
            'EM_den_std'  : np.nanstd(skyDenEM[los], ddof=1),
            'ratio_avg'   : np.nanmean(ff),
            'ratio_std'   : np.nanstd(ff, ddof=1),
        }

        # ==================================================
        # Store the results in the data frame
        # ==================================================
        df = df.append(data, ignore_index=True)

    # ==================================================
    # Add the density to the df
    # ==================================================
    df['den'] = dens

    # ==================================================
    # Set the path for saving the file
    # ==================================================
    path = os.path.join('..', '..', 'data', 'den', 'ff', pdf, 'T_{:d}'.format(int(tem)))
    mkdir(path)

    # ==================================================
    # Save the data as a csv file
    # ==================================================
    ion = cel_den + '_den'

    if params:
        for key, value in params.items():
            value = str(value)
            ion += '_{:s}_{:s}'.format(key, value.replace('.', ''))

    ion += '.csv'
    df.to_csv(os.path.join(path, ion), index=False)

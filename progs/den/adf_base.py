"""
Instance:
    Tem:    Constant
    Den:    Variable

Iterates over a range of mean electron densities and estimates the
density from the observed emission using a CEL.

The density estimate is then used to reconstruct the abundance using
a CEL and a ORL by comparing the line intensity with the H-beta intensity.
The ADF value is then computed.

Note: The true abundance is 1 by default.
"""

import sys, os; sys.path.append(os.path.join('..', '..'))
import numpy  as np
import pandas as pd

from nebulous.geom  import sphere
from nebulous.cel   import cel_den_dict, cel_tem_dict
from nebulous.orl   import orl_dict
from nebulous.misc  import den_dict, fix_params, mkdir
from nebulous.pdf   import pdfs
from nebulous.utils import getDepth

# ==================================================
# Set the nebula parameters
# ==================================================
dim   = (30,)
loc   = sphere(dim=dim, inRad=0.3, outRad=0.9)
los   = getDepth(loc=loc, dim=dim) > 5
convl = True

# ==================================================
# Function that runs the simulation
# ==================================================
def simul(cel_den, cel_tem, orl, pdf, params, tem=10e3, kernel=2):

    # ==================================================
    # Set params to an empty dictionary if None
    # ==================================================
    if params is None:
        params = {}

    # ==================================================
    # Get the ion type for saving the file
    # ==================================================
    ion = cel_tem if cel_tem else cel_den

    # ==================================================
    # Create the grid over the density space
    # ==================================================
    dens = den_dict[cel_den]

    # ==================================================
    # Grab the appropriate ion diagnostics
    # ==================================================
    cel_tem = cel_tem_dict[cel_tem] if cel_tem else None
    cel_den = cel_den_dict[cel_den]
    orl = orl_dict[orl]
    h1  = orl_dict['HI']

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
        print("PDF = {:s}, Ion = {:s}, Mean = {:.0f}".format(pdf, ion, x))

        # ==================================================
        # If there is a normal distribution of densities,
        # then use <sigma> * <x> for the standard deviation.
        # ==================================================
        p = fix_params(params=params, pdf=pdf, x=x)

        # ==============================================
        # Generate the electron densities
        # ==============================================
        n_e = pdfs[pdf](dim=dim, loc=loc, mean=x, **p)

        # ==============================================
        # Generate the H-beta intensities
        # ==============================================
        h1.getEmissivity(tem=tem, n_e=n_e)
        h1.getSkyEmiss(convl=convl, kernel=kernel)

        # ==============================================
        # Generate the CEL emission to get the density
        # estimate.
        # ==============================================
        cel_den.getEmissivity(tem=tem, n_e=n_e, loc=loc)
        cel_den.getSkyEmiss(convl=convl, kernel=kernel)
        cel_den.getSkyDen(skyTem=tem)

        # ==============================================
        # Get the abundance estimate; if a temperature
        # sensitive line set is passed, then use this
        # set to get the ion abundance estimate
        # ==============================================
        if cel_tem:
            cel_tem.getEmissivity(tem=tem, n_e=n_e, loc=loc)
            cel_tem.getSkyEmiss(convl=convl, kernel=kernel)
            cel_tem.getIonAbundance(skyTem=tem, skyDen=cel_den.skyDen, Hbeta=h1.skyBeta, los=los)
            cel_abd = cel_tem.ionAbundance[0][los]
        else:
            cel_den.getIonAbundance(skyTem=tem, skyDen=cel_den.skyDen, Hbeta=h1.skyBeta, los=los)
            cel_abd = cel_den.ionAbundance[0][los]

        # ==============================================
        # Generate the ORL emission and estimate the
        # abundance
        # ==============================================
        orl.getEmissivity(tem=tem, n_e=n_e)
        orl.getSkyEmiss(convl=convl, kernel=kernel)
        orl.getIonAbundance(skyTem=tem, skyDen=cel_den.skyDen, Hbeta=h1.skyBeta, los=los)

        # ==============================================
        # Compute the ADF values and store the results
        # ==============================================
        data = {
            "CEL_abd_avg" : np.nanmean(cel_abd),
            "CEL_abd_std" : np.nanstd(cel_abd, ddof=1),
        }

        for i, label in enumerate(orl.wave):
            wave = label[:4]
            orl_adf = orl.ionAbundance[i][los] / cel_abd
            orl_abd = orl.ionAbundance[i][los]

            data['ORL_abd_avg_' + wave] = np.nanmean(orl_abd)
            data['ORL_abd_std_' + wave] = np.nanstd(orl_abd, ddof=1)
            data['ADF_avg_' + wave] = np.nanmean(orl_adf)
            data['ADF_std_' + wave] = np.nanstd(orl_adf, ddof=1)

        df = df.append(data, ignore_index=True)

    # ==================================================
    # Add the density to the data frame
    # ==================================================
    df['den'] = dens

    # ==================================================
    # Set the path for saving the file
    # ==================================================
    path = os.path.join('..', '..', 'data', 'den', 'adf', pdf, 'T_{:d}'.format(int(tem)))
    mkdir(path)

    # ==================================================
    # Save the data as a csv file
    # ==================================================
    ion += '_tem' if cel_tem else '_den'

    if params:
        for key, value in params.items():
            value = str(value)
            ion += '_{:s}_{:s}'.format(key, value.replace('.', ''))

    ion += '.csv'
    df.to_csv(os.path.join(path, ion), index=False)

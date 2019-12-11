"""
Instance:
    Den:    Variable
    Tem:    Polytrope(Den)

Iterates over a range of polytropic indecies and estimates the
temperature from the observed emission using a CEL and the Balmer jump.
The density is assumed equal to the mean density.

The temperature estimates are then used to estimate the electron density.

The density and temperature estimates are then used to reconstruct the
abundance using a CEL and a ORL by comparing the line intensity with
the H-beta intensity. The ADF value is then computed.

Note: The true abundance is 1 by default.
"""

import sys, os; sys.path.append(os.path.join('..', '..'))
import numpy  as np
import pandas as pd

from nebulous.geom  import sphere
from nebulous.cel   import cel_den_dict, cel_tem_dict
from nebulous.orl   import orl_dict
from nebulous.pdf   import pdfs
from nebulous.utils import getDepth
from nebulous.misc  import fix_params, mkdir

# ==================================================
# set the nebula parameters
# ==================================================
dim = (30,30,30)
loc   = sphere(dim=dim, inRad=0.3, outRad=0.9)
depth = getDepth(loc=loc, dim=dim)
los   = depth > 5

# ==================================================
# Function that runs the simulation
# ==================================================
def simul(cel_den, cel_tem, orl, pdf, params, grid=50, kernel=1, convl=True,
            cel_den_wave=0, cel_tem_wave=0, tem_mean=8e3, den_mean=1e3):

    # ==================================================
    # Copy the density ion for saving
    # ==================================================
    ion = cel_den

    # ==================================================
    # Set the path for saving the file
    # ==================================================
    path = os.path.join(
        '..', '..', 'data', 'den_tem', 'adf', pdf,
        'N_{:d}_T_{:d}'.format(int(den_mean), int(tem_mean))
    )
    mkdir(path)

    # ==================================================
    # Set params to an empty dictionary if None
    # ==================================================
    if params is None:
        params = {}

    # ==================================================
    # Grab the appropriate ion diagnostics
    # ==================================================
    cel_den = cel_den_dict[cel_den]
    cel_tem = cel_tem_dict[cel_tem]
    orl = orl_dict[orl]
    h1  = orl_dict['HI']
    bj  = orl_dict['BJ']

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
    # Iterate through each value in the index grid.
    # ==================================================
    for index in gammas:

        # ==================================================
        # Print out the current status
        # ==================================================
        #print("PDF = {:s}, Ion = {:s}, Index = {:.2f}".format(pdf, ion, index))
        print("PDF = {:s}, Ion = {:s}, Index = {:.2f}, Params = {}".format(pdf, ion, index, params))


        # ==================================================
        # Generate the temperature distribution
        # ==================================================
        tem = pdfs['polytrope'](cube=n_e, index=index, mean=tem_mean, geom=False, loc=loc)

        # ==============================================
        # Generate the H-beta intensities
        # ==============================================
        h1.getEmissivity(tem=tem, n_e=n_e)
        h1.getSkyEmiss(convl=convl, kernel=kernel)

        # ==============================================
        # Get the temperature estimate from the CELs
        # Assumes density is equal to mean density.
        # ==============================================
        cel_tem.getEmissivity(tem=tem, n_e=n_e, loc=loc)
        cel_tem.getSkyEmiss(convl=convl, kernel=kernel)
        cel_tem.getSkyTem(skyDen=den_mean)

        # ==============================================
        # Get the density from the CELs.
        # Uses temperature estimate from CELs.
        # ==============================================
        cel_den.getEmissivity(tem=tem, n_e=n_e, loc=loc)
        cel_den.getSkyEmiss(convl=convl, kernel=kernel)
        cel_den.getSkyDen(skyTem=cel_tem.skyTem)

        # ==============================================
        # Get the abundances from the two CELs
        # ==============================================
        cel_den.getIonAbundance(
            skyTem=cel_tem.skyTem,
            skyDen=cel_den.skyDen,
            Hbeta=h1.skyBeta,
            los=los
        )
        abd_den = cel_den.ionAbundance[cel_den_wave][los]

        cel_tem.getIonAbundance(
            skyTem=cel_tem.skyTem,
            skyDen=cel_den.skyDen,
            Hbeta=h1.skyBeta,
            los=los
        )
        abd_tem = cel_tem.ionAbundance[cel_tem_wave][los]

        # ==============================================
        # Get the ORL temperature from the balmer jump
        # ==============================================
        bj.getEmissivity(tem=tem, n_e=n_e, loc=loc)
        bj.getSkyEmiss(convl=convl, kernel=kernel)
        bj.getSkyTem(skyDen=den_mean, los=los)

        # ==============================================
        # Get the ion abundance from the ORL.
        # Uses CELs estimate for the density.
        # ==============================================
        orl.getEmissivity(tem=tem, n_e=n_e)
        orl.getSkyEmiss(convl=convl, kernel=kernel)
        orl.getIonAbundance(
            skyTem=bj.skyTem,
            skyDen=cel_den.skyDen,
            Hbeta=h1.skyBeta,
            los=los
        )

        # ==============================================
        # Compute diagnostical statistics
        # ==============================================
        data = {
            "CEL_den_abd_avg" : np.nanmean(abd_den),
            "CEL_den_abd_std" : np.nanstd(abd_den, ddof=1),
            "CEL_tem_abd_avg" : np.nanmean(abd_tem),
            "CEL_tem_abd_std" : np.nanstd(abd_tem, ddof=1),
            "BJ_tem_avg"      : np.nanmean(bj.skyTem[los]),
            "BJ_tem_std"      : np.nanstd(bj.skyTem[los], ddof=1),
            "CEL_tem_avg"     : np.nanmean(cel_tem.skyTem[los]),
            "CEL_tem_std"     : np.nanstd(cel_tem.skyTem[los], ddof=1),
            "CEL_den_avg"     : np.nanmean(cel_den.skyDen[los]),
            "CEL_den_std"     : np.nanstd(cel_den.skyDen[los], ddof=1)
        }

        # ==============================================
        # Compute ADF statistics
        # ==============================================
        for i, label in enumerate(orl.wave):

            # ==========================================
            # Abundance estimates
            # ==========================================
            orl_abd = orl.ionAbundance[i][los]

            # ==========================================
            # ADF estimates
            # ==========================================
            adf_den = orl_abd / abd_den
            adf_tem = orl_abd / abd_tem

            # ==========================================
            # ADF statistics
            # ==========================================
            data['ORL_abd_avg_' + label[:4]] = np.nanmean(orl_abd)
            data['ORL_abd_std_' + label[:4]] = np.nanstd(orl_abd, ddof=1)
            data['ADF_den_avg_' + label[:4]] = np.nanmean(adf_den)
            data['ADF_den_std_' + label[:4]] = np.nanstd(adf_den, ddof=1)
            data['ADF_tem_avg_' + label[:4]] = np.nanmean(adf_tem)
            data['ADF_tem_std_' + label[:4]] = np.nanstd(adf_tem, ddof=1)

        df = df.append(data, ignore_index=True)

    # ==================================================
    # Add the indecies
    # ==================================================
    df['gamma'] = gammas

    # ==================================================
    # Save the data as a csv file
    # ==================================================
    if params:
        for key, value in params.items():
            value = str(value)
            ion += '_{:s}_{:s}'.format(key, value.replace('.', ''))

    ion += '.csv'
    df.to_csv(os.path.join(path, ion), index=False)

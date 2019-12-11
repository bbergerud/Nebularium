import sys, os; sys.path.append(os.path.join('..', '..'))
import numpy  as np
import pandas as pd

from nebulous.geom  import sphere
from nebulous.cel   import cel_den_dict, cel_tem_dict
from nebulous.orl   import orl_dict
from nebulous.misc  import fix_params, mkdir
from nebulous.pdf   import pdfs
from nebulous.utils import getDepth

from tqdm import tqdm

# ==================================================
# set the nebula parameters
# ==================================================
dim   = (30,)
loc   = sphere(dim=dim, inRad=0.3, outRad=0.9)
los   = getDepth(loc=loc, dim=dim) > 5
convl = True

# ==================================================
# Function that runs the simulation
# ==================================================
def simul(cel_den, cel_tem, orl, pdf, params, den=1000, kernel=1, grid=100):

    # ==================================================
    # Set params to an empty dictionary if None
    # ==================================================
    if params is None:
        params = {}

    # ==================================================
    # Get the ion type for saving the file
    # ==================================================
    ion = cel_den if cel_den else cel_tem

    # ==================================================
    # Create the grid over the temperature space
    # ==================================================
    tems = np.linspace(5e3, 15e3, grid)

    # ==================================================
    # Grab the appropriate ion diagnostics
    # ==================================================
    cel_tem = cel_tem_dict[cel_tem]
    cel_den = cel_den_dict[cel_den] if cel_den else None
    orl = orl_dict[orl]
    h1  = orl_dict['HI']
    bj  = orl_dict['BJ']

    # ==================================================
    # Create a data frame to hold the values
    # ==================================================
    df = pd.DataFrame()

    # ==================================================
    # Iterate through each value in the temperatures grid
    # ==================================================
    print("\nPDF={:s}, Ion={:s}, Args={:}".format(pdf, ion, params))

    for x in tqdm(tems):

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
        # Generate the H-beta intensities
        # ==============================================
        h1.getEmissivity(tem=tem, n_e=den)
        h1.getSkyEmiss(convl=convl, kernel=kernel)

        # ==============================================
        # Get the temperature estimate from the CELs
        # ==============================================
        cel_tem.getEmissivity(tem=tem, n_e=den, loc=loc)
        cel_tem.getSkyEmiss(convl=convl, kernel=kernel)
        cel_tem.getSkyTem(skyDen=den)

        # ==============================================
        # Get the abundance estimate; if a density
        # sensitive CEL is passed, then use this
        # to get the ion abundance estimate
        # *** Estimating the density has little impact,
        # other than increasing the computation time ***
        # ==============================================
        if cel_den:
            cel_den.getEmissivity(tem=tem, n_e=den, loc=loc)
            cel_den.getSkyEmiss(convl=convl, kernel=kernel)
            cel_den.getIonAbundance(skyTem=cel_tem.skyTem, skyDen=den, Hbeta=h1.skyBeta, los=los)
            cel_abd = cel_den.ionAbundance[0][los]
        else:
            cel_tem.getIonAbundance(skyTem=cel_tem.skyTem, skyDen=den, Hbeta=h1.skyBeta, los=los)
            cel_abd = cel_tem.ionAbundance[0][los]

        # ==============================================
        # Get the ORL temperature from the balmer jump
        # ==============================================
        bj.getEmissivity(tem=tem, n_e=den, loc=loc)
        bj.getSkyEmiss(convl=convl, kernel=kernel)
        bj.getSkyTem(skyDen=den)

        # ==============================================
        # Get the ion abundance from the ORL using the
        # Balmer jump as the temperature estimate.
        # (Using CEL density estimate has little impact,
        # other than an increased computational cost)
        # ==============================================
        orl.getEmissivity(tem=tem, n_e=den)
        orl.getSkyEmiss(convl=convl, kernel=kernel)
        orl.getIonAbundance(skyTem=bj.skyTem, skyDen=den, Hbeta=h1.skyBeta, los=los)

        # ==============================================
        # Compute the ADF values and store the results
        # ==============================================
        data = {
            "CEL_adf_avg" : np.nanmean(cel_abd),
            "CEL_adf_std" : np.nanstd(cel_abd, ddof=1),
            "BJ_tem_avg"  : np.nanmean(bj.skyTem[los]),
            "BJ_tem_std"  : np.nanstd(bj.skyTem[los], ddof=1),
            "CEL_tem_avg" : np.nanmean(cel_tem.skyTem[los]),
            "CEL_tem_std" : np.nanstd(cel_tem.skyTem[los], ddof=1)
        }

        for i, label in enumerate(orl.wave):

            wave = label[:4]
            orl_abd = orl.ionAbundance[i][los]
            adf = orl_abd / cel_abd

            data['ORL_abd_avg_' + wave] = np.nanmean(orl_abd)
            data['ORL_abd_std_' + wave] = np.nanstd(orl_abd, ddof=1)
            data['ADF_avg_' + wave] = np.nanmean(adf)
            data['ADF_std_' + wave] = np.nanstd(adf, ddof=1)


        df = df.append(data, ignore_index=True)

    # ==================================================
    # Add the temperature values to the data frame
    # ==================================================
    df['tem'] = tems

    # ==================================================
    # Set the path for saving the file
    # ==================================================
    path = os.path.join(
        '..', '..', 'data', 'tem', 'adf', pdf,
        'N_{:d}'.format(int(den))
    )
    mkdir(path)

    # ==================================================
    # Save the data as a csv file
    # ==================================================
    ion += '_den' if cel_den else '_tem'

    if params:
        for key, value in params.items():
            value = str(value)
            ion += '_{:s}_{:s}'.format(key, value.replace('.', ''))

    ion += '.csv'
    df.to_csv(os.path.join(path, ion), index=False)

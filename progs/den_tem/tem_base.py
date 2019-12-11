import sys, os; sys.path.append(os.path.join('..', '..'))
import numpy  as np
import pandas as pd

from nebulous.geom  import sphere
from nebulous.cel   import cel_tem_dict
from nebulous.orl   import orl_dict
from nebulous.pdf   import pdfs
from nebulous.utils import getDepth
from nebulous.misc  import fix_params, mkdir

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
def simul(ion, pdf, params, tem_mean, den_mean, grid=25, convl=True, kernel=1):

    # ==================================================
    # Grab the appropriate diagnostic
    # ==================================================
    if ion in cel_tem_dict.keys():
        ion_tem = cel_tem_dict[ion]
    elif ion == 'BJ':
        ion_tem = orl_dict[ion]
    else:
        print('Not an available diagnostic. Exiting.')
        sys.exit(1)

    # ==================================================
    # Set params to an empty dictionary if no values are passed
    # ==================================================
    if params is None:
        params = {}

    # ==================================================
    # Create the grid over the index space
    # ==================================================
    gammas = np.linspace(0, 2, grid)

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
    # Create a data frame to hold the values
    # ==================================================
    df = pd.DataFrame()

    # ==================================================
    # Iterate through each value in the index grid
    # ==================================================
    print
    for index in gammas:

        # ==================================================
        # Print out the current status
        # ==================================================
        print("PDF = {:s}, Ion = {:s}, Index = {:.2f}, Params = {}".format(pdf, ion, index, params))

        # ==================================================
        # Generate the temperature distribution
        # ==================================================
        tem = pdfs['polytrope'](cube=n_e, index=index, mean=tem_mean, geom=False, loc=loc)

        # ==============================================
        # Get the temperature estimate
        # ==============================================
        ion_tem.getEmissivity(tem=tem, n_e=n_e, loc=loc)
        ion_tem.getSkyEmiss(convl=convl, kernel=kernel)
        ion_tem.getSkyTem(skyDen=den_mean)

        # ==============================================
        # Store the temperature estimate
        # ==============================================
        data = {
            'tem_avg': np.nanmean(ion_tem.skyTem[los]),
            'tem_std': np.nanstd(ion_tem.skyTem[los], ddof=1)
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
        '..', '..', 'data', 'den_tem', 'tem', pdf,
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

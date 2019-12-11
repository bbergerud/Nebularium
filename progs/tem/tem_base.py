"""

"""

import sys, os; sys.path.append(os.path.join('..', '..'))
import numpy  as np
import pandas as pd

from nebulous.geom  import sphere
from nebulous.cel   import cel_tem_dict
from nebulous.orl   import orl_dict
from nebulous.pdf   import pdfs
from nebulous.misc  import fix_params, mkdir
from nebulous.utils import getDepth

# ==================================================
# Set the nebula parameters
# ==================================================
dim   = (30,30,30)
loc   = sphere(dim=dim, inRad=0.3, outRad=0.9)
los   = getDepth(loc=loc, dim=dim) > 5
convl = True

# ==================================================
# Function that runs the simulation
# ==================================================
def simul(ion, pdf, params, den=1e3, kernel=1, grid=100):

    # ==================================================
    # Set params to an empty dictionary if None
    # ==================================================
    if params is None:
        params = {}

    # ==================================================
    # Grab the appropriate ions
    # ==================================================
    if ion in cel_tem_dict.keys():
        ion_tem = cel_tem_dict[ion]
    elif ion in orl_dict.keys():
        ion_tem = orl_dict[ion]
    else:
        print("Not an available ion. Exiting.\n")
        sys.exit(1)

    # ==================================================
    # Create the grid over the temperature space
    # ==================================================
    tems = np.linspace(5e3, 15e3, grid)

    # ==================================================
    # Create a data frame to hold the values
    # ==================================================
    df = pd.DataFrame()

    # ==================================================
    # Iterate through each value in the temperatures grid
    # ==================================================
    for x in tems:

        # ==================================================
        # If there is a normal distribution of temperatures,
        # then use <sigma> * <x> for the standard deviation.
        # ==================================================
        p = fix_params(params=params, pdf=pdf, x=x)

        # ==================================================
        # Generate the temperature distribution
        # ==================================================
        tem = pdfs[pdf](dim=dim, loc=loc, mean=x, **p)

        # ==================================================
        # Get the emissivities and temperature estimate
        # ==================================================
        ion_tem.getEmissivity(tem=tem, n_e=den, loc=loc)
        ion_tem.getSkyEmiss(convl=convl, kernel=kernel)
        ion_tem.getSkyTem(skyDen=den)

        # ==================================================
        # Store the values
        # ==================================================
        data = {
            'tem_avg': np.nanmean(ion_tem.skyTem[los]),
            'tem_std': np.nanstd(ion_tem.skyTem[los], ddof=1)
        }

        df = df.append(data, ignore_index=True)

    # ==================================================
    # Add the temperatures
    # ==================================================
    df['tem'] = tems

    # ==================================================
    # Set the path for saving the file
    # ==================================================
    path = os.path.join(
        '..', '..', 'data', 'tem', 'tem', pdf,
        'N_{:d}'.format(int(den))
    )
    mkdir(path)

    # ==================================================
    # Save the data as a csv file
    # ==================================================
    ion += '_tem'

    if params:
        for key, value in params.items():
            value = str(value)
            ion += '_{:s}_{:s}'.format(key, value.replace('.', ''))

    ion += '.csv'
    df.to_csv(os.path.join(path, ion), index=False)

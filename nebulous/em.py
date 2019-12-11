import numpy as np
from .utils import convl2D, getDepthTrue

def getEM(n_e, tem=None, skyTem=None, geomTem=False, depth=None, convl=True, kernel=1):
    """
    Computes the emission measure given a cube of elecron densities
    <n_e> and temperatures <tem>.

    Parameters:
        n_e                 3D density array
        tem                 3D temperture array if temperature fluctuations
        skyTem              2D array of temperatuers along LOS
        geomTem             use the geometric temperature
        depth               depth along the line of sight
        convl               boolean to apply gaussian filter
        kernel              convolution kernel in standard deviations

    Returns:
        EM                  2D array of emission measures on the sky
    """
    # ==================================================
    # Constant nebular temperature
    # ==================================================
    if not isinstance(tem, np.ndarray):
        EM = np.sum(n_e**2, axis=-1)

    # ==================================================
    # Temperature fluctuations
    # ==================================================
    else:
        # ==============================================
        # Compute T^-0.5
        # ==============================================
        loc = np.where(tem > 0)
        sqrt_t_inv = np.zeros_like(tem)
        sqrt_t_inv[loc] = 1. / np.sqrt(tem[loc])

        # ==============================================
        # Estimate temperature along the line of sight
        # if the skyTem is not passed as an argument.
        # ==============================================
        if not isinstance(skyTem, (float, int, np.ndarray)):

            # =========================================
            # Get LOS depth if none is passed
            # =========================================
            if isinstance(depth, (int, float, type(None))):
                depth = getDepthTrue(tem)

            # =========================================
            # Create an array to hold the temperatures
            # estimated along the line of sights
            # =========================================
            skyTem = np.zeros_like(depth)
            los = depth > 0

            # =========================================
            # Define the temperature functions
            # =========================================
            def geom_tem(tem):
                tem_sum = np.sum(tem, axis=-1)
                skyTem[los] = tem_sum[los] / depth[los]
                return skyTem

            def mean_tem(tem, n_e):
                den_sum = np.sum(n_e, axis=-1)
                den_tem_sum = np.sum(n_e*tem, axis=-1)
                skyTem[los] = den_tem_sum[los] / den_sum[los]
                return skyTem

            # =========================================
            # Use the appropriate temperature estimate
            # =========================================
            if geomTem:
                skyTem = geom_tem(tem)
            else:
                if isinstance(n_e, np.ndarray):
                    skyTem = mean_tem(tem=tem, n_e=n_e)
                else:
                    skyTem = geom_tem(tem)

            # =========================================
            # Evaluate the emission measure.
            # =========================================
            EM = np.sum(n_e**2 * sqrt_t_inv, axis=-1) * np.sqrt(skyTem)

        else:
            # ==============================================
            # Emission measure; since the temperature are
            # assumed post-convolving, the temperature
            # adjustment comes at the end
            # ==============================================
            EM = np.sum(n_e**2 * sqrt_t_inv, axis=-1)
            if convl:
                EM = convl2D(EM, kernel)
            return EM * np.sqrt(skyTem)

    return convl2D(EM, kernel) if convl else EM

def getSkyDenEM(EM, depth, depthMin=0):
    """
    Returns the density estimate given the observed emission
    measure and the depth along the line of sight.

    Parameters:
        EM          emission measure
        depth       cell depth along each line of sight
        depthMin    minimum cell depth to compute the emission measure

    Returns:
        skyDen      2D array of density esimates on the sky
    """
    # ==================================================
    # Find lines of sight with sufficient depth
    # ==================================================
    los = depth > depthMin

    # ==================================================
    # Estimate density, n_{e} ~ sqrt(EM / L)
    # ==================================================
    skyDen = np.zeros_like(depth, dtype='float')
    skyDen[los] = np.sqrt(EM[los] / depth[los])

    return skyDen

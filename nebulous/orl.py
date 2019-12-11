import pyneb as pn, sys
import numpy as np
from scipy.interpolate import interp1d
from .ion import ion
from .utils import convl2D

class ORL(ion):

    def __init__(self, atom, ion, wave_label):

        if not isinstance(wave_label, tuple):
            if isinstance(wave_label, list):
                wave_label = tuple(wave_label)
            else:
                wave_label = tuple([wave_label])

        self.wave = wave_label
        self.atom = pn.RecAtom(atom, ion)

    def getEmissivity(self, tem, n_e, n_i=None, loc=None):
        super(ORL,self).getEmissivity(wave_param='label',
            tem=tem, n_e=n_e, n_i=n_i, loc=loc)

    def getSkyEmiss(self, convl, kernel=1):
        super(ORL,self).getSkyEmiss(convl=convl, kernel=kernel)

    def getIonAbundance(self, skyTem, skyDen, Hbeta, los=None):
        super(ORL,self).getIonAbundance(skyTem=skyTem, skyDen=skyDen,
            Hbeta=Hbeta, los=los, wave_param = "label")


class HI(ORL):
    def __init__(self):
        super(HI,self).__init__(atom='H', ion=1, wave_label = ("4_2",))

    def getEmissivity(self, tem, n_e, loc=None):
        super(HI, self).getEmissivity(tem=tem, n_e=n_e, n_i=n_e, loc=loc)
        self.jBeta = self.emiss[0]

    def getSkyEmiss(self, convl=True, kernel=1):
        super(HI, self).getSkyEmiss(convl=convl, kernel=kernel)
        self.skyBeta = self.skyEmiss[0]


class OII(ORL):
    def __init__(self):
        super(OII,self).__init__(atom='O', ion=2, wave_label = ('4089.29', '4638.86', '4641.81', '4649.13'))

    def getEmissivity(self, tem, n_e, n_i=None, loc=None):
        super(OII, self).getEmissivity(tem=tem, n_e=n_e, n_i=n_i, loc=loc)

    def getSkyEmiss(self, convl=True, kernel=1):
        super(OII,self).getSkyEmiss(convl=convl, kernel=kernel)



# ============================================================
# Balmer Jump for ORL temperature determination
# ============================================================

class BJ(ORL):
    def __init__(self, transition="11_2"):
        super(BJ,self).__init__(atom='H', ion=1, wave_label = (transition,))

    def getEmissivity(self, tem, n_e, loc=None):
        super(BJ, self).getEmissivity(tem=tem, n_e=n_e, n_i=n_e, loc=loc)
        self.__getBalmerEmissivity(tem=tem, n_e=n_e, loc=loc)

    def getSkyEmiss(self, convl=True, kernel=1):
        super(BJ, self).getSkyEmiss(convl=convl, kernel=kernel)
        self.__getSkyBalmer(convl=convl, kernel=kernel)

    def getSkyTem(self, skyDen=1000, los=None, **kwargs):
        if isinstance(los, type(None)):
            los = self.skyEmiss[0] > 0
        if isinstance(skyDen, np.ndarray):
            skyDen = skyDen[los]

        # ======================================================
        # Compute the ratio of the balmer jump to the
        # recombination line strength.
        # ======================================================
        ratio = self.skyBJ[los] / self.skyEmiss[0][los]

        # ======================================================
        # If the electron density is passed as an array,
        # then use the 2D spline to estimate the temperature;
        # else use the 1D spline.
        # ======================================================
        if isinstance(skyDen, np.ndarray):
            print('<skyDen> must be a single value, not an array.' )
            sys.exit(1)
        else:
            tem_func = self.spline1D(den=skyDen, **kwargs)
            tems = tem_func(ratio)

        temBJ = np.zeros_like(self.skyBJ)
        temBJ[los] = tems
        self.skyTem = temBJ

    # ======================================================
    # Emissivity and sky intensity of balmer jump
    # ======================================================
    def __getBalmerEmissivity(self, tem, n_e, loc=None):

        # ==================================================
        # Determine the cube size; if <loc> is not passed,
        # then find the cells that have non-zero values.
        # ==================================================
        if isinstance(n_e, np.ndarray):
            emiss = np.zeros_like(n_e)
            if isinstance(loc, type(None)):
                loc = n_e > 0
        elif isinstance(tem, np.ndarray):
            emiss = np.zeros_like(tem)
            if isinstance(loc, type(None)):
                loc = tem > 0
        else:
            print("n_e or tem must be an array")
            sys.exit(1)

        # ==================================================
        # Compute the "emission" of the balmer jump.
        # The density dependence goes as n_e^2
        # The temperature dependence goes as T^(-3/2)
        # ==================================================
        if isinstance(n_e, np.ndarray):
            emiss[loc] = n_e[loc]**2
        else:
            emiss[loc] = n_e**2

        if isinstance(tem, np.ndarray):
            emiss[loc] *= tem[loc]**(-1.5)
        else:
            emiss[loc] *= tem**(-1.5)

        # ==================================================
        # Store the emission array
        # ==================================================
        self.BJ = emiss

    def __getSkyBalmer(self, convl=True, kernel=1):
        skyBJ = np.sum(self.BJ, axis=-1)
        if convl:
            skyBJ = convl2D(skyBJ, kernel)
        self.skyBJ = skyBJ

    # ======================================================
    # Splines for estimating the temperature from the
    # observed ratio and the estimated density
    # ======================================================

    def spline1D(self, den, kind='slinear', grid=1000):
        """
        Uses a 1D spline to create a function that will return the
        temperature given the observed ratio of the balmer strength
        to the strength of the H11-2 line at a given density.

        Parameters:
            den         Electron density to evaluate at (cm^3)
            kind        Kind of interpolation to use
            grid        Linear grid spacing for temperatures
        """
        # ===================================================
        # Create a grid over the temperature range.
        # The range of values over which PyNeb works is given
        # ===================================================
        tems = np.linspace(500, 30e3, grid)

        # ===================================================
        # Compute the ratio of the balmer jump strength to the
        # strength of the H 11-2 line.
        #   Note that both strengths have an n_e^2 dependence,
        # which cancels out.
        # ===================================================
        j_H  = self.atom.getEmissivity(tem=tems, den=den, label=self.wave[0])
        j_BJ = tems**(-1.5)
        ratio = j_BJ / j_H

        # ===================================================
        # Perform an interpolation of the ratio and temperature
        # to create a function that will compute the temperature
        # given a ratio.
        # ===================================================
        tem_func = interp1d(ratio, tems, kind=kind, fill_value='extrapolate')

        # ===================================================
        # Return the temperature function
        # ===================================================
        return tem_func




# ==========================================

orl_dict = {
    'HI'  : HI(),
    'OII' : OII(),
    'BJ'  : BJ()
}

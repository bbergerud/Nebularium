from  .ion   import ion
from  .utils import convl2D
import pyneb as pn
import numpy as np

class CEL(ion):
    def __init__(self, atom, ion, wave):

        if not isinstance(wave, tuple):
            if isinstance(wave, list):
                wave = tuple(wave)
            else:
                wave = tuple([wave])

        self.wave = wave
        self.atom = pn.Atom(atom, ion)

    def getEmissivity(self, tem, n_e, n_i=None, loc=None):
        super(CEL, self).getEmissivity(wave_param="wave",
            tem=tem, n_e=n_e, n_i=n_i, loc=loc)

    def getTemDen(self, func=None, skyTem=None, skyDen=None, to_eval=None, los=None):
        """
        Computes the temperature or density.
        """
        # ============================================================
        # Default temperature and density values
        # ============================================================
        default_density = 1e3
        default_temperature = 10e3

        # ============================================================
        # Get the atom type, the wavelengths, and the emission (intensity)
        # observed along the line of sight.
        # ============================================================
        atom = self.atom
        wave = self.wave
        skyEmiss = self.skyEmiss

        # ============================================================
        # If no function is passed to combine the observed intensities
        # then use a default one. The temperature sensitive lines are
        # assumed to contain three lines, while the density sensitive
        # ones are assumed to contain only two lines.
        # ============================================================
        if not callable(func):
            if len(wave) == 3:
                func = lambda x,y,z: (x+y)/z
            else:
                func = lambda x,y: x/y

        # ============================================================
        # If no lines of sight <los> are passed, use the lines
        # of sight with non-zero emission
        # ============================================================
        if isinstance(los, type(None)):
            los = np.where(skyEmiss[1] > 0)

        # ============================================================
        # Get the line intensities for each line of sight
        # ============================================================
        lineIntensity = []
        for i, _ in enumerate(wave):
            lineIntensity.append(skyEmiss[i][los])
        lineIntensity = tuple(lineIntensity)

        # ============================================================
        # Compute the line ratio defined by the function.
        # ============================================================
        lineRatio = func(*lineIntensity)

        # ============================================================
        # Estimate the temperature if there are three wavelengths
        # ============================================================
        if len(wave) == 3:

            # ========================================================
            # If no electron density (skyDen) is passed, use the
            # default value
            # ========================================================
            if isinstance(skyDen, type(None)):
                skyDen = default_density

            # ========================================================
            # If an array respresenting the electron density across
            # the sky is passed, extract the densities for each LoS.
            # ========================================================
            if isinstance(skyDen, np.ndarray):
                skyDen = skyDen[los]

            # ========================================================
            # If no evaluation function was passed, add the intensities
            # of the first two lines and divided by the intensity of the
            # last line.
            # ========================================================
            if isinstance(to_eval, type(None)):
                to_eval = "(L({:d}) + L({:d})) / L({:d})".format(*wave)

            # ========================================================
            # Create an array to hold the temperature estimates on the
            # sky. Insert temperature estimates for each line of sight.
            # ========================================================
            skyTem = np.zeros_like(skyEmiss[0])
            skyTem[los] = atom.getTemDen(
                int_ratio = lineRatio,          # Intensity ratio
                den=skyDen,                     # Electron densities
                to_eval=to_eval                 # Line ratio function
            )

            self.skyTem = skyTem

        # ============================================================
        # Estimate the density if there are two wavelengths
        # ============================================================
        else:
            # ========================================================
            # If no temperature was input, use the default value
            # ========================================================
            if isinstance(skyTem, type(None)):
                skyTem = default_temperature

            # ========================================================
            # If a sky map of the temperatures was passed, extract
            # the values associated with each line of sight.
            # ========================================================
            if isinstance(skyTem, np.ndarray):
                skyTem = skyTem[los]

            # ========================================================
            # Create an array to hold the density estimates on the sky
            # Insert the density estimates for each line of sight.
            # ========================================================
            skyDen = np.zeros_like(skyEmiss[0])
            skyDen[los] = atom.getTemDen(
                int_ratio = lineRatio,
                tem=skyTem,
                wave1=wave[0],
                wave2=wave[1]
            )

            self.skyDen = skyDen

    def getIonAbundance(self, skyTem, skyDen, Hbeta, los=None):
        """
        Estimate the ionic abundances relative to hydrogen.

        Parameters:
            skyTem             Temperatures
            skyDen             Electron densities
            Hbeta           H-beta intensity on sky
            los             lines of sight
        """
        super(CEL,self).getIonAbundance(
            skyTem=skyTem,
            skyDen=skyDen,
            Hbeta=Hbeta,
            los=los,
            wave_param = "wave"
        )

class ArIV_den(CEL):
    def __init__(self):
        super(ArIV_den, self).__init__(atom='Ar', ion=4, wave = (4711, 4740))

    def getSkyDen(self, skyTem=10e3, los=None):
        self.getTemDen(skyTem=skyTem, func=lambda x,y: x/y, los=los)

class ArIII_tem(CEL):
    def __init__(self):
        super(ArIII_tem, self).__init__(atom='Ar', ion=3, wave=(7136, 7751, 5192))

    def getSkyTem(self, skyDen=1000):
        self.getTemDen(skyDen=skyDen, func=lambda x,y,z: (x+y)/z)

class CII_den(CEL):
    def __init__(self):
        super(CII_den, self).__init__(atom = 'C', ion=2, wave=(2328, 2326))

    def getSkyDen(self, skyTem=10e3):
        self.getTemDen(skyTem=skyTem, func=lambda x,y: x/y)

class CIII_den(CEL):
    def __init__(self):
        super(CIII_den, self).__init__(atom = 'C', ion=3, wave=(1907,1909))

    def getSkyDen(self, skyTem=10e3):
        self.getTemDen(skyTem=skyTem, func=lambda x,y: x/y)

class ClIII_den(CEL):
    def __init__(self):
        super(ClIII_den,self).__init__(atom='Cl', ion=3, wave=(5518,5538))

    def getSkyDen(self, skyTem=10e3):
        self.getTemDen(skyTem=skyTem, func=lambda x,y: x/y)

class ClIV_tem(CEL):
    def __init__(self):
        super(ClIV_tem, self).__init__(atom='Cl', ion=4, wave=(7530, 8045, 5323))

    def getSkyTem(self, skyDen=1000):
        self.getTemDen(skyDen=skyDen, func=lambda x,y,z: (x+y)/z)


class KV_den(CEL):
    def __init__(self):
        super(KV_den,self).__init__(atom='K', ion=5, wave=(4123, 4163))

    def getSkyDen(self, skyTem=10e3):
        self.getTemDen(skyTem=skyTem, func=lambda x,y: x/y)


class NI_den(CEL):
    def __init__(self):
        super(NI_den,self).__init__(atom='N', ion=1, wave = (5198, 5200))

    def getSkyDen(self, skyTem=10e3):
        self.getTemDen(skyTem=skyTem, func=lambda x,y: x/y)

class NIII_den(CEL):
    def __init__(self):
        super(NIII_den,self).__init__(atom='N', ion=3, wave = (1749,1752))

    def getSkyDen(self, skyTem=10e3):
        self.getTemDen(skyTem=skyTem, func=lambda x,y: x/y)

class NII_tem(CEL):
    def __init__(self):
        super(NII_tem,self).__init__(atom='N', ion=2, wave = (6548, 6584, 5754))

    def getSkyTem(self, skyDen=1000):
        self.getTemDen(skyDen=skyDen, func=lambda x,y,z: (x+y)/z)

class NeIII_tem(CEL):
    def __init__(self):
        super(NeIII_tem,self).__init__(atom='Ne', ion=3, wave = (3869, 3968, 3343))

    def getSkyTem(self, skyDen=1000):
        self.getTemDen(skyDen=skyDen, func=lambda x,y,z: (x+y)/z)

class NeIV_den(CEL):
    def __init__(self):
        super(NeIV_den,self).__init__(atom='Ne', ion=4, wave = (2425, 2423))

    def getSkyDen(self, skyTem=10e3, los=None):
        self.getTemDen(skyTem=skyTem, los=los, func=lambda x,y: x/y)

class OII_den(CEL):
    def __init__(self):
        super(OII_den,self).__init__(atom='O', ion=2, wave = (3729, 3726))

    def getSkyDen(self, skyTem=10e3, los=None):
        self.getTemDen(skyTem=skyTem, los=los, func=lambda x,y: x/y)

class OIII_den(CEL):
    def __init__(self):
        super(OIII_den,self).__init__(atom='O', ion=3, wave = (88.36e4, 51.81e4))

    def getSkyDen(self, skyTem=10e3, los=None):
        self.getTemDen(skyTem=skyTem, los=los, func=lambda x,y: x/y)

class OIII_tem(CEL):
    def __init__(self):
        super(OIII_tem,self).__init__(atom='O', ion=3, wave = (5007, 4959, 4363))

    def getSkyTem(self, skyDen=1000, los=None):
        self.getTemDen(skyDen=skyDen, los=los, func=lambda x,y,z: (x+y)/z)

class OIV_den(CEL):
    def __init__(self):
        super(OIV_den,self).__init__(atom='O', ion=4, wave = (1405,1401))

    def getSkyDen(self, skyTem=10e3, los=None):
        self.getTemDen(skyTem=skyTem, los=los, func=lambda x,y: x/y)

class SII_den(CEL):
    def __init__(self):
        super(SII_den,self).__init__(atom='S', ion=2, wave = (6716, 6731))

    def getSkyDen(self, skyTem=10e3):
        self.getTemDen(skyTem=skyTem, func=lambda x,y: x/y)

class SIII_tem(CEL):
    def __init__(self):
        super(SIII_tem,self).__init__(atom='S', ion=3, wave = (9531, 9069, 6312))

    def getSkyTem(self, skyDen=1000):
        self.getTemDen(skyDen=skyDen, func=lambda x,y,z: (x+y)/z)


class SiIII_den(CEL):
    def __init__(self):
        super(SiIII_den,self).__init__(atom='Si', ion=3, wave = (1883, 1892))

    def getSkyDen(self, skyTem=10e3):
        self.getTemDen(skyTem=skyTem, func=lambda x,y: x/y)



# =======================================================
# Dictionaries for CELs
# =======================================================
cel_den_dict = {
    'ArIV' : ArIV_den(),
    'CIII' : CIII_den(),
    'ClIII': ClIII_den(),
    'KV'   : KV_den(),
    'NI'   : NI_den(),
    'NIII' : NIII_den(),
    'NeIV' : NeIV_den(),
    'OII'  : OII_den(),
    'OIII' : OIII_den(),
    'OIV'  : OIV_den(),
    'SII'  : SII_den(),
    'SiIII': SiIII_den()
}

cel_tem_dict = {
    'ArIII' : ArIII_tem(),
    'ClIV'  : ClIV_tem(),
    'NII'   : NII_tem(),
    'NeIII' : NeIII_tem(),
    'OIII'  : OIII_tem(),
    'SIII'  : SIII_tem()
}

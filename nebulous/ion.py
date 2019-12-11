from .utils import convl2D
import numpy as np
import sys

class ion:

    def getLatexSymbol(self, delim='\;'):
        roman = {
            1: 'i',
            2: 'ii',
            3: 'iii',
            4: 'iv',
            5: 'v',
            6: 'vi'
        }

        #latex = r'$\rm \left[{:s} \; {:s}\right]$'.format(
        #        self.atom.elem, roman[self.atom.spec])

        latex = r'$\mathrm{' + self.atom.elem + '}' + delim \
              + r'\textsc{' + roman[self.atom.spec] + r'}$'

        return latex

    def getEmissivity(self, wave_param, tem, n_e, n_i=None, loc=None):
        """
        Computes the volume emissivities for each cell at each
        wavelengths and stores in the variable <self.emiss>

        Parameters:
            wave_param      indicator of self.wave values {"wave", "label"}
            tem             temperature(s)
            n_e             electron densit(y/ies)
            n_i             ion densit(y/ies)
            loc             cell locations within the nebula
        """
        # =============================================================
        # Extract the PyNeb atom class as well as the wavelength values
        # and the ionization state
        # =============================================================
        atom = self.atom
        wave = self.wave

        # =============================================================
        # Test to see if the density and/or temperatures are
        # stored as arrays.
        # =============================================================
        logical1 = isinstance(n_e, np.ndarray)
        logical2 = isinstance(tem, np.ndarray)
        logical3 = isinstance(n_i, np.ndarray)

        # =============================================================
        # If none of the inputs are arrays, then issue a warning and abort.
        # =============================================================
        if not (logical1 or logical2 or logical3):
            print("<tem>, <n_e>, or <n_i> must be an array")
            sys.exit(1)

        # -------------------------------------------------------------

        # =============================================================
        # If the electron density is stored as an array, then proceed
        # =============================================================
        if logical1:

            # =========================================================
            # Check if <loc> has been set. If not, then select the cells
            # with non-zero densities.
            # =========================================================
            if isinstance(loc, type(None)):
                loc = np.where(n_e > 0)

            # =========================================================
            # Create an array to hold the emissivities associated with each cell
            # =========================================================
            emiss = np.zeros((len(wave), *n_e.shape))

            # =========================================================
            # Extract the densities
            # =========================================================
            n_e = n_e[loc]

        # =============================================================
        # If the temperature has been stored as an array, then proceed
        # =============================================================
        if logical2:

            # =========================================================
            # Test if <loc> has been set. If not, then select the cells
            # that have non-zero temperatures.
            # =========================================================
            if isinstance(loc, type(None)):
                loc = np.where(tem > 0)

            # =========================================================
            # Test to see if an array has been created to hold the
            # emissivities (see first if). If not, then make.
            # =========================================================
            try: emiss
            except: emiss = np.zeros((len(wave), *tem.shape))

            # =========================================================
            # Extract the temperatures
            # =========================================================
            tem = tem[loc]

        # =============================================================
        # If the ion density is stored as an array, then proceed
        # =============================================================
        if logical3:

            # =========================================================
            # Check if <loc> has been set. IF not, then select the cells
            # with non-zero densities.
            # =========================================================
            if isinstance(loc, type(None)):
                loc = np.where(n_i > 0)

            # =========================================================
            # Test to see if an array has been created to hold the
            # emissivities (see first if). If not, then make.
            # =========================================================
            try: emiss
            except: emiss = np.zeros((len(wave), *n_i.shape))

            # =========================================================
            # Extract the densities
            # =========================================================
            n_i = n_i[loc]

        # =============================================================
        # If no ion densities have been supplied, then assume that
        # the ion density is proportional to the electron density
        # (?) Apply an ionization correction via the Saha equation (?)
        # =============================================================
        if isinstance(n_i, type(None)):
            n_i = n_e

            """
            ion_frac = saha(
                elem=self.atom.elem,
                tem=tem,
                n_e=n_e,
                ion=self.atom.spec+1 if self.atom.type == 'rec' else self.atom.spec,
                only_ions=False if self.atom.spec == 1 else True
            )

            n_i = n_e * ion_frac
            """

        # =============================================================
        # Create a dictionary for passing to the getEmissivity function.
        # If the electron densities and temperatures are both arrays,
        # then set the product term to false (as each cell is paired)
        # =============================================================
        params = {
            "tem": tem,
            "den": n_e,
            "product": False if (logical1 and logical2) else True
        }

        # =============================================================
        # For each wave, update the dictionary and compute the line intensity
        # by multiplying the emissivity by the electron and ion densities.
        # =============================================================
        for i, wl in enumerate(wave):
            params[wave_param] = wl
            emiss[i][loc] = atom.getEmissivity(**params) * n_e * n_i

        # =============================================================
        # Store the result.
        # =============================================================
        self.emiss = emiss


    def getSkyEmiss(self, convl=True, kernel=1):
        """
        Computes the line instensity alone a line of sight and
        stores in the variable <self.skyEmiss>

        Parameters:
            convl       boolean to convole the intensity image
            kernel      gaussian filter kernel value
        """
        emiss = self.emiss
        wave = self.wave

        # Create an array to hold the intensity values as observed
        # on the sky.
        dim = np.shape(emiss)[1:-1]
        skyEmiss = np.zeros((len(wave), *dim))

        # For each wavelength, compute the intensity by summing along
        # the line of sight. Option to convolve the image with a
        # gaussian filter.
        for i, _ in enumerate(wave):
            emission = np.nansum(self.emiss[i], axis=-1)
            skyEmiss[i] = convl2D(emission, kernel) if convl else emission

        self.skyEmiss = skyEmiss

    def getIonAbundance(self, skyTem, skyDen, Hbeta, los, wave_param):
        """
        Computes the abudance estimates given the density and
        temperature along each line of sight and stores in the
        variable <self.ionAbundance>

        To call:
            getIonAbundance(skyTem, skyDen, Hbeta, los, wave_param)

        Parameters:
            skyTem          temperature estimates
            skyDen          density estimates
            Hbeta           H-beta intensities
            los             light of sight positions
            wave_param
        """
        # ================================================
        # If no line of sight positions have been passed,
        # use the lines of sight with non-zero H-beta
        # intensities.
        # ================================================
        if isinstance(los, type(None)):
            los = Hbeta > 0

        # ================================================
        # Extract the temperatures and densities along
        # the line of sights.
        # ================================================
        if isinstance(skyDen, np.ndarray):
            skyDen = skyDen[los]
        if isinstance(skyTem, np.ndarray):
            skyTem = skyTem[los]

        # ================================================
        # If either the temperature of density are constant,
        # create an array that is the same length as the
        # other.
        # ================================================
        if isinstance(skyDen, (int, float)):
            skyDen = np.repeat(skyDen, len(skyTem))
        if isinstance(skyTem, (int, float)):
            skyTem = np.repeat(skyTem, len(skyDen))

        params = {
            "den": skyDen,
            "tem": skyTem,
        }

        ionDen = np.zeros_like(self.skyEmiss)
        for i, sky in enumerate(self.skyEmiss):
            lr = 100*sky[los] / Hbeta[los]
            params["int_ratio"] = lr
            params[wave_param] = self.wave[i]
            ionDen[i][los] = self.atom.getIonAbundance(**params)

        self.ionAbundance = ionDen

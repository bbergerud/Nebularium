from .utils import makeCube, getCoordinates, getRadialDistance
from scipy.stats import beta, expon, lognorm, powerlognorm
import numpy as np, sys

def beta(dim, loc, mean, alpha, beta, seed=82921):
    """
    Fills cells at <loc> with numbers sampled from the beta distribution
    with <mu=mean> and parameters <alpha> and <beta>; returns the cube.

    Parameters:
        dim         cube dimensions {tuple}
        loc         array containing cells representing the nebula {np.ndarray}
        mean        mean value {float}
        alpha       parameter value {float > 0}
        beta        parameter value {float > 0}
        seed        random number seed {int}

    Returns:
        cube        cube containing random values {3D array}
    """

    # ==========================================================
    # Make sure <alpha> and <beta> are valid.
    # ==========================================================
    if (alpha <= 0) | (beta <= 0):
        print('<alpha> and <beta> must both be greater than zero.')
        sys.exit(1)

    # ==========================================================
    # Set the random number seed
    # ==========================================================
    np.random.seed(seed)

    # ==========================================================
    # Determine the number of cells that need to be filled
    # ==========================================================
    numCells = len(loc[0])

    # ==========================================================
    # Sample values from beta distribution
    # ==========================================================
    values = expon.beta(a=alpha, b=beta)

    # ==========================================================
    # Normalize to the desired mean
    # ==========================================================
    values *= mean / values.mean()

    # ==========================================================
    # Make a cube to hold the values and fill the cells
    # indicated by <loc> with the random values
    # ==========================================================
    cube = makeCube(dim)
    cube[loc] = values

    # ==========================================================
    # Return the cube
    # ==========================================================
    return(cube)


def exponential(dim, loc, mean, seed=1000):
    """
    Fills cells at <loc> with numbers sampled from an exponential distribution
    with <mu=mean> and returns the cube.

    Parameters:
        dim         cube dimensions {tuple}
        loc         array containing cells representing the nebula {np.ndarray}
        mean        mean value {float}
        seed        random number seed {int}

    Returns:
        cube        cube containing random values {3D array}
    """
    # ==========================================================
    # Set the random number seed
    # ==========================================================
    np.random.seed(seed)

    # ==========================================================
    # Determine the number of cells that need to be filled
    # ==========================================================
    numCells = len(loc[0])

    # ==========================================================
    # Sample values from exponential distribution with
    # the provided mean
    # ==========================================================
    values = expon.rvs(scale=mean, size=numCells)

    # ==========================================================
    # Make a cube to hold the values and fill the cells
    # indicated by <loc> with the random values
    # ==========================================================
    cube = makeCube(dim)
    cube[loc] = values

    # ==========================================================
    # Return the cube
    # ==========================================================
    return(cube)


def lognormal(dim, loc, mean, sigma, seed=5007):
    """

    """
    # ==========================================================
    # Set the random number seed
    # ==========================================================
    np.random.seed(seed)

    # ==========================================================
    # Determine the number of cells that need to be filled
    # ==========================================================
    numCells = len(loc[0])

    # ==========================================================
    # Determine the <scale> parameter: <mean = scale exp(s^2/2)>
    # ==========================================================
    scale = mean * np.exp(-0.5 * sigma**2)

    # ==========================================================
    # Sample values
    # ==========================================================
    values = lognorm.rvs(sigma, scale=scale, size=numCells)

    # ==========================================================
    # Make cube and fill
    # ==========================================================
    cube = makeCube(dim)
    cube[loc] = values

    # ==========================================================
    # Return the cube
    # ==========================================================
    return(cube)


def lognormalPareto(dim, loc, mean, sigma, c, seed=7007):
    """

    """
    # ==========================================================
    # Set the random number seed
    # ==========================================================
    np.random.seed(seed)

    # ==========================================================
    # Determine the number of cells that need to be filled
    # ==========================================================
    numCells = len(loc[0])

    # ==========================================================
    # Sample values from distribution
    # ==========================================================
    values = powerlognorm.rvs(c=c, s=sigma, size=numCells)
    values *= mean / values.mean()

    # ==========================================================
    # Make cube and fill
    # ==========================================================
    cube = makeCube(dim)
    cube[loc] = values

    # ==========================================================
    # Return the cube
    # ==========================================================
    return(cube)



def mlp(dim, loc, mean, sigma, alpha, seed=3923):
    """
    Fills cells at <loc> with numbers sampled from the modified lognormal
    pareto distribution with <mu=mean> and parameters <sigma> and <alpha>
    and returns the cube.

    Parameters:
        dim         cube dimensions {tuple}
        loc         array containing cells representing the nebula {np.ndarray}
        mean        mean value {float}
        sigma       distribution parameter {float}
        alpha       distribution parameter {float>1}
        seed        random number seed {int}

    Returns:
        cube        cube containing random values {3D array}
    """

    # ==========================================================
    # Check if <alpha> > 1
    # ==========================================================
    if alpha <= 1:
        print("In function <mlp> please use <alpha> > 1")
        sys.exit(1)

    # ==========================================================
    # Set the random seed
    # ==========================================================
    np.random.seed(seed)

    # ==========================================================
    # Determine the number of cells that need to be filled
    # ==========================================================
    numCells = len(loc[0])

    # ==========================================================
    # Determine the parameter <mu> to have a mean density
    # given by <mean>
    # ==========================================================
    mu = np.log(mean*(1-1./alpha)) - 0.5*sigma**2

    # ==========================================================
    # Sample random values from the MLP distribution
    # ==========================================================
    norm = np.random.normal(size=numCells)
    unif = np.random.uniform(size=numCells)
    values = np.exp(mu + sigma*norm - np.log(unif)/alpha)

    # ==========================================================
    # Make cube and fill
    # ==========================================================
    cube = makeCube(dim)
    cube[loc] = values

    # ==========================================================
    # Return the cube
    # ==========================================================
    return(cube)

def normal(dim, loc, mean, sigma, seed=8938):
    """

    """
    # ==========================================================
    # Set the random seed
    # ==========================================================
    np.random.seed(seed)

    # ==========================================================
    # Determine the number of cells that need to be filled
    # ==========================================================
    numCells = len(loc[0])

    # ==========================================================
    # Sample values from the distribution
    # While any of the values are less than 0,
    # continue to resample
    # ==========================================================
    sample = np.random.normal(loc=mean, scale=sigma, size=numCells)
    while min(sample) < 0:
        tmp = sample < 0
        resample = np.random.normal(loc=mean, scale=sigma, size=sum(tmp))
        sample[tmp] = resample

    # ==========================================================
    # Make cube and fill
    # ==========================================================
    cube = makeCube(dim)
    cube[loc] = sample

    # ==========================================================
    # Return the cube
    # ==========================================================
    return(cube)

def polytrope(cube, index, mean, geom=False, loc=None):
    """
    Given a cube containing values, returns another cube
    with values based on a polytropic relation with index
    <index> normalized to have a mean value <mean>.


    Parameters:
        cube            cube of values to use for polytropic relation
        index           Index relation y = const * x^(index - 1)
        mean            mean value of returned array {float}
        geom            method by which the mean value is calculated
                        (by volume {true} or particles {false}) {boolean}
        loc             cell locations
    """
    # ==========================================================
    # Make sure <cube> is a numpy array
    # ==========================================================
    if not isinstance(cube, np.ndarray):
        print("Input parameter <cube> must be an array")
        sys.exit(1)

    # ==========================================================
    # Find the cells that are not empty if <loc> not input
    # ==========================================================
    if isinstance(loc, type(None)):
        loc = cube > 0

    # ==========================================================
    # Create a new cube to hold the new values.
    # ==========================================================
    new_cube = np.zeros_like(cube)

    # ==========================================================
    # Apply the polytrope transformation to the values in <cube>
    # ==========================================================
    new_cube[loc] = cube[loc]**(index-1)

    # ==========================================================
    # Normalize to the correct mean temperature, which are
    # either the volumetric mean or by the particle numbers.
    # ==========================================================
    if geom:
        new_cube[loc] *= mean / new_cube[loc].mean()
    else:
        weighted = np.sum(cube[loc] * new_cube[loc]) / np.sum(cube[loc])
        new_cube[loc] *= mean / weighted

    return(new_cube)


def radialGradient(dim, loc, func, mean=None):
    """
    Function that applies a radial gradient
    """
    # ==========================================================
    # Get the (scaled) radial distances
    # ==========================================================
    distances = getRadialDistance(dim=dim)[loc]
    distances /= np.max(distances)

    # ==========================================================
    # Apply the functional form; adjust the mean value
    # ==========================================================
    values = func(distances)

    # ==========================================================
    # Adjust the mean value (if applicable)
    # ==========================================================
    if mean:
        values *= mean / np.mean(values)

    # ==========================================================
    # Create a cube; insert the values
    # ==========================================================
    cube = makeCube(dim)
    cube[loc] = values

    # ==========================================================
    # Return the cube
    # ==========================================================
    return cube



# ===================================================
# Dictionaries that reference the distribution functions
# ===================================================
pdfs = {
    'beta'       : beta,
    'exponential': exponential,
    'lognormal'  : lognormal,
    'mlp'        : mlp,
    'normal'     : normal,
    'pareto'     : lognormalPareto,
    'polytrope'  : polytrope,
    'gradient'   : radialGradient
}

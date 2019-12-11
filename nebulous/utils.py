from scipy.ndimage import gaussian_filter
import numpy as np


def convl2D(image, kernel=1.0, mode='constant'):
    return gaussian_filter(image, sigma=kernel, mode=mode)

def getCoordinates(dim):
    """
    Returns the coordinates of each cell with the center of
    the cube as the origin.

    Parameters:
        dim     cube dimensions (xdim, ydim, zdim) {tuple}

    Returns:
        x   x-coordinate
        y   y-coordinate
        z   z-coordinate (depth)
    """

    # ==================================================
    # Make sure <dim> has the proper size
    # ==================================================
    dim = parseCubeDimensions(dim)

    # ==================================================
    # Center the coordinates at the center of the sphere
    # ==================================================
    x = np.arange(dim[0], dtype='float')
    y = np.arange(dim[1], dtype='float')
    z = np.arange(dim[2], dtype='float')

    x -= np.mean(x)
    y -= np.mean(y)
    z -= np.mean(z)

    y, x, z = np.meshgrid(y, x, z)

    # ==================================================
    # Return the coordinates
    # ==================================================
    return(x, y, z)

def getDepthTrue(cube):
    """
    Computes the true line of sight depth, ignoring cells with
    zero density along the line of sight.

    Parameters:
        cube            a 3D array containing nebular values

    Returns:

    Postcondition:
    """
    return np.count_nonzero(cube, axis=-1)

def getDepth(dim, loc):
    """
    Computes the depth along the line of sight, counting
    all cells within the outer-boundary of the nebula,
    even ones empty of particles.

    To call:
        getDepth(dim, loc)
    """
    # ==================================================
    # Make a cube with the provided dimensions
    # ==================================================
    cube = makeCube(dim)

    # ==================================================
    # Assign each value within the nebula a value > 0
    # ==================================================
    cube[loc] = 1

    # ==================================================
    # Compute and return the depth along the line of sight
    # ==================================================
    return getDepthTrue(cube)

def getRadialDistance(dim):
    """
    Given the dimensions of the cube, computes the distance
    of each cell from the center of the cube.
    """
    # ==================================================
    # Get the cell coordinates
    # ==================================================
    x, y, z = getCoordinates(dim)

    # ==================================================
    # Compute the radial distance
    # ==================================================
    dist = np.sqrt(x**2 + y**2 + z**2)

    # ==================================================
    # Return the radial distances
    # ==================================================
    return(dist)


def makeCube(dim):
    dim = parseCubeDimensions(dim)
    cube = np.zeros(dim)
    return(cube)


def parseCubeDimensions(dim):
    """
    Returns a tuple representation of the cube dimensions.
    """
    if isinstance(dim, tuple):
        if len(dim) != 3:
            return 3*(dim[0],)
        else:
            return dim
    else:
        return 3*(dim,)

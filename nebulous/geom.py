from .utils import getCoordinates, getRadialDistance, makeCube, parseCubeDimensions
import numpy as np

def sphere(dim, inRad=0.3, outRad=0.9, axis=0):
    """
    Method for generating a spherical nebula.

    Parameters:
        dim         dimension of cube
        inRad       fractional inner radius (0 < inRad < outRad)
        outRad      fractional outer radius (inRad < outRad < 1)
        axis        axis of <dim> associated with <inRad, outRad>

    Returns
        cells       tuple containing cell locations within the nebula

    Postcondition:
        The cell locations that are within the inner and outer
        radii are returned. If <dim> is a single integer, then
        the dimension is (dim, dim, dim).
    """
    # ==================================================
    # Parse the input dimensions
    # ==================================================
    dim = parseCubeDimensions(dim)

    # ==================================================
    # Determine the inner and outer radii of the nebula
    # ==================================================
    inRad  = inRad  * (0.5 * dim[axis])
    outRad = outRad * (0.5 * dim[axis])

    # ==================================================
    # Compute the radial distance
    # ==================================================
    radial_distance = getRadialDistance(dim)

    # ==================================================
    # Determine which cells are part of the nebula
    # ==================================================
    cells = np.where(
        (radial_distance >= inRad) & \
        (radial_distance <= outRad)
    )

    # ==================================================
    # Return the cell locations contained with the
    # boundary of the nebula
    # ==================================================
    return(cells)



def partition(loc, pvals, seed):
    """
    Method for partitioning cells into several distinct groupings.

    Variables:
        loc             cell locations within the nebula
        pvals           list of partitioning probabilities
        seed            random number seed

    Returns
        new_loc         List of tuples containing the cell coordinates
                        for each of the different partitions.

    Postcondition:
        The cell locations are split into len(<pvals>) partitions
        and the partitions return in a list in the same manner as
        <loc>.
    """
    # ==========================================================
    # Set the random number seed
    # ==========================================================
    np.random.seed(seed)

    # ==================================================
    # Determing the number of cells to sample from
    # ==================================================
    numCells = loc[0].shape[0]

    # ==================================================
    # Randomly assign each cell location to a partition
    # ==================================================
    sample = np.random.choice(len(pvals), size=numCells, p=pvals)

    # ==================================================
    # Iterate through each partition and retrieve the
    # cell coordinates.
    # ==================================================
    new_loc = []
    for i, p in enumerate(pvals):

        # ==============================================
        # Find the cells that have been assigned to the
        # current partition
        # ==============================================
        temp = sample == i

        # ==============================================
        # Extract the cell locations for the current
        # partition
        # ==============================================
        partition = []
        for coord in loc:
            partition.append(coord[temp])

        # ==============================================
        # Store a tuple of the cell coordinates
        # ==============================================
        new_loc.append(tuple(partition))

    return new_loc

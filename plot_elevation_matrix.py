import pickle
import numpy as np
from mayavi import mlab
import sys


def unpickle_elevation_matrix(pickle_file):
    """
    Reads a pickled elevation matrix
    :param pickle_file: location of pickle file
    :return: elevation matrix
    """
    with open(pickle_file, 'rb') as pickle_file:
        matrix = pickle.load(pickle_file)
    return matrix


def convert_matrix(matrix, scale_factor):
    """
    Converts an elevation matrix into x, y, z numpy arrays
    :param matrix: elevation matrix
    :param scale_factor: distance in meters between 2 x or y points
    :return: x, y, z numpy arrays
    """
    x, y, z = [], [], []
    for row in matrix:
        for value in row:
            x.append(value[0] * scale_factor)
            y.append(value[1] * scale_factor)
            z.append(value[2])
    return np.array(x), np.array(y), np.array(z)


def plot_mlab(x, y, z):
    """
    Plots the elevation matrix to a mayavi object
    :param x: x_values
    :param y: y_values
    :param z: z_values
    :return: None
    """
    mlab.figure(1, fgcolor=(0, 0, 0), bgcolor=(1, 1, 1), size=(1024, 768))
    pts = mlab.points3d(x, y, z, z, scale_mode='none', scale_factor=1.0)
    mesh = mlab.pipeline.delaunay2d(pts)

    surf = mlab.pipeline.surface(mesh)

    mlab.show()


def main():
    if len(sys.argv) != 2:
        print("Invalid number of arguments")
        exit(1)

    loaded_matrix = unpickle_elevation_matrix(sys.argv[1])
    x, y, z = convert_matrix(loaded_matrix, 300)
    plot_mlab(x, y, z)


if __name__ == "__main__":
    main()

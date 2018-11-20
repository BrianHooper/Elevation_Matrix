from pickle import load
from numpy import array
import numpy as np
from mayavi import mlab
import matplotlib.pyplot as plt


def unpickle_elevation_matrix(pickle_file):
    """
    Reads a pickled elevation matrix
    :param pickle_file: location of pickle file
    :return: elevation matrix
    """
    with open(pickle_file, 'rb') as pickle_file:
        matrix = load(pickle_file)
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
    return array(x), array(y), array(z)


def plot_mlab(x, y, z):
    """
    Plots the elevation matrix to a mayavi object
    :param x: x_values
    :param y: y_values
    :param z: z_values
    :return: None
    """
    mlab.figure(1, fgcolor=(0, 0, 0), bgcolor=(0, 0, 0), size=(1024, 768))
    pts = mlab.points3d(x, y, z, z, scale_mode='none', scale_factor=0.0)
    mesh = mlab.pipeline.delaunay2d(pts)

    mlab.pipeline.surface(mesh)

    mlab.show()


def f(x, y):
    return np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)

def main():
    loaded_matrix = unpickle_elevation_matrix("matrix_pickle_k2.bin")
    x, y, z = convert_matrix(loaded_matrix, 300)

    plot_mlab(x, y, z)


    plt.tricontour(x.ravel(), y.ravel(), z.ravel(), 100)
    plt.show()
    print("stop")

if __name__ == "__main__":
    main()

# Brian Hooper
# November 8th, 2018

import json
import requests
import pickle
import sys

URL_HEAD = "https://maps.googleapis.com/maps/api/elevation/json?locations="


def parse_json(json_data):
    """
    Extracts elevation from json data
    :param json_data: json data object
    :return: elevation as float
    """
    return float(json_data["results"][0]["elevation"])


def retrieve_elevation(latitude, longitude, api_key):
    """
    Retrieves elevation data from google maps api
    :param latitude: x coordinate
    :param longitude: y coordinate
    :param api_key: api key for google maps
    :return: elevation at coordinate
    """
    url = URL_HEAD + str(latitude) + "," + str(longitude) + "&key=" + api_key
    raw_json = requests.get(url).text
    json_data = json.loads(raw_json)
    elevation = parse_json(json_data)
    return elevation


def create_matrix(latitude, longitude, radius, spacing, api_key):
    """
    Creates a matrix of (latitude, longitude, elevation) tuples
    :param latitude: center point latitude
    :param longitude: center point longitude
    :param radius: 1/2 width of matrix
    :param spacing: distance between points
    :param api_key: google maps api key
    :return: elevation matrix
    """
    total_elements = 2 * radius * (2 * radius + 1)
    matrix = []
    for y in range(-radius, radius + 1):
        y_index = radius + y
        row = []
        for x in range(-radius, radius + 1):
            x_index = (radius + x) + (2 * radius * y_index)
            relative_latitude = latitude + (x * spacing)
            relative_longitude = longitude + (y * spacing)
            print("Percent: %.4f: %.5f, %.5f" % ((x_index / total_elements), relative_latitude, relative_longitude))
            elevation = retrieve_elevation(relative_latitude, relative_longitude, api_key)
            row.append((relative_latitude, relative_longitude, elevation))
        matrix.append(row)
    return matrix


def to_relative_matrix(matrix):
    """
    Converts an elevation matrix to a matrix of relative values
    :param matrix: elevation matrix
    :return: relative matrix
    """
    new_matrix = []
    for x in range(0, len(matrix)):
        new_row = []
        for y in range(0, len(matrix[x])):
            new_row.append((x, y, matrix[x][y][2]))
        new_matrix.append(new_row)
    return new_matrix


def pickle_matrix(matrix, pickle_file):
    """
    Pickles elevation matrix so it can be reused
    :param matrix: elevation matrix
    :param pickle_file: path of pickle file
    :return: None
    """
    with open(pickle_file, 'wb') as pickle_file:
        pickle.dump(matrix, pickle_file)


def main():
    if len(sys.argv) != 4:
        print("Invalid number of arguments")
        exit(1)

    api_key = sys.argv[1]
    latitude = float(sys.argv[2])
    longitude = float(sys.argv[3])

    matrix = create_matrix(latitude, longitude, 20, 0.005, api_key)
    matrix = to_relative_matrix(matrix)
    pickle_matrix(matrix, "matrix_pickle.bin")


if __name__ == "__main__":
    main()

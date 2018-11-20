# Brian Hooper
# November 8th, 2018

from json import JSONDecodeError, loads
from requests import get, exceptions
from pickle import dump
from sys import argv
from math import radians, cos, sin, asin, sqrt

URL_HEAD = "https://maps.googleapis.com/maps/api/elevation/json?locations="


def progress_bar(percent, width=50):
    """
    prints a progress bar to the console
    :param percent: current percentage completed
    :param width: number of characters wide to make the progress bar
    :return: None
    """
    num_pounds = int(percent * width)
    pounds = "#" * num_pounds
    dashes = "-" * (width - num_pounds)
    print("\rProgress: %7.3f%% %s%s" % (percent * 100, pounds, dashes), end="")


def parse_json(json_data):
    """
    Extracts elevation from json data
    :param json_data: json data object
    :return: elevation as float
    """
    if "results" in json_data:
        if type(json_data["results"]) == list and len(json_data["results"]) != 0:
            if "elevation" in json_data["results"][0]:
                return int(json_data["results"][0]["elevation"])
    return 0


def retrieve_elevation(latitude, longitude, api_key):
    """
    Retrieves elevation data from google maps api
    :param latitude: x coordinate
    :param longitude: y coordinate
    :param api_key: api key for google maps
    :return: elevation at coordinate
    """
    url = URL_HEAD + str(latitude) + "," + str(longitude) + "&key=" + api_key
    try:
        http_request = get(url)
    except exceptions.RequestException as e:
        print(e)
        return 0
    if http_request.status_code == 200:
        raw_json = http_request.text
        try:
            json_data = loads(raw_json)
            elevation = parse_json(json_data)
            return elevation
        except JSONDecodeError:
            return 0
    else:
        return 0


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371
    return int(c * r * 1000)


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

    step_distance = haversine(latitude, longitude, latitude + spacing, longitude + spacing)

    width = 2 * radius + 1
    total_elements = width * width

    latitude_range = list(map(lambda i: round((i * spacing) + latitude, 6), range(-radius, radius + 1)))
    longitude_range = list(map(lambda i: round((i * spacing) + longitude, 6), range(-radius, radius + 1)))
    matrix = [[(0, 0, 0) for _ in range(width)] for _ in range(width)]

    for x in range(width):
        for y in range(width):
            progress_bar(((x * width) + y) / (total_elements - 1))
            elevation = retrieve_elevation(latitude_range[x], longitude_range[y], api_key)
            matrix[x][y] = (x, y, elevation)
    print("")
    return matrix


def pickle_matrix(matrix, pickle_file):
    """
    Pickles elevation matrix so it can be reused
    :param matrix: elevation matrix
    :param pickle_file: path of pickle file
    :return: None
    """
    with open(pickle_file, 'wb') as pickle_file:
        dump(matrix, pickle_file)


def main():
    if len(argv) != 4:
        print("Invalid number of arguments")
        exit(1)

    api_key = argv[1]
    latitude = float(argv[2])
    longitude = float(argv[3])

    matrix = create_matrix(latitude, longitude, 50, 0.0005, api_key)
    pickle_matrix(matrix, "matrix_pickle.bin")


if __name__ == "__main__":
    main()

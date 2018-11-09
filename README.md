# Elevation Matrix

Elevation_Matrix uses the Google Maps Elevation API to create a matrix of elevation values for a region given by a GPS location, and then plot them as a 3D surface using the Mayavi library.

The program is split into two modules, request_elevation_data.py, for downloading elevation data from Google Maps, and plot_elevation_matrix.py, for plotting the elevation matrix onto a 3D surface.

Plot generated from K2 mountain:

![](https://raw.githubusercontent.com/BrianHooper/Elevation_Matrix/master/k2_plot.png)

Google Earth screenshot of same location:

![](https://raw.githubusercontent.com/BrianHooper/Elevation_Matrix/master/k2_earth.png)

# Use

The program can be run from the command line by running

```
python3 request_elevation_data.py <api_key> <latitude> <longitude>
python3 plot_elevation_matrix.py <pickled_binary_file>
```

Necessary libraries are numpy and mayavi. Mayavi can be difficult to install, but I've had good luck with the following commands on Ubuntu 17.10:

```
 sudo python3 -m pip install mayavi
 sudo python3 -m pip install pyqt5
 ```


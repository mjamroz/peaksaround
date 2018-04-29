#!/usr/bin/env python

from osgeo import gdal
import matplotlib.pyplot as plt


from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from peaks import PeaksAround
from plot import format_for_plot

#lat, lon = 45.187739, 5.714140
lat, lon = 45.2087542, 5.8590479 # vieux
#lat, lon = 45.234440, 5.710000 # neron

gdal.UseExceptions()
ds = gdal.Open('srtm_38_03.tif')
band = ds.GetRasterBand(1)
elevation = band.ReadAsArray()


nrows, ncols = elevation.shape

x0, dx, dxdy, y0, dydx, dy = ds.GetGeoTransform()

x1 = x0 + dx * ncols
y1 = y0 + dy * nrows
print nrows, ncols, x0, '-', x1, y0, '-', y1


def calc_ranges(lat, lon, delta, nrows, ncols, dx, dy, x0, y0):
    lon_x = int((lon-x0)/dx)
    lat_y = int((lat-y0)/dy)
    delta_x = delta/dx
    delta_y = delta/dy
    ranges = [int(lon_x-delta_x), int(lon_x+delta_x), int(lat_y-delta_y), int(lat_y+delta_y)]
    for i in range(len(ranges)):
        if ranges[i] < 0:
            ranges[i] = 0

    if ranges[0] > nrows:
        ranges[0] = nrows
    if ranges[1] > nrows:
        ranges[1] = nrows
    if ranges[2] > ncols:
        ranges[2] = ncols
    if ranges[3] > ncols:
        ranges[3] = ncols

    if ranges[0] > ranges[1]:
        t = ranges[0]
        ranges[0] = ranges[1]
        ranges[1] = t
    if ranges[2] > ranges[3]:
        t = ranges[2]
        ranges[2] = ranges[3]
        ranges[3] = t

    print "ranges =", ranges
    return ranges

def get_surrounding(lat, lon, delta=0.1):
    global nrows, ncols, dx, dy, x0, y0
    ranges = calc_ranges(lat, lon, delta, nrows, ncols, dx, dy, x0, y0)
    rows = []
    cols = []
    elevations = []
    aatans = []
    for row in range(ranges[0], ranges[1]):
        for col in range(ranges[2], ranges[3]):
            ele = elevation[col][row]
            col_coord = x0 + dx * col
            row_coord = y0 + dy * row
            rows.append(row_coord)
            cols.append(col_coord)
            elevations.append(ele)
            # x0 4.9995835028 (lon) y0 50.0004170299 (lat)
            lat_ = row_coord - lat
            lon_ = col_coord - lon
            atan = np.arctan2(lat_, lon_)
            aatans.append(atan)

    return (rows, cols, elevations, aatans)

rows, cols, elevations, atans_ele = get_surrounding(lat, lon)

#f, axarr = plt.subplots()
#ax = axarr
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


#ax.set_xlim([-np.pi, np.pi])
#Peaks = PeaksAround(lat, lon, 1)
#peaks = format_for_plot(Peaks)
#atans, alts, names = [], [], []
#for e in peaks:
#    atans.append(e[0])
#    alts.append(e[1])
#    names.append(e[2])

ax.scatter(atans_ele, elevations, alpha=0.5)
#ax.scatter(rows, cols, alpha=0.1)
#ax.scatter(atans, alts)
#for i in range(len(atans)):
    #ax.text(atans[i], alts[i], repr(names[i]), fontsize=6, rotation=-45)

plt.show()

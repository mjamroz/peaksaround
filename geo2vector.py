#!/usr/bin/env python

from osgeo import gdal
import numpy as np


class TifReader():
    def __init__(self, filename):
        gdal.UseExceptions()
        ds = gdal.Open(filename)
        band = ds.GetRasterBand(1)
        self.elevation = band.ReadAsArray()
        self.nrows, self.ncols = self.elevation.shape
        self.xoff, self.a, _, self.yoff, _, self.e = ds.GetGeoTransform()

        # lat y
        lat_range_ = (self.yoff, self.yoff + self.e*self.nrows)
        lon_range_ = (self.xoff, self.xoff + self.a*self.ncols)
        self.lat_range = (np.min(lat_range_), np.max(lat_range_))
        self.lon_range = (np.min(lon_range_), np.max(lon_range_))

    def in_the_range(self, lat, lon):
        return lat >= self.lat_range[0] and lat < self.lat_range[1] \
            and lon >= self.lon_range[0] and lon < self.lon_range[1]

    def pixel2coord(self, x, y):
        xp = self.a * x + self.xoff
        yp = self.e * y + self.yoff
        return(xp, yp)

    def coord2pixel(self, xp, yp):
        x = (xp - self.xoff) / self.a
        y = (yp - self.yoff) / self.e
        return(int(round(x)), int(round(y)))

    def testing_conversion(self):
        for r in range(self.nrows):
            for c in range(self.ncols):
                p2c = self.pixel2coord(r, c)
                c2p = self.coord2pixel(p2c[0], p2c[1])
                assert r == c2p[0] and c == c2p[1]

    def square(self, x_from, x_to, y_from, y_to):
        xr1, yr1 = self.coord2pixel(x_from, y_from)
        xr2, yr2 = self.coord2pixel(x_to, y_to)

        d = [xr1, xr2, yr2, yr1]
        for e in range(4):
            if d[e] < 0:
                d[e] = 0

        temp = []

        assert yr2 < yr1
        assert xr1 < xr2

        for row in range(xr1, xr2):
            for col in range(yr2, yr1):
                if row < self.nrows and col < self.ncols:
                    p2c = self.pixel2coord(row, col)
                    temp.append([1.0*p2c[0], 1.0*p2c[1], 1.0*self.elevation[row][col]])
        return temp

# Corner Coordinates:
#     Upper Left  (  -0.0004166,  50.0004170) (  0d 0' 1.50"W, 50d 0' 1.50"N)
#     Lower Left  (  -0.0004166,  44.9995837) (  0d 0' 1.50"W, 44d59'58.50"N)
#     Upper Right (   5.0004167,  50.0004170) (  5d 0' 1.50"E, 50d 0' 1.50"N)
#     Lower Right (   5.0004167,  44.9995837) (  5d 0' 1.50"E, 44d59'58.50"N)
#


if __name__ == "__main__":
    g = TifReader("srtm_37_03.tif")
    print g.square(-1.0004166, 4.99999, 44.9995837, 45.001)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peaks import PeaksAround
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import Basemap

import numpy as np
import matplotlib.pyplot as plt

#gubalo
#lat, lon = 49.3058851,19.9259982
# saint bruno
lat, lon = 45.187739, 5.714140
# lat, lon = 45.6736,6.3803 # albertville
# vieux
#lat, lon = 45.2087542, 5.8590479
my_alt = 250
# Pelvoux/@44.9030791,6.3736697
#lat, lon = 44.9030791, 6.3736697

Peaks = PeaksAround(lat, lon, my_alt)

def format_for_plot(Peaks):
    atans, names, alts, lons, lats, distances = [], [], [], [], [], []
    for e in Peaks.visible_from_me():
        lat_ = e[3] - lat
        lon_ = e[4] - lon
        lats.append(lat_)
        lons.append(lon_)
        alts.append(e[2])
        names.append(e[1])
        distances.append(e[5])
        atan = np.arctan2(lon_, lat_)
        atans.append(atan)
    peaks = zip(atans, alts, names, distances)
    return Peaks.hide_peaks_behind(peaks)

def plot_peaks(peaks, cut=3000):
    if cut > len(peaks):
        cut = len(peaks)
    atans, alts, names = [], [], []
    for e in peaks:
        atans.append(e[0])
        alts.append(e[1])
        names.append(e[2])
    f, axarr = plt.subplots()
    ax = axarr
    ax.set_xlim([-np.pi, np.pi])
    ax.set_ylim([np.min(alts)-500, np.max(alts)+500])
    ax.scatter(atans[:cut], alts[:cut])
    for i in range(cut):
        ax.text(atans[i], alts[i], repr(names[i]), fontsize=6, rotation=-45)
    plt.show()


if __name__ == "__main__":
# fine test:
    peaks_faked = [
            (1, 1000.0, '<-- alt, dist -->', 1000),
            (1, 500.0, '<-- alt, dist -->', 2000),
            (1, 2500.0, '<-- alt, dist -->', 3000),
            (1, 3000.0, '<-- alt, dist -->', 4000),
            (1, 2900.0, '<-- alt, dist -->', 5000),
            (1, 7000.0, '<-- alt, dist -->', 6000),
            ]
    plot_peaks(format_for_plot(Peaks))

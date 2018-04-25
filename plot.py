#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peaks import PeaksAround
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import Basemap

import numpy as np
import matplotlib.pyplot as plt


# saint bruno
lat, lon = 45.187739, 5.714140
# vieux
#lat, lon = 45.2087542, 5.8590479
my_alt = 200
# Pelvoux/@44.9030791,6.3736697
#lat, lon = 44.9030791, 6.3736697

peaks = PeaksAround(lat, lon)
atans, names, alts, lons, lats = [], [], [], [], []
for e in peaks.visible_from_me(my_alt=my_alt):
    lat_ = e[3] - lat
    lon_ = e[4] - lon
    lats.append(lat_)
    lons.append(lon_)
    alts.append(e[2])
    names.append(e[1])
    atan = np.arctan2(lon_, lat_)
    atans.append(atan)

def plot_peaks(atans, alts, names, cut=30):
    f, axarr = plt.subplots()
    ax = axarr
    #ax.set_xlim([-2*np.pi, 2*np.pi])
    ax.scatter(atans[:cut], alts[:cut])
    for i in range(cut):
        ax.text(atans[i], 1000, repr(names[i]), fontsize=6, rotation=-90)
    plt.show()


def hide_peaks_behind(atans, names, alts, my_alt, bin_size=0.1):
    temp = []
    for e in zip(atans, names, alts):
        temp.append(e)
    temp.sort(key=lambda tup: tup[0])
    print temp


hide_peaks_behind(atans, names, alts, 200)

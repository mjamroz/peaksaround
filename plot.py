#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peaks import PeaksAround
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import Basemap

import numpy as np
import matplotlib.pyplot as plt


# saint bruno
lat, lon = 45.187739, 5.714140
lat, lon = 45.6736,6.3803 # albertville
# vieux
#lat, lon = 45.2087542, 5.8590479
my_alt = 2000
# Pelvoux/@44.9030791,6.3736697
#lat, lon = 44.9030791, 6.3736697

peaks = PeaksAround(lat, lon)
atans, names, alts, lons, lats, distances = [], [], [], [], [], []
for e in peaks.visible_from_me(my_alt=my_alt):
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

def plot_peaks(peaks, cut=300):
    print peaks
    if cut > len(peaks):
        cut = len(peaks)
    atans, alts, names = [], [], []
    for e in peaks:
        atans.append(e[0])
        alts.append(e[1])
        names.append(e[2])
    f, axarr = plt.subplots()
    ax = axarr
    #ax.set_xlim([-2*np.pi, 2*np.pi])
    ax.scatter(atans[:cut], alts[:cut])
    for i in range(cut):
        ax.text(atans[i], 1000, repr(names[i]), fontsize=6, rotation=-90)
    plt.show()

def pick_only_closest(peaks, my_alt):
    # altitude / distance = tg theta

    if len(peaks) < 2:
        return peaks
    peaks.sort(key=lambda tup: tup[3])

    # first peak always visible
    cleaned = [peaks[0]]
    peaks.remove(peaks[0])

    changed = True
    while changed:
        last_peak = cleaned[-1]
        last_peak_tg = (last_peak[1])/last_peak[3]
        changed = False
        for p in peaks:
            curr_peak_tg = (p[1])/p[3]
            if curr_peak_tg > last_peak_tg:
                cleaned.append(p)
                peaks.remove(p)
                changed = True
    return cleaned


def hide_peaks_behind(peaks, my_alt, bin_size=0.2):
    temp = []

    picked = []
    for e in peaks:
        temp.append(e)
    temp.sort(key=lambda tup: tup[0])
    # make grid of bin_size edges
    c0 = -np.pi*2
    for c in np.arange(-np.pi*2+bin_size, np.pi*2, bin_size):
        grid = []
        for e in temp:
            if e[0] < c and e[0] >= c0:
                grid.append(e)
        picked += pick_only_closest(grid, my_alt)
        c0 = c
    return picked


peaks = hide_peaks_behind(peaks, my_alt)
plot_peaks(peaks)

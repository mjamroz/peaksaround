#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import math
import csv


def populate_database():
    conn = sqlite3.connect("summits.db")  # http://www.sotadata.org.uk/summits.aspx
    conn.text_factory = str
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS summits (id integer primary key, \
              name text not null, lon float, lat float, alt float)")
    c.execute("DELETE FROM summits")
    with open('summitslist.csv', 'rb') as csvfile:
        summits = csv.reader(csvfile, delimiter=',')
        data = []
        for summit in summits:
            name = summit[3]
            alt = summit[4]
            lon = summit[8]
            lat = summit[9]
            data.append([name, lon, lat, alt])
        c.executemany("INSERT INTO summits(name, lon, lat, alt) VALUES \
                      (?,?,?,?)", data)
    conn.commit()


conn = sqlite3.connect("summits.db")
conn.text_factory = str
cursor = conn.cursor()


def haversine(lon1, lat1, lon2, lat2):
    # https://community.esri.com/groups/coordinate-reference-systems/blog/2017/10/05/haversine-formula
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)
    a = math.sin(math.radians(lat2 - lat1) / 2.0) ** 2 + math.cos(phi_1) * \
        math.cos(phi_2) * math.sin(math.radians(lon2 - lon1)/2.0) ** 2
    c = 6371000 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return round(c, 3)


def calc(lat, lon, limit=100):
    # https://stackoverflow.com/a/7472230

    global cursor
    fud = math.pow(math.cos(math.radians(lat)), 2)
    cursor.execute("SELECT lat,lon,name,alt FROM summits ORDER BY ((? - lat) * \
                   (? - lat) + (? - lon) * (? - lon) * ?) LIMIT ?",
                   [lat, lat, lon, lon, fud, limit])
    for e in cursor.fetchall():
        lat_ = e[0]
        lon_ = e[1]
        print e[2], e[3], haversine(lon_, lat_, lon, lat)


# saint bruno
lat = 45.1841555
lon = 5.7208091
calc(lat, lon)

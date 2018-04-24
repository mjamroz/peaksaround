#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import math
import csv
import json


def view_range(height):
    return 3.57 * math.sqrt(height) * 1000


def populate_database_from_osm():
    conn = sqlite3.connect("summits.db")
    # wget https://overpass-api.de/api/interpreter?data=%5Bout%3Ajson%5D%3B%0A%28%0A%20%20node%5B%22natural%22%3D%22peak%22%5D%2835.496456056584165%2C-10.107421874999998%2C56.897003921272606%2C28.5205078125%29%3B%0A%29%3B%0Aout%20body%3B%0A%3E%3B -O peaks_europe.json
    conn.text_factory = str
    c = conn.cursor()
    try:
        c.execute("DROP TABLE summits")
    except sqlite3.OperationalError:
        print "table not dropped"
    c.execute("CREATE TABLE IF NOT EXISTS summits (id integer primary key, \
              name text not null, lon float, lat float, alt float, \
              viewrange float, wikipedia text)")
    c.execute("CREATE INDEX sum_lon ON summits(lon)")
    c.execute("CREATE INDEX sum_lat ON summits(lat)")
    c.execute("CREATE INDEX sum_alt ON summits(alt)")
    with open('peaks_europe.json', 'r') as jsonfile:
        summits = json.loads(jsonfile.read())
        data = []
        for summit in summits['elements']:

            if 'name' not in summit['tags'] or 'ele' not in summit['tags']:
                print "Cannot import ", summit
                continue
            try:
                alt = summit['tags']['ele'].replace("m", "").replace(",", ".")
                _ = float(alt)
            except ValueError:
                print "Cannot parse alt", summit
                continue
            name = summit['tags']['name']
            lon = summit['lon']
            lat = summit['lat']
            wiki = ''
            if 'wikipedia' in summit['tags']:
                wiki = summit['tags']['wikipedia']

            viewrange = view_range(float(alt))
            data.append([name, lon, lat, alt, viewrange, wiki])
        c.executemany("INSERT INTO summits(name, lon, lat, alt, viewrange, wikipedia) VALUES \
                      (?,?,?,?,?,?)", data)
        print "Imported ", len(data), " summits"
    conn.commit()


def populate_database():
    # for data from http://www.sotadata.org.uk/summits.aspx
    conn = sqlite3.connect("summits.db")
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
    c = 6378137 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return c #round(c, 3)


def visible_from_me(lat, lon, limit=1000, my_alt=400):
    # https://stackoverflow.com/a/7472230

    i = 0
    global cursor
    fud = math.pow(math.cos(math.radians(lat)), 2)
    cursor.execute("SELECT lat,lon,name,alt,viewrange FROM summits ORDER BY ((? - lat) * \
                   (? - lat) + (? - lon) * (? - lon) * ?) LIMIT ?",
                   [lat, lat, lon, lon, fud, limit])
    for e in cursor.fetchall():
        lat_ = e[0]
        lon_ = e[1]

        distance = haversine(lon_, lat_, lon, lat)
        # if distance to the mountain is less than visible range from the mountain - then we will see it.(?)
        if distance <= e[4] + view_range(my_alt):
            print i, e[2], e[3], haversine(lon_, lat_, lon, lat), e[4]
            i+=1


#populate_database_from_osm()
# saint bruno
lat, lon = 45.1841555, 5.7208091
# Pelvoux/@44.9030791,6.3736697
#lat, lon = 44.9030791, 6.3736697

visible_from_me(lat, lon)

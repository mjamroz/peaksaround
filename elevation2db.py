#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
from geo2vector import TifReader

class PopulateElevations:
    def __init__(self):
            self.conn = sqlite3.connect("summits.db")
            self.conn.text_factory = str
            self.c = self.conn.cursor()
            self.c.execute("SELECT lat,lon FROM summits")
            self.summits = self.c.fetchall()

    def create_table(self):
        try:
            self.c.execute("DROP TABLE elevations")
        except sqlite3.OperationalError:
            print "table not dropped"
        self.c.execute("CREATE TABLE IF NOT EXISTS elevations (id integer primary key, \
                lon float, lat float, ele integer)")
        self.c.execute("CREATE INDEX ele_lon ON elevations(lon)")
        self.c.execute("CREATE INDEX ele_lat ON elevations(lat)")
        self.c.execute("CREATE INDEX ele_alt ON elevations(ele)")
        self.c.execute("CREATE UNIQUE INDEX ele_one ON elevations(ele, lon, lat)")
        self.conn.commit()

    def populate(self, file_to_parse):
        delta = 0.01
        g = TifReader(file_to_parse)
        # LAT = Y = ~45

        for summit in self.summits:
            lat, lon = summit
            if g.in_the_range(lat, lon):
                #print lat, g.lat_range, lon, g.lon_range
                elevations = g.square(lon - delta, lon + delta, lat - delta, lat + delta)
                self.c.executemany("INSERT OR IGNORE INTO elevations(lon, lat, ele) VALUES(?,?,?)", elevations)
        self.conn.commit()



if __name__ == "__main__":
    d = PopulateElevations()
    d.create_table()
    for tif in ['srtm_37_03.tif', 'srtm_38_03.tif']:
        d.populate(tif)

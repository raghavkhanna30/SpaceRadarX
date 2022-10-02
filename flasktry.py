from flask import Flask
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from PIL import Image
import json
import urllib.request
from geopy.geocoders import Nominatim
import turtle

app = Flask(__name__)
@app.route("/")

def index():
   
    issimage = Image.open("iss.gif")
    fig = plt.figure(figsize=(7,6))
    while(True):
        url = 'http://api.open-notify.org/iss-now.json'
        response = urllib.request.urlopen(url)
        result = json.loads(response.read())

        location = result['iss_position']
        latiss = float(location['latitude'])
        loniss = float(location['longitude'])
        print('Latitude: ', latiss)
        print('Longitude: ', loniss)
        
        ocean_map = (plt.get_cmap('ocean'))(210)
        cmap = plt.get_cmap('gist_earth')

        # call the basemap and use orthographic projection at viewing angle
        m1 = Basemap(projection='ortho',
                lat_0=latiss,lon_0=loniss,resolution=None)

        # define map coordinates from full-scale globe
        map_coords_xy = [m1.llcrnrx,m1.llcrnry,m1.urcrnrx,m1.urcrnry]
        map_coords_geo = [m1.llcrnrlat,m1.llcrnrlon,m1.urcrnrlat,m1.urcrnrlon]

        #zoom proportion and re-plot map 
        zoom_prop = 2.0 # use 1.0 for full-scale map

        m = Basemap(projection='ortho',resolution='l',
                lat_0=latiss,lon_0=loniss,llcrnrx=-map_coords_xy[2]/zoom_prop,
                llcrnry=-map_coords_xy[3]/zoom_prop,urcrnrx=map_coords_xy[2]/zoom_prop,
                urcrnry=map_coords_xy[3]/zoom_prop)

        # coastlines, map boundary, fill continents/water, fill ocean, draw countries
        m.drawmapboundary(fill_color=ocean_map)
        m.fillcontinents(color=cmap(200),lake_color=ocean_map)
        m.drawcoastlines()
        m.drawcountries()

        # latitude/longitude line vectors
        lat_line_range = [-90,90]
        lat_lines = 8
        lat_line_count = (lat_line_range[1]-lat_line_range[0])/lat_lines

        merid_range = [-180,180]
        merid_lines = 8
        merid_count = (merid_range[1]-merid_range[0])/merid_lines

        m.drawparallels(np.arange(lat_line_range[0],lat_line_range[1],lat_line_count))
        m.drawmeridians(np.arange(merid_range[0],merid_range[1],merid_count))

        # scatter to indicate lat/lon point
        x,y = m(loniss,latiss)
        m.scatter(x,y,marker='o',color='#DDDDDD',s=3000,zorder=10,alpha=0.7,\
                edgecolor='#000000')
        m.scatter(x,y,marker='o',color='#000000',s=100,zorder=10,alpha=0.7,\
                edgecolor='#000000')

        plt.annotate(str("ISS Location"), xy=(x, y),  xycoords='data',
                    xytext=(-110, -10), textcoords='offset points',
                    color='k',fontsize=12,bbox=dict(facecolor='w', alpha=0.5),
                    arrowprops=dict(arrowstyle="fancy", color='k'))

        # save figure at 150 dpi and show it
        plt.savefig('ortho_zoom_example.png',dpi=150,transparent=True)
        return plt.show()

if __name__ == "__main__":
    app.start(host="127.0.0.1",port=8080,debug=True)
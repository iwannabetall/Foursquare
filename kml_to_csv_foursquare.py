#!/usr/bin/python # -*- coding: utf-8 -*-
from unidecode import unidecode
import csv
from xml.dom.minidom import parseString

###REMOVE THE NAME AND DESCRIPTION HEADERS AT TOP OF FILE OR RENAME THEM
#def findCentroidGivenKML(location):
#Read KML file as a string
file = open(kml_file)
data = file.read()
file.close()

#Parse that string into a DOM
dom = parseString(data)

#initialize latitude and longitude lists
latitudes = []
longitudes = []
places = []
description = []
checkindate = []
link = []

#Iterate through a collection of coordinates elements
for d in dom.getElementsByTagName('coordinates'):
    #Break them up into latitude and longitude
    coords = d.firstChild.data.split(',')
    longitudes.append(float(coords[0]))
    latitudes.append(float(coords[1]))

for d in dom.getElementsByTagName('name'):
	places.append(d.firstChild.data.encode('utf-8'))  #remove unicode

for d in dom.getElementsByTagName('description'):
	desc = d.firstChild.nextSibling.nextSibling
	if desc == None:
		desc = 'n/a'
	else: 
		desc = d.firstChild.nextSibling.nextSibling.data.encode('utf-8')
	description.append(desc)
	#description.append(d.firstChild.data.encode('utf-8'))
	
for d in dom.getElementsByTagName('a'):
	link.append(d.getAttribute("href").encode('utf-8'))

for d in dom.getElementsByTagName('published'):
	checkindate.append(d.firstChild.data.encode('utf-8'))

foursquaredata = []
#foursquaredata = array([places, checkindate, link, latitudes, longitudes, description])
filename = "foursquaredata.csv"
foursquaredata = np.column_stack([places,checkindate, link, latitudes, longitudes, description])  #concatenate columns 
with open(filename, "w") as f:
    writer = csv.writer(f, delimiter=",")
    #header of the data 
    writer.writerow(["Place", "Check in Date", "Link", "Latitude", "Longitude", "Description"])
    writer.writerows(foursquaredata)
#d.firstChild.nextSibling
#d.firstChild.nextSibling.firstChild.data.encode('utf-8')


'<Placemark><name>Sunflower</name><description>@<a href="https://foursquare.com/v/sunflower/4a8141daf964a520aef61fe3">Sunflower</a>- FINALLY HERE!! With Sonya and co</description><updated>Sun, 14 Aug 16 02:39:49 +0000</updated><published>Sun, 14 Aug 16 02:39:49 +0000</published><visibility>1</visibility><Point><extrude>1</extrude><altitudeMode>relativeToGround</altitudeMode><coordinates>-122.39748903309618,37.762526888561446</coordinates></Point></Placemark>'


    '''#find the centroid
    centerLatitude = sum(latitudes)/len(latitudes)
    centerLongitude = sum(longitudes)/len(longitudes)
    return ([centerLongitude,centerLatitude])
    from pykml import parser
from lxml import etree
from pykml.parser import Schema
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import GX_ElementMaker as GX
from xml.dom.minidom import parseString


kml_file = 'foursquare.kml'
kml_file = '4sq.kml'
with open(kml_file) as f:
    doc = parser.parse(f)

root = parser.fromstring(open('foursquare.kml', 'r').read())
print etree.tostring(doc, pretty_print=True)

print root.Folder.Placemark.Point.coordinates  #prints coordinates 

for d in root.getElementsByTagName('coordinates'):
	print d.Folder.Placemark.Point.coordinates	

'''
"""
GET X & Y coordinates from Salesforce report 
PURPOSE:  CSV file generated will be used in supportroute.py

Notes: modified for demo purposes.  API to get x/y takes time.  
	- Generate SF report only for new properties
	- append to exisiting file 
"""

import csv as csv
from geopy.geocoders import Nominatim
import time

#--------------------------------------------------------#
# 
#		Functions and Variables
#
#--------------------------------------------------------#

#init geolocator
geolocator = Nominatim()

class ImportCSVdata(object):
	def __init__(self, filename, dataframe):
		self.filename = filename
		self.dataframe = dataframe
		self.makedataframe()
		
	def makedataframe(self):
		readdata = csv.reader(open(self.filename,"r"))
		for row in readdata:
			self.dataframe.append(row)
		self.dataframe.pop(0)			#remover header, set to variable if needed
		return (self.dataframe)


#prepare address strings before calling geopy.geocoders
def geolocator_formatready(x):
	#Format each row for geolocator package
	newlist = []
	for i,row in enumerate(x):
		newrow =  ("\"{}, {}, {} {}\"".format(row[1],row[2],row[3],row[4]))
		newlist.append(newrow)
	return newlist


# extract 1 list with streetname & geocoordinates
def feedtogeolocator(x):
	coordlist = []
	for i, row in enumerate(x):
		for j, y in enumerate(streetnames):
			if i == j:
				coords = geolocator.geocode(row)
				row = (y, coords.latitude, coords.longitude)
				print (row)
				coordlist.append(row) 
	return (coordlist)


def csv_writer(data):
    with open("coordinatelist.csv", "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)


housedataframe = []

# in case report footer changes
report_footerrow = 6


#--------------------------------------------------------#
# 
#		Methods
#
#--------------------------------------------------------#

#Salesforce report format [ID][Street][City][State][Zip]
ImportCSVdata("houseaddresses.csv", housedataframe)

housedataframe = housedataframe[:-report_footerrow]

# 1st column in CSV file has identifiers for x & y
streetnames = list(x[1] for x in housedataframe)

# prepare list for geolocator
formatedlist = [("\"{}, {}, {} {}\"".format(row[1],row[2],row[3],row[4])) for i, row in enumerate(housedataframe)]

coordlist = feedtogeolocator(formatedlist)

csv_writer(coordlist)

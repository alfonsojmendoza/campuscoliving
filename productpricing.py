"""

PRICING OF NEW INVENTORY

PURPOSE:
	Room size and quality vary greatly in housing network. It is important to be consistent when pricing room prices. 
		- customers can get a sense of purpose for pricing, i.e. not arbitrarty, 'Campus put some careful
			 thought into why room is priced this much' 
		- Sales & Support that answer questions about why a room is priced as such have the data to back it up
		- Transparency

METHOD:
	Based on input from dept heads, the following points are important, in descending order.
		1) Square footage of individual room
		2) Amount of Shared Space
			- MORE shared space DECREASES range of room prices 
			- LESS shared space INCREASES range of room prices
		3) Room Amenities: no particular order, all variables relative to all rooms in 1 property
			- windows - more sunlight
			- relative location - away from common areas/noisy streets/ etc
			- closet size

"""

import csv as csv
import numpy as np
#import tkinter as tk 

onlineform = []

#  House details needed from Salesforce, change for each new house
house_rent = float(7500)
house_sqft = float(1900)
house_upmark = float(150)
membershipprice = float(150)

# Affects range of room prices, typically '0.03'
# 	Check & Balance for Marketing / Sales team  
weightpercent = float(0.03)

#Ops Team submits file with following info [Room Name][Room Sq Ft][Var 1][Var 2][Var 3]
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


# Prepping data from ops team
userinput = []
ImportCSVdata("elsie.csv", userinput)


#list of just roomnames
roomnames = list(x[0] for x in userinput)

#list withoutroomnames, used for calculations
roommeasurements = list(x[1:] for x in userinput)


#--------------------------------------------------------#
# baseprice ==
#		Main algorithm for calculating price of each room
#
#--------------------------------------------------------#
#variables used in algorithm
roomcount = len(roomnames)
roomdata = np.array(roommeasurements, dtype = float)	
roomvariable = roomdata[:,1:4].sum(axis = 1)	# Sum of Room Variable Scores
interiorspace = int(roomdata[:,:1].sum(axis = 0))	 # Sum of Room (sq ft)


baseprice = [((house_rent / house_sqft ) * (((house_sqft - interiorspace)/roomcount) + x[0] )) for x in roomdata]
baseprice = np.array(baseprice)


# Normalizing price so sum of rooms == total rent
sumproductnow = (baseprice * roomvariable).sum(axis = 0)

normalizedprice = (house_rent/(weightpercent*sumproductnow+house_rent)*
				(weightpercent* baseprice * roomvariable + baseprice))

normalizedprice = np.around(normalizedprice,decimals = -1)


#  Upmark of prices
publishedprice = normalizedprice + membershipprice

print ("\nRoom Name\t\tNormalized ($)\t\tPublished Price ($)")
for x,y,z in zip(normalizedprice,roomnames,publishedprice):
	print ("\t{}\t\t\t$ {} \t\t\t$ {}".format(y,x,z))
print ("\nSum of Calcuations:\t$ {} \t Monthly Rent:\t {}".format(normalizedprice.sum(axis = 0), house_rent))

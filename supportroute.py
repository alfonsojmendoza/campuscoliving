"""
SUPPORT ROUTE

PURPOSE:
	Staff typically visits a few houses/day to check in on community well being, maintenance issues, or routine inspections.
	**Demo code**  Edited for demo purposes/privacy of clients
  Generates itinerary for short distance between all locations.


"""
import csv as csv
from itertools import permutations


#--------------------------------------------------------#
# 
#		Functions and Variables
#
#--------------------------------------------------------#

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

masterhouselist = []

ImportCSVdata("housecoords.csv", masterhouselist)

#in case CSV file structure changes, only have to change this 
column_streetid = 0

# office coordinates
startpoint = [37.782255, -122.410508]

# variables stated.  GUI using tkinter for early end-user version
initialinput = ("AdressA", "AddressB", "AddressC", "AddressD", "AddressE")


#--------------------------------------------------------#
# 
#	Match User's input to database of location,x,y
#
#--------------------------------------------------------#

# create list matching userinput with x & y coordinates
matchedlist = [x for x in masterhouselist for y in initialinput if x[column_streetid] == y]

#save street ids to separate list
streetnames = list(x[column_streetid] for x in matchedlist)

#make list with just x & y coordinates
coordinates = list(x[1:3] for x in matchedlist)

#convert to integers
intcoordinates = [[float(i) for i in row] for row in coordinates]

#insert start point to list
intcoordinates.insert(0, startpoint)


#--------------------------------------------------------#
# 
# Find shortest distance by brute force
#	 - Fine for this applicationbecause locations visited are rarely > 5/day
#
#--------------------------------------------------------#

#  Source: Stackexchange @Caridorc 
# http://codereview.stackexchange.com/questions/81865/travelling-salesman-using-brute-force-and-heuristics

def distance(point1, point2):
    return (((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2) ** 0.5)

def total_distance(points):
    return sum([distance(point, points[index + 1]) for index, point in enumerate(points[:-1])])

def travelling_salesman(points, start = None):
    if start is None:
        start = points[0]
    return min([perm for perm in permutations(points) if perm[0] == start], key = total_distance)

sortedlist = travelling_salesman(intcoordinates)


#--------------------------------------------------------#
# 
#	Get Itinerary by matching sorted list to street name
#
#--------------------------------------------------------#

matchedlistintegers = [(a, b) for a, b in zip(streetnames,intcoordinates)]

itinerary = [x for y in sortedlist for x in matchedlistintegers  if x[1]== y]

print("Itinerary: Start Point = office")
for i, x in enumerate(itinerary):
	print("{}.\t{}".format(i+1, x[0]))





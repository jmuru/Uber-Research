# Joseph
# Tami
# CS591 project

import csv
import re
import gmplot
import itertools
from time import sleep
import multiprocessing as mp
from geopy.geocoders import Nominatim

'''
area codes to check taxis: 10035, 10029
heatmaps creation, find control
    uber not being used
    where taxis are being used
create radius around control

create taxi revenue function 
    isolate fare amount
difference in diffference both revenue and far 

Broad stats:
number of rides increase or decrease
'''
geolocator = Nominatim()

GLOBAL_REGEX = re.compile('([\d])+\w')
# importing the data files
def write(data, filename):
    fl = open(filename, 'w')
    writer = csv.writer(fl)
    for values in data:
        writer.writerow(values)
    fl.close()

def smaller(orig, small):
    i = 0
    for row in orig:
        if not i == 1 :
            newRow = [row[1],row[4],row[5],row[6],row[9],row[10],row[12],row[17]]
            small.append(newRow)
        i = i + 1

def readJoe(filename):
    data = []
    with open(filename) as file:
        r = csv.reader(file, delimiter=',')
        firstLine = True
        for row in r:
            if firstLine:
                firstLine = False
                continue
            else:
                data.append(row);
        return data

# for uber data
def longLatSmallReader(filename):
    dataLat = []
    dataLong = []
    with open(filename) as file:
        r = csv.reader(file, delimiter=',')
        for row in r:
            dataLat.append(float(row[0]))
            dataLong.append(float(row[1]))
        print len(dataLat)
        return (dataLat, dataLong)

def longLatSmallerWriter(data, filename):
    longLat = []
    for row in data:
        longLat.append([row[1], row[2]])
    fl = open(filename, 'w')
    writer = csv.writer(fl)
    for elem in longLat:
        writer.writerow(elem)
    fl.close()

def readIncrementUber(filename):
    data = []
    with open(filename) as file:
        fifthlines = itertools.islice(file, 2, None, 102)
        for row in fifthlines:
            data.append(row.split(','))
        return data

#for green taxi data
def readIncrementGreenTaxi(filename):
    data = []
    with open(filename) as file:
        fifthlines = itertools.islice(file, 3, None, 103)
        for row in fifthlines:
            data.append(row.split(','))
        print len(data)
        return data

# for taxi data
def readIncrementYellowTaxi(filename):
    data = []
    with open(filename) as file:
        fifthlines = itertools.islice(file, 5, None, 1005)
        for row in fifthlines:
            data.append(row.split(','))
        print len(data)
        return data

def longLatFilterGreen(data):
    filteredLat = []
    filteredLng = []
    for elem in data:
        filteredLat.append(float(elem[6]))
        filteredLng.append(float(elem[5]))
    return (filteredLat, filteredLng)

def longLatFilterYellow(data):
    filteredLatP = []
    filteredLngP = []
    # filteredLatD = []
    # filteredLngD = []
    for elem in data:
        filteredLatP.append(float(elem[6]))
        filteredLngP.append(float(elem[5]))
        # filteredLatD.append(float(elem[10]))
        # filteredLngD.append(float(elem[9]))
    return (filteredLatP, filteredLngP)

# create maps
def createHeatmap(lat, lng):
    gmap = gmplot.GoogleMapPlotter(40.7141667, -74.0063889, 10)
    gmap.heatmap(lat, lng)
    gmap.draw('heatmap.html')

def createPins(lat, lng):
    gmap = gmplot.GoogleMapPlotter(40.7141667, -74.0063889, 10)
    gmap.scatter(lat, lng, 'k', marker=True)
    gmap.draw('marker.html')

def findFromCoord(long, lat):
    coordString = str(long) + ", " + str(lat)
    coord = geolocator.reverse(coordString)
    return coord

def filterPostal(lat_list, lng_list, filename):
    fl = open(filename, 'w')
    writer = csv.writer(fl)
    for i in range(7, len(lat_list), 100):
         x = str(findFromCoord(lat_list[i], lng_list[i]))
         new_x = x.split(',')
         writer.writerow(new_x)
         sleep(1)
    fl.close()

# geolocation 
# x = str(findFromCoord(40.722300, -73.988700))
# num_x  = len(x.split(','))
# print int(x.split(',')[num_x - 2])
# TESTS: build the all of the data

# green taxi 2015

# janGreen2015 = readIncrementGreenTaxi('green-2015/green_tripdata_2015-01.csv')
# (janGLat, janGLng) = longLatFilterGreen(janGreen2015)
# febGreen2015 = readIncrementGreenTaxi('green-2015/green_tripdata_2015-02.csv')
# (febGLat, febGLng) = longLatFilterGreen(febGreen2015)
# marGreen2015 = readIncrementGreenTaxi('green-2015/green_tripdata_2015-03.csv')
# (marGLat, marGLng) = longLatFilterGreen(marGreen2015)
# aprGreen2015 = readIncrementGreenTaxi('green-2015/green_tripdata_2015-04.csv')
# (aprGLat, aprGLng) = longLatFilterGreen(aprGreen2015)
# mayGreen2015 = readIncrementGreenTaxi('green-2015/green_tripdata_2015-05.csv')
# (mayGLat, mayGLng) = longLatFilterGreen(mayGreen2015)
# junGreen2015 = readIncrementGreenTaxi('green-2015/green_tripdata_2015-06.csv')
# (junGLat, junGLng) = longLatFilterGreen(junGreen2015)

# yellow taxi 2015

janYellow2015 = readIncrementYellowTaxi('yellow-2015/yellow_tripdata_2015-01.csv')
(janY2015Lat, janY2015Lng) = longLatFilterYellow(janYellow2015)
# filterPostal(janY2015Lat, janY2015Lng, 'addresses/yellow-taxi-2015/janYellowLoc2015.csv')
# filterPostal(janY2015Lat, janY2015Lng, 'addresses/yellow15-treatment/jan15Treat.csv')
'''
janYellow2015 recorded
control
10035: 4 / 106 3.77%
treatment
11430:
'''
# febYellow2015 = readIncrementYellowTaxi('yellow-2015/yellow_tripdata_2015-02.csv')
# (febY2015Lat, febY2015Lng) = longLatFilterYellow(febYellow2015)
# filterPostal(febY2015Lat, febY2015Lng, 'addresses/taxi-2015/febYellowLoc2015.csv')
'''
febYellow2015 recorded
10035: 2 / 103 1.9%
'''
# marYellow2015 = readIncrementYellowTaxi('yellow-2015/yellow_tripdata_2015-03.csv')
# (marY2015Lat, marY2015Lng) = longLatFilterYellow(marYellow2015)
# filterPostal(marY2015Lat, marY2015Lng, 'addresses/taxi-2015/marYellowLoc2015.csv')
'''
marYellow2015 recorded
10035: 3/108 2.78%
'''
# aprYellow2015 = readIncrementYellowTaxi('yellow-2015/yellow_tripdata_2015-04.csv')
# (aprY2015Lat, aprY2015Lng) = longLatFilterYellow(aprYellow2015)
# filterPostal(aprY2015Lat, aprY2015Lng, 'addresses/taxi-2015/aprYellowLoc2015.csv')
'''
aprYellow2015 recorded
10035: 4/104 3.8%
10029: 1/104
'''
# mayYellow2015 = readIncrementYellowTaxi('yellow-2015/yellow_tripdata_2015-05.csv')
# (mayY2015Lat, mayY2015Lng) = longLatFilterYellow(mayYellow2015)
# filterPostal(mayY2015Lat, mayY2015Lng, 'addresses/taxi-2015/mayYellowLoc2015.csv')
'''
mayYellow2015 recorded
10035: 3/108 2.78%
10029: 1/108
'''
# junYellow2015 = readIncrementYellowTaxi('yellow-2015/yellow_tripdata_2015-06.csv')
# (junY2015Lat, junY2015Lng) = longLatFilterYellow(junYellow2015)
# filterPostal(junY2015Lat, junY2015Lng, 'addresses/taxi-2015/junYellowLoc2015.csv')
'''
junYellow2015 recorded
10035: 4/103 3.8%
10029: 2/103
'''

# yellow taxi 2009

# janYellow2009 = readIncrementYellowTaxi('yellow-2009/yellow_tripdata_2009-01.csv')
# (janY2009Lat, janY2009Lng) = longLatFilterYellow(janYellow2009)
# filterPostal(janY2009Lat, janY2009Lng, 'addresses/yellow-taxi-2009/janYellowLoc2009.csv')
'''
janYellow2009 recorded
10035: 4/116 3.4%
10029: 0/116
'''
# febYellow2009 = readIncrementYellowTaxi('yellow-2009/yellow_tripdata_2009-02.csv')
# (febY2009Lat, febY2009Lng) = longLatFilterYellow(febYellow2009)
# filterPostal(febY2009Lat, febY2009Lng, 'addresses/yellow-taxi-2009/febYellowLoc2009.csv')
'''
febYellow2009 recorded
10035: 2/110 1.8%
10029: 3/110
'''
# marYellow2009 = readIncrementYellowTaxi('yellow-2009/yellow_tripdata_2009-03.csv')
# (marY2009Lat, marY2009Lng) = longLatFilterYellow(marYellow2009)
# filterPostal(marY2009Lat, marY2009Lng, 'addresses/yellow-taxi-2009/marYellowLoc2009.csv')
'''
marYellow2009 recorded
10035: 5/118 4.23%
10029: 1/118
'''
# aprYellow2009 = readIncrementYellowTaxi('yellow-2009/yellow_tripdata_2009-04.csv')
# (aprY2009Lat, aprY2009Lng) = longLatFilterYellow(aprYellow2009)
# filterPostal(aprY2009Lat, aprY2009Lng, 'addresses/yellow-taxi-2009/aprYellowLoc2009.csv')
'''
aprYellow2009 recorded
10035: 6/117 5.1%
10029: 0/117
'''
# mayYellow2009 = readIncrementYellowTaxi('yellow-2009/yellow_tripdata_2009-05.csv')
# (mayY2009Lat, mayY2009Lng) = longLatFilterYellow(mayYellow2009)
# filterPostal(mayY2009Lat, mayY2009Lng, 'addresses/yellow-taxi-2009/mayYellowLoc2009.csv')
'''
mayYellow2009 recorded
10035: 2/122 1.7%

'''
# junYellow2009 = readIncrementYellowTaxi('yellow-2009/yellow_tripdata_2009-06.csv')
# (junY2009Lat, junY2009Lng) = longLatFilterYellow(junYellow2009)
# filterPostal(junY2009Lat, junY2009Lng, 'addresses/yellow-taxi-2009/junYellowLoc2009.csv')
'''
junYellow2009 recorded
10035: 2/118 1.7%
10029: 1/118
'''
# uber 2014
# (aprUber2014Lat, aprUber2014Lng) = longLatSmallReader('uber-2014/uber-april-2014.csv')
# (mayUber2014Lat, mayUber2014Lng) = longLatSmallReader('uber-2014/uber-may-2014.csv')
# (junUber2014Lat, junUber2014Lng) = longLatSmallReader('uber-2014/uber-june-2014.csv')
# (julyUber2014Lat, julyUber2014Lng) = longLatSmallReader('uber-2014/uber-july-2014.csv')
# (augUber2014Lat, augUber2014Lng) = longLatSmallReader('uber-2014/uber-aug-2014.csv')
# (septUber2014Lat, septUber2014Lng) = longLatSmallReader('uber-2014/uber-sept-2014.csv')

#yellow 2013
# janYellow2013 = readIncrementYellowTaxi('yellow-2013/yellow_tripdata_2013-01.csv')
# (janY2013Lat, janY2013Lng) = longLatFilterYellow(janYellow2013)
# filterPostal(janY2013Lat, janY2013Lng, 'addresses/yellow-taxi-2013/janYellowLoc2013.csv')
'''
janYellow2013 recorded
10035: 5 / 120 4.2%
'''
# febYellow2013 = readIncrementYellowTaxi('yellow-2013/yellow_tripdata_2013-02.csv')
# (febY2013Lat, febY2013Lng) = longLatFilterYellow(febYellow2013)
# filterPostal(febY2013Lat, febY2013Lng, 'addresses/yellow-taxi-2013/febYellowLoc2013.csv')
'''
febYellow2013 recorded
10035: 3 / 113 2.7%
'''
# marYellow2013 = readIncrementYellowTaxi('yellow-2013/yellow_tripdata_2013-03.csv')
# (marY2013Lat, marY2013Lng) = longLatFilterYellow(marYellow2013)
# filterPostal(marY2013Lat, marY2013Lng, 'addresses/yellow-taxi-2013/marYellowLoc2013.csv')
'''
marYellow2015 recorded
10035: 3/ 129 2.3%
'''
# aprYellow2013 = readIncrementYellowTaxi('yellow-2013/yellow_tripdata_2013-04.csv')
# (aprY2013Lat, aprY2013Lng) = longLatFilterYellow(aprYellow2013)
# filterPostal(aprY2013Lat, aprY2013Lng, 'addresses/yellow-taxi-2013/aprYellowLoc2013.csv')
'''
aprellow2015 recorded
10035: 2 / 124 1.6%
'''
# mayYellow2013 = readIncrementYellowTaxi('yellow-2013/yellow_tripdata_2013-05.csv')
# (mayY2013Lat, mayY2013Lng) = longLatFilterYellow(mayYellow2013)
# filterPostal(mayY2013Lat, mayY2013Lng, 'addresses/yellow-taxi-2013/mayYellowLoc2013.csv')
'''
mayYellow2015 recorded
10035: 3/ 109 2.8%
'''
# junYellow2013 =  readIncrementYellowTaxi('yellow-2013/yellow_tripdata_2013-06.csv')
# (junY2013Lat, junY2013Lng) = longLatFilterYellow(junYellow2013)
# filterPostal(junY2013Lat, junY2013Lng, 'addresses/yellow-taxi-2013/junYellowLoc2013.csv')
'''
mayYellow2015 recorded
10035: 1/ 119 0.8%
'''
# create maps





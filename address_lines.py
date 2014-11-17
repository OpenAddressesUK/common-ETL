#
# Open addresses ETL Common Library
# 
# Address Lines Parser Class
#
# Version       1.0 (Python) in progress
# Author        John Murray
# Licence       CC By SA
#
# Purpose       Parse, validate and extract elements from UK addresses
#

import re
from pprint import pprint
import csv
import string
import collections

class AddressLines:

    def __init__(self, cur):            # Instantiation - takes database connection
        self.address = []               # Initialise address list to empty
        self.pcarea = ''                # Initialise postcode area to null string
        self.lines = 0                  # Initialise number of elements to 0
        self.towns = {}                 # Initialise towns object to empty
        self.streets = {}               # Initialise street types
        self.townpos = [-1, -1]         # Position of town in address [line, subline, word]
        self.aons = []                  # Position of addressable objects within the address
        self.elements = collections.OrderedDict()   # Formatted address elements
        self.pcpoint = (0,0)            # Postcode coordinates
        self.cur = cur
        query = "SELECT `pcarea`, `town` FROM `Posttowns`;"
        self.cur.execute(query)
        nrecs = 0
        for row in self.cur.fetchall() :
            words = [w.translate(None,string.punctuation) for w in re.split(' |-',row[1])]
            key = words[0][:4]
            if row[0] not in self.towns:
                self.towns[row[0]] = {}
            if key not in self.towns[row[0]]:
                self.towns[row[0]][key] = []
            self.towns[row[0]][key].append([row[1],words])
            nrecs += 1
        # print "Records read: " + str(nrecs)
        # pprint(self.towns)
        
    def setAddress(self, address, pc):
        # self.address = address
        self.address = []
        for line in address:
            self.address.extend(line.split(","))
        self.pcarea = pc.getArea("S")
        self.pcpoint = pc.centroid
        self.postcode = pc.getPostcode("S")
        self.townpos = [-1, -1, -1]
        self.elements = {}
        
    def getTownKey(self,town):
        words = [w.translate(None,string.punctuation) for w in re.split(' |-',town.upper())]
        return [words[0][:4],words]
        
    def getTown(self):
        lineno = 0
        # Reverse search for town
        for i in range(len(self.address),0,-1):
            # print i
            words = re.findall(r"[\w']+",self.address[i-1])
            # print "Words"
            # print words
            for j in range(0,len(words)):
                keys = self.getTownKey(words[j])
                # print "Keys"
                # print keys
                if self.pcarea in self.towns:
                    if keys[0] in self.towns[self.pcarea]:
                        matchwords = 0
                        town = -1
                        # print self.towns[self.pcarea][keys[0]]
                        for k in range(0,len(self.towns[self.pcarea][keys[0]])):
                            if self.towns[self.pcarea][keys[0]][k][1][0] == keys[1][0]:
                                ntwords = len(self.towns[self.pcarea][keys[0]][k][1])
                                if ntwords > matchwords:
                                    m = 1
                                    for l in range(1,ntwords):
                                        if (j+l) < len(words) and words[j+l][:2].upper() == self.towns[self.pcarea][keys[0]][k][1][l][:2]:
                                            m += 1
                                    if m > matchwords:
                                        matchwords = m
                                        town = k
                                        self.townpos = [i-1, j]
                        if town > -1:  
                            self.elements['town'] = collections.OrderedDict()
                            self.elements['town']['name'] = self.towns[self.pcarea][keys[0]][town][0]
                            if j == 0:
                                self.address[i-1] = ''
                            else:
                                self.address[i-1] = string.join(words[0:j], " ")
                            for k in range (i,len(self.address)):
                                self.address[k] = ''
                            return self.towns[self.pcarea][keys[0]][town][0]
        
        return ''
        
    def getStreet(self):
        if self.pcpoint[0] > 0:
            query = "SELECT `Name`, `Centx`, `Centy` FROM `OS_Locator` WHERE `Name` > '' AND CONTAINS(`MBR25` ,POINT( "+str(self.pcpoint[0])+", "+str(self.pcpoint[1])+"));"
            self.cur.execute(query)
            max = len(self.address)
            streets = []
            streetlines = []
            centroids = []
            for street in self.cur.fetchall():
                for i in range(0,max):  # Look for number at start of word
                    if street[0] in self.address[i]:
                        if street[0] not in streets:
                            streets.append(street[0])
                            streetlines.append(i)
                            centroids.append([street[1], street[2]])
            # print self.address   
            # print streets
            # print centroids
            if len(streets) == 1:
                self.address[streetlines[0]] = self.address[streetlines[0]].replace(streets[0],"").strip()
                self.elements['street'] = collections.OrderedDict()
                self.elements['street']['name'] = streets[0]
                self.elements['street']['geometry'] = collections.OrderedDict()
                self.elements['street']['geometry']['type'] = 'Point'
                self.elements['street']['geometry']['coordinates'] = [centroids[0][1], centroids[0][0]]
                if streetlines[0] < (len(self.address) - 1):
                    if self.address[streetlines[0]+1] != '' and not any(char.isdigit() for char in self.address[streetlines[0]+1]):
                        self.elements['locality'] = collections.OrderedDict()
                        self.elements['locality']['name'] = self.address[streetlines[0]+1]
                        self.address[streetlines[0]+1] = ''
            elif len(streets) > 1:
                max = len(streets)
                if streets[max-1] in streets[max-2] and streetlines[max-1] == streetlines[max-2]:
                    self.elements['street'] = collections.OrderedDict()
                    self.elements['street']['name'] = streets[max-2]
                    self.elements['street']['geometry'] = collections.OrderedDict()
                    self.elements['street']['geometry']['type'] = 'Point'
                    self.elements['street']['geometry']['coordinates'] = [centroids[max-2][1], centroids[max-2][0]]
                    self.address[streetlines[max-2]] = self.address[streetlines[max-2]].replace(streets[max-2],"").strip()
                    if streetlines[max-2] < (len(self.address) - 1):
                        if self.address[streetlines[max-2]+1] != '' and not any(char.isdigit() for char in self.address[streetlines[max-2]+1]):
                            self.elements['locality'] = collections.OrderedDict()
                            self.elements['locality']['name'] = self.address[streetlines[max-2]+1]
                            self.address[streetlines[max-2]+1] = ''
                elif streets[max-2] in streets[max-1] and streetlines[max-2] == streetlines[max-1]:
                    self.elements['street'] = collections.OrderedDict()
                    self.elements['street']['name'] = streets[max-1]
                    self.elements['street']['geometry'] = collections.OrderedDict()
                    self.elements['street']['geometry']['type'] = 'Point'
                    self.elements['street']['geometry']['coordinates'] = [centroids[max-1][1], centroids[max-1][0]]
                    self.address[streetlines[max-1]] = self.address[streetlines[max-1]].replace(streets[max-1],"").strip()
                    if streetlines[max-1] < (len(self.address) - 1):
                        if self.address[streetlines[max-1]+1] != '' and not any(char.isdigit() for char in self.address[streetlines[max-1]+1]):
                            self.elements['locality'] = collections.OrderedDict()
                            self.elements['locality']['name'] = self.address[streetlines[max-1]+1]
                            self.address[streetlines[max-1]+1] = ''
                else:
                    self.elements['street'] = collections.OrderedDict()
                    self.elements['street']['name'] = streets[max-1] + ", " + streets[max-2]
                    self.elements['street']['geometry'] = collections.OrderedDict()
                    self.elements['street']['geometry']['type'] = 'Point'
                    self.elements['street']['geometry']['coordinates'] = [centroids[max-2][1], centroids[max-2][0]]
                    self.address[streetlines[max-1]] = self.address[streetlines[max-1]].replace(streets[max-1],"").strip()                    
                    self.address[streetlines[max-2]] = self.address[streetlines[max-2]].replace(streets[max-2],"").strip()
                    if streetlines[max-1] < (len(self.address) - 1):
                        if self.address[streetlines[max-1]+1] != '' and not any(char.isdigit() for char in self.address[streetlines[max-1]+1]):
                            self.elements['locality'] = collections.OrderedDict()
                            self.elements['locality']['name'] = self.address[streetlines[max-1]+1]
                            self.address[streetlines[max-1]+1] = ''
            # print self.address
            # print self.elements
                
        
    def getAons(self):
        self.aons = []
        if self.townpos[0] == -1:
            self.getTown()
        max = len(self.address)
        for i in range(0,max):      # Look for number at start of word
            if self.address[i] != '':
                words = self.address[i].split()
                for j in range(0,len(words)):
                    if words[j][0].isdigit():
                        self.aons.append([i,j,string.join(words[0:j]," "),words[j],string.join(words[j+1:]," ")])
        pos = 1
        if self.aons == []:
            self.aons.append([0,0,0,"",self.address[0],""])
        if len(self.aons) == 1:
            self.elements['paon'] = collections.OrderedDict()
            self.elements['paon']['name'] = (self.aons[0][3]+" "+self.aons[0][4]).strip()
            pos = self.aons[0][0] + 1
            if self.aons[0][0] > 0:
                self.elements['saon'] = collections.OrderedDict()
                self.elements['saon']['name'] = self.address[0]
        elif len(self.aons) >= 2:
            self.elements['paon'] = collections.OrderedDict()
            self.elements['paon']['name'] = (self.aons[1][3]+" "+self.aons[1][4]).strip()
            pos = self.aons[0][0] + 1
            self.elements['saon'] = collections.OrderedDict()
            self.elements['saon']['name'] = self.address[0].strip()
        return self.aons

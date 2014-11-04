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
        self.townpos = [-1, -1, -1]     # Position of town in address [line, subline, word]
        self.aons = []                  # Position of addressable objects within the address
        self.elements = collections.OrderedDict()   # Formatted address elements
        query = "SELECT `pcarea`, `town` FROM `Posttowns`;"
        cur.execute(query)
        nrecs = 0
        for row in cur.fetchall() :
            words = [w.translate(None,string.punctuation) for w in re.split(' |-',row[1])]
            key = words[0][:4]
            if row[0] not in self.towns:
                self.towns[row[0]] = {}
            if key not in self.towns[row[0]]:
                self.towns[row[0]][key] = []
            self.towns[row[0]][key].append([row[1],words])
            nrecs += 1
        print "Records read: " + str(nrecs)
        pprint(self.towns)
        
    def setAddress(self, address, pcarea):
        # self.address = address
        self.address = []
        for line in address:
            self.address.extend(line.split(","))
        self.pcarea = pcarea
        self.townpos = [-1, -1, -1]
        self.elements = {}
        
    def getTownKey(self,town):
        words = [w.translate(None,string.punctuation) for w in re.split(' |-',town.upper())]
        return [words[0][:4],words]
        
    def getTown(self):
        lineno = 0
        for line in reversed(self.address):
            lineno += 1
            sublines = line.split(",")
            sublineno = 0
            for subline in sublines:
                sublineno += 1
                words = re.findall(r"[\w']+",subline)
                # print "Words"
                # print words
                for i in range(0,len(words)):
                    keys = self.getTownKey(words[i])
                    # print "Keys"
                    # print keys
                    if self.pcarea in self.towns:
                        if keys[0] in self.towns[self.pcarea]:
                            matchwords = 0
                            town = -1
                            # print self.towns[self.pcarea][keys[0]]
                            for j in range(0,len(self.towns[self.pcarea][keys[0]])):
                                # print "loop j="+str(j)
                                # print self.towns[self.pcarea][keys[0]][j][0]
                                # print self.towns[self.pcarea][keys[0]][j][1]
                                if self.towns[self.pcarea][keys[0]][j][1][0] == keys[1][0]:
                                    ntwords = len(self.towns[self.pcarea][keys[0]][j][1])
                                    # print "ntwords ="+str(ntwords)
                                    if ntwords > matchwords:
                                        m = 1
                                        for k in range(1,ntwords):
                                            # print "loop k="+str(k)
                                            # print self.towns[self.pcarea][keys[0]][j][1][k]
                                            if (i+k) < len(words) and words[i+k][:2].upper() == self.towns[self.pcarea][keys[0]][j][1][k][:2]:
                                                m += 1
                                        if m > matchwords:
                                            matchwords = m
                                            town = j
                            if town > -1:
                                self.townpos = [len(self.address)-lineno, sublineno, i]
                                self.elements['town'] = self.towns[self.pcarea][keys[0]][town][0]
                                return self.towns[self.pcarea][keys[0]][town][0]
        
        return ''
        
    def getAons(self):
        self.aons = []
        if self.townpos[0] == -1:
            self.getTown()
        if self.townpos[0] == -1:
            max = len(self.address)
        else:
            max = self.townpos[0]
        for i in range(0,max):      # Look for number at start of word
            sublines = self.address[i].split(",")
            for j in range(0,len(sublines)):
                words = sublines[j].split()
                for k in range(0,len(words)):
                    if words[k][0].isdigit():
                        self.aons.append([i,j,k,string.join(words[0:k]," "),words[k],string.join(words[k+1:]," ")])
        pos = 1
        if self.aons == []:
            self.aons.append([0,0,0,"",self.address[0],""])
        if len(self.aons) == 1:
            self.elements['paon'] = (self.aons[0][3]+" "+self.aons[0][4]).strip()
            pos = self.aons[0][0] + 1
            if self.aons[0][0] > 0:
                self.elements['saon'] = self.address[0]
            if self.aons[0][5] != "":
                self.elements['street'] = self.aons[0][5]
            else:
                if (self.aons[0][0]+1) < max:
                    self.elements['street'] = self.address[self.aons[0][0]+1]
                pos = self.aons[0][0] + 2
        elif len(self.aons) >= 2:
            self.elements['paon'] = (self.aons[1][3]+" "+self.aons[1][4]).strip()
            pos = self.aons[0][0] + 1
            self.elements['saon'] = self.address[0].strip()
            if self.aons[1][5] != "":
                self.elements['street'] = self.aons[1][5].strip()
            else:
                self.elements['street'] = self.address[self.aons[1][0]+1].strip()
                pos = self.aons[0][0] + 2        
        if pos < max:
            if self.address[pos] > "":
                self.elements['locality'] = self.address[pos]
        return self.aons

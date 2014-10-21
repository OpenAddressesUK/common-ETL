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

class AddressLines:

    def __init__(self, towns='OA_Posttowns.csv'):        # Instantiation - takes list of strings as address argument
        self.address = []               # Initialise address list to empty
        self.pcarea = ''                # Initialise postcode area to null string
        self.lines = 0                  # Initialise number of elements to 0
        self.towns = {}                 # Initialise towns object to empty
        with open(towns, 'rb') as csvfile:
            townreader = csv.DictReader(csvfile)
            nrecs = 0
            for row in townreader:
                words = [w.translate(None,string.punctuation) for w in re.split(' |-',row['Posttown'])]
                key = words[0][:4]
                if row['Area'] not in self.towns:
                    self.towns[row['Area']] = {}
                if key not in self.towns[row['Area']]:
                    self.towns[row['Area']][key] = []
                self.towns[row['Area']][key].append([row['Posttown'],words])
                nrecs += 1
        # print "Records read: " + str(nrecs)
        # pprint(self.towns)
        
    def setAddress(self, address, pcarea):
        self.address = address
        self.pcarea = pcarea
        
    def getTownKey(self,town):
        words = [w.translate(None,string.punctuation) for w in re.split(' |-',town.upper())]
        return [words[0][:4],words]
        
    def getTown(self):
        for line in reversed(self.address):
            sublines = line.split(",")
            for subline in sublines:
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
                                return self.towns[self.pcarea][keys[0]][town][0]
        
        return ''

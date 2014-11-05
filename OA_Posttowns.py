# 
# Open addresses Common ETL Library
# Open addresses Extract Post Towns From Wikipedia
#
#
# Version       1.0 (Python) in progress
# Author        John Murray
# Licence       MIT
#
# Purpose       Script to Extract posttowns from Wikipedia
#

import ConfigParser
from HTMLParser import HTMLParser
import urllib
import urllib2
import csv
from bulkinsert import *

# Read database configuration from config file
config = ConfigParser.ConfigParser()
config.read("oa_alpha_etl.cnf")
username = config.get('database', 'username')
password = config.get('database', 'password')
hostname = config.get('database', 'hostname')
database = config.get('database', 'database')

dbConn = MySQLdb.connect(host=hostname,user=username,passwd=password,db=database)
cur = dbConn.cursor() 

query = "TRUNCATE TABLE  `Posttowns`;"
cur.execute(query)

fields = ["pcarea", "town"]

bi = BulkInsert(cur,"Posttowns",fields)

url = "http://en.wikipedia.org/wiki/List_of_post_towns_in_the_United_Kingdom"

class TownExtractor(HTMLParser):

    def reset(self):
        HTMLParser.reset(self)
        self.towns = []
        self.pcarea = ''
        self.towntable = False
        self.areatag = False
        self.towntag = False

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            attrs = dict(attrs)   # store attributes in object
            # print attrs
            if "class" in attrs:
                if attrs['class'] == "toccolours":
                    self.towntable = True
        if tag == "tr" and self.towntable:
            self.pcarea = ""
        if tag == "a" and self.towntable:
            attrs = dict(attrs)   # store attributes in object
            if "title" in attrs:
                if self.pcarea == "":
                    self.areatag = True
                else:
                    self.towntag = True
                    town = attrs['title'].split(",")[0].decode('ISO-8859-1').encode('ascii','ignore').upper()

    def handle_endtag(self, tag):
        if tag == "table":
            self.towntable = False
            
    def handle_data(self, data):
        if self.areatag:
            self.pcarea = data
            self.areatag = False
        if self.towntag: 
            self.towns.append([self.pcarea, data.decode('ISO-8859-1').encode('ascii','ignore').upper()])
            self.towntag = False
            
response = urllib2.urlopen(url)
html = response.read()

print "Parsing Wikipedia Page " + url

parser = TownExtractor()
parser.feed(html)

for t in parser.towns:
    bi.addRow(t)

bi.close()
dbConn.commit()
dbConn.close()

print str(len(parser.towns)) + " posttowns written to database."

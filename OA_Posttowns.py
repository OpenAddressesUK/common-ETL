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

from HTMLParser import HTMLParser
import urllib
import urllib2
import csv

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
            
csvout = open('OA_Posttowns.csv', 'w') 
writer = csv.writer(csvout, delimiter=',',quotechar='"', quoting=csv.QUOTE_ALL)
writer.writerow(['Area', 'Posttown'])

response = urllib2.urlopen(url)
html = response.read()

print "Parsing Wikipedia Page " + url

parser = TownExtractor()
parser.feed(html)

writer.writerows(parser.towns)

csvout.close()

print str(len(parser.towns)) + " posttowns written to database."

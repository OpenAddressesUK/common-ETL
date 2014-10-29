# 
# Open addresses Common ETL Library
# Open addresses Collect Raw Data
#
#
# Version       1.0 (Python) in progress
# Author        John Murray
# Licence       MIT
#
# Purpose       Script to Colect Bulk Open Data feeds
#

import ConfigParser
from HTMLParser import HTMLParser
import urllib
import urllib2
import zipfile
import MySQLdb

class LinkExtractor(HTMLParser):

    def reset(self):
        HTMLParser.reset(self)
        self.links      = []
        
    def setPattern(self,url,start,type):
        self.start = start
        self.type = type
        if "/" in url:
            self.base = url[0:url.rfind("/")] + "/"
        else:
            self.base = url + "/"

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attrs = dict(attrs)   # store attributes in object
            # print attrs
        if tag == "a" and "href" in attrs:
            href = attrs["href"]
            if href.lower().endswith("."+self.type) and (href.lower().startswith(self.start) or ("/"+self.start) in href.lower()):
                if not href.lower().startswith("http://") and not href.lower().startswith("https://"):
                    href = self.base + href
                self.links.append(href)
                
def collectData(cur,url,filestart,filetype):

    response = urllib2.urlopen(url)
    html = response.read()

    parser = LinkExtractor()
    parser.setPattern(url,filestart,filetype)
    parser.feed(html)
    
    for l in parser.links:
        file = l[l.rfind("/")+1:]
        response = urllib2.urlopen(l)
        meta = response.info()
        query = "SELECT * FROM `Files` WHERE `fileurl`='"+l+"' AND `size`='"+meta['Content-Length']+"' AND `modtime`='"+meta['Last-Modified']+"';"
        cur.execute(query)
        if cur.rowcount == 0:
            print "Downloading: "+l
            print urllib.urlretrieve(l, file)
            query = "INSERT INTO `Files`(`fileurl`, `size`, `modtime`) VALUES ('"+l+"','"+meta['Content-Length']+"','"+meta['Last-Modified']+"')"
            cur.execute(query)
            dbConn.commit()
            if filetype.lower() == 'zip':
                print "Unzipping: "+file
                with zipfile.ZipFile(file, "r") as z:
                    z.extractall()
        else:
            print "Unchanged: "+l
    
config = ConfigParser.ConfigParser()

config.read("oa_alpha_etl.cnf")
username = config.get('database', 'username')
password = config.get('database', 'password')
hostname = config.get('database', 'hostname')
database = config.get('database', 'database')

dbConn = MySQLdb.connect(host=hostname,user=username,passwd=password,db=database)
cur = dbConn.cursor() 

sources = config.get('sources', 'sources').split(",")

for s in sources:
    url = config.get(s, 'url')
    filestart = config.get(s, 'filestart')
    filetype = config.get(s, 'filetype')
    collectData(cur,url,filestart,filetype)
    
dbConn.close()
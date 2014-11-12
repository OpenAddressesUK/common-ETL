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
import fnmatch
import time

class LinkExtractor(HTMLParser):

    def reset(self):
        HTMLParser.reset(self)
        self.links      = []
        
    def setPattern(self,url,mask,type):
        self.mask = mask
        self.type = type
        if "/" in url:
            self.base = url[0:url.rfind("/")] + "/"
        else:
            self.base = url + "/"

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attrs = dict(attrs)   # store attributes in object
        if tag == "a" and "href" in attrs:
            href = attrs["href"]
            if "/" in href:
                file = href[href.rfind("/")+1:].lower()
            else:
                file = href.lower()
#            if href.lower().endswith("."+self.type) and (href.lower().maskswith(self.mask) or ("/"+self.mask) in href.lower()):
            if file.endswith("."+self.type) and fnmatch.fnmatch(file,self.mask):
                if not href.lower().startswith("http://") and not href.lower().startswith("https://"):
                    href = self.base + href
                self.links.append(href)
                
def collectData(cur,url,filemask,filetype,fileget):

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    response = opener.open(url)
    html = response.read()

    parser = LinkExtractor()
    parser.setPattern(url,filemask,filetype)
    parser.feed(html)
    
    links = parser.links
    
    files = []
    latest = 0
    
    for l in links:
        response = urllib2.urlopen(l)
        meta = response.info()
#       modtime = time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(meta['Last-Modified'],"%a, %d %b %Y %H:%M:%S %Z")) 
        modtime = time.strptime(meta['Last-Modified'],"%a, %d %b %Y %H:%M:%S %Z")
        files.append([l,meta['Content-Length'],modtime])
        if modtime > latest:
            latest = modtime
    
    for f in files:
        file = f[0][f[0].rfind("/")+1:]
        query = "SELECT * FROM `Files` WHERE `fileurl`='"+f[0]+"' AND `size`='"+f[1]+"' AND `modtime`='"+time.strftime('%Y-%m-%d %H:%M:%S',f[2])+"';"
        cur.execute(query)
        if cur.rowcount == 0:
            if fileget == 'all' or (fileget == 'latest' and f[2] >= latest):
                print "Downloading: "+f[0]
                print urllib.urlretrieve(f[0], file)
                query = "INSERT INTO `Files`(`fileurl`, `size`, `modtime`) VALUES ('"+f[0]+"','"+f[1]+"','"+time.strftime('%Y-%m-%d %H:%M:%S',f[2])+"')"
                cur.execute(query)
                dbConn.commit()
                if filetype.lower() == 'zip':
                    print "Unzipping: "+file
                    with zipfile.ZipFile(file, "r") as z:
                        z.extractall()
            else:
                print "Not latest: "+f[0]
        else:
            print "Unchanged: "+f[0]
    
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
    filemask = config.get(s, 'filemask')
    filetype = config.get(s, 'filetype')
    if config.has_option(s, 'get'):
        fileget = config.get(s, 'get')
    else:
        fileget = "all"
    collectData(cur,url,filemask,filetype,fileget)
    
dbConn.close()
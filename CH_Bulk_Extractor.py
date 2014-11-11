# 
# Open addresses Companies House ETL Library
# Open addresses Companies House ETL tool
#
#
# Version       1.0 (Python) in progress
# Author        John Murray
# Licence       MIT
#
# Purpose       Bulk extract of addresses from Companies House Data
#

import ConfigParser
import csv
import glob
from postcode_class import *
from address_lines import *
import sys
import json
import datetime
import time
import urllib
import urllib2
import MySQLdb

# Read api configuration from config file
config = ConfigParser.ConfigParser()
config.read("oa_alpha_etl.cnf")
apiurl = config.get('api', 'url')
apitoken = config.get('api', 'token')

# Read database configuration from config file
username = config.get('database', 'username')
password = config.get('database', 'password')
hostname = config.get('database', 'hostname')
database = config.get('database', 'database')

dbConn = MySQLdb.connect(host=hostname,user=username,passwd=password,db=database)
cur = dbConn.cursor() 

a = AddressLines(cur)

csvout = open('CompanyTowns.txt', 'wb') 
companywriter = csv.writer(csvout, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
companywriter.writerow(['Postcode', 'Town', 'Sector', 'Aons'])

for file in glob.glob("Basic*.csv"):
    start_time = time.time()
    print file
    nrecs = 0
    csvfile = open(file, 'rb')
    companyreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    companyreader.fieldnames = [field.strip() for field in companyreader.fieldnames]
    for row in companyreader:
        nrecs += 1
        # print row
        if (nrecs % 1000) == 0:
            print "Records read: " + str(nrecs)
            elapsed = time.time() - start_time
            # print str(elapsed) + " secs elapsed"
            # print str((60 * nrecs) / elapsed) + " recs/min"
        if 'RegAddress.PostCode' in row:
            if row['RegAddress.PostCode'] > '':
                pc = Postcode(row['RegAddress.PostCode'],cur)
                if pc.current != -1:
                    lines = [row['RegAddress.AddressLine1'], row['RegAddress.AddressLine2'], row['RegAddress.PostTown'], row['RegAddress.County']]
                    a.setAddress(lines,pc)
                    if a.getTown() != '':
                        # Future code for inference - not active in alpha
                        # try:
                        #    companywriter.writerow([pc.getPostcode("S"), a.getTown(), pc.getSector("S")])
                        # except:
                        #     print row
                        #    sys.exit("Sector failure")
                        a.getStreet()
                        a.getAons()
                        out = {}
                        out['address'] = a.elements
                        out['address']['postcode'] = pc.getPostcode("S")
                        # Next line for future use for inference
                        # out['address']['sector'] = pc.getSector("S")
                        out['provenance'] = {}
                        out['provenance']['executed_at'] = datetime.datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")
                        out['provenance']['url'] = "http://download.companieshouse.gov.uk/en_output.html"
                        out['provenance']['filename'] = file
                        out['provenance']['record_no'] = str(nrecs)
                        # print out
                        # print json.dumps(out, indent=1)
                        # print lines
                        post = {}
                        data = json.dumps(out, indent=1)
                        # print data
                        headers = { 'ACCESS_TOKEN' : apitoken }
                        url = apiurl
                        req = urllib2.Request(url, data, headers)
                        try: 
                            response = urllib2.urlopen(req)
                        except urllib2.HTTPError as e:
                           sys.exit("Aborted - Ingester API HTTP Error: " + str(e.code) + " - " + e.reason)
                        except URLError as e:
                           sys.exit("Aborted - Ingester API URL Error: " + str(e.code) + " - " + e.reason)
                        the_page = response.read()
    elapsed = time.time() - start_time
    print str(elapsed) + " secs elapsed"
    print str((60 * nrecs) / elapsed) + " recs/min"
    csvfile.close()
    
csvout.close()

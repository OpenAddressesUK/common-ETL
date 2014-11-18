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
import collections

# Store a list of addresses into the API
def storeAddresses(out):
    if len(out['addresses']) > 0:                # Check there is data to write
        data = json.dumps(out, indent=1)
        headers = { 'ACCESS_TOKEN' : apitoken }
        url = apiurl
        req = urllib2.Request(url, data, headers)
        ntries = 0
        while ntries < max_tries:
            try:
                response = urllib2.urlopen(req)
                the_page = response.read()
                time.sleep(10)
                break
            except urllib2.HTTPError as e:
                time.sleep(wait_min + wait_increment * ntries)
                ntries += 1
                err = e
                print "Warning - Ingester API HTTP Error encountered - retrying ("+str(ntries)+"): " + str(e.code) + " - " + e.reason
            except urllib2.URLError as e:
               sys.exit("Fatal error - Ingester API URL Error: " + str(e.code) + " - " + e.reason)
        if ntries >= max_tries:
            sys.exit ("Fatal error - Ingester API HTTP Error max tries reached ("+str(ntries)+")")

# Process a single file
def process_file(file):
    start_time = time.time()
    print file
    nrecs = 0

    # Load CSV file
    csvfile = open(file, 'rb')
    companyreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    companyreader.fieldnames = [field.strip() for field in companyreader.fieldnames]

    out = {}                            # Reset output buffer
    out['addresses'] = []

    for row in companyreader:
        nrecs += 1
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
                        address = collections.OrderedDict()
                        address['address'] = a.elements
                        address['address']['postcode'] = collections.OrderedDict()
                        address['address']['postcode']['name'] = pc.getPostcode("S")
                        address['address']['postcode']['geometry'] = collections.OrderedDict()
                        address['address']['postcode']['geometry']['type'] = 'Point'
                        address['address']['postcode']['geometry']['coordinates'] = [pc.centroid[1], pc.centroid[0]]
                        # Next line for future use for inference
                        # out['address']['sector'] = pc.getSector("S")
                        address['provenance'] = {}
                        address['provenance']['executed_at'] = datetime.datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")
                        address['provenance']['url'] = "http://download.companieshouse.gov.uk/en_output.html"
                        address['provenance']['filename'] = file
                        address['provenance']['record_no'] = str(nrecs)
                        # print out
                        # print json.dumps(out, indent=1)
                        # print lines
                        out['addresses'].append(address)

        if (nrecs % 100) == 0:          # Buffer full - send records to API
            print "Records read: " + str(nrecs)
            elapsed = time.time() - start_time
            print str(elapsed) + " secs elapsed"
            print str((60 * nrecs) / elapsed) + " recs/min"
            storeAddresses(out)         # Write records in buffer to API
            out = {}                    # Reset output
            out['addresses'] = []

    print "Records read: " + str(nrecs)
    elapsed = time.time() - start_time
    print str(elapsed) + " secs elapsed"
    print str((60 * nrecs) / elapsed) + " recs/min"
    storeAddresses(out)                 # Write remaining records in buffer
    csvfile.close()

# Main script

# Error timeout parameters
max_tries = 100                         # Maximum number of retries
wait_min = 1                            # First wait time (seconds)
wait_increment = 5                      # Wait time increment (seconds)

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
    process_file(file)

csvout.close()

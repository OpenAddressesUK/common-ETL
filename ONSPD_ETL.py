# 
# Open addresses ETL Common Library
# Open addresses ONSPD ETL tool
#
#
# Version       1.0 (Python) in progress
# Author        John Murray
# Licence       MIT
#
# Purpose       Extract elements from ONSPD table
#

import ConfigParser
import csv
import glob
import MySQLdb
import string
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

query = "TRUNCATE TABLE  `ONSPD`;"
cur.execute(query)
fields = ["pcds", "usertype", "EA", "NO", "osgrdind", "ctry", "current"]

bi = BulkInsert(cur,"ONSPD",fields)

for file in glob.glob("ONSPD*.csv"):
    print file
    nrecs = 0
    csvfile = open(file, 'rb')
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    reader.fieldnames = [field.strip() for field in reader.fieldnames]
    for row in reader:
        nrecs += 1
        # print row
        if (nrecs % 10000) == 0:
            print "Records read: " + str(nrecs)
        if 'oseast1m' in row:
            if row['oseast1m'] > '':
                if row['doterm'] > "":
                    current = '0'
                else:
                    current = '1'
                lines = [row['pcds'],row['usertype'], row['oseast1m'], row['osnrth1m'], row['osgrdind'], row['ctry'][0], current]
                bi.addRow(lines)
    print "Records read: " + str(nrecs)
    csvfile.close()
bi.close() 
dbConn.commit()
dbConn.close()

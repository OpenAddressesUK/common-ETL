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

ONSPD_fields = ["pcds", "usertype", "EA", "NO", "osgrdind", "ctry", "current"]

ONSPD_bi = BulkInsert(cur,"ONSPD",ONSPD_fields)

query = "TRUNCATE TABLE  `ONSPD_Changes`;"
cur.execute(query)

change_fields = ["curr_pcds", "term_pcds"]

change_bi = BulkInsert(cur,"ONSPD_Changes",change_fields)

ret_pcds = []
cur_pcds = []

for file in glob.glob("ONSPD*.csv"):
    print file
    nrecs = 0
    csvfile = open(file, 'rb')
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    reader.fieldnames = [field.strip() for field in reader.fieldnames]
    for row in reader:
        nrecs += 1
        if (nrecs % 10000) == 0:
            print "Records read: " + str(nrecs)
        if 'oseast1m' in row:
            if row['doterm'] > "":
                current = '0'
                if row['oseast1m'] > '':
                    ret_pcds.append((row['pcds'], row['oseast1m'], row['osnrth1m']))
            else:
                current = '1'
                if row['oseast1m'] > '':
                    cur_pcds.append((row['pcds'], row['oseast1m'], row['osnrth1m']))
            if row['oseast1m'] > '':
                lines = [row['pcds'], row['usertype'], row['oseast1m'], row['osnrth1m'], row['osgrdind'], row['ctry'][0], current]
            else:
                lines = [row['pcds'], row['usertype'], "NULL", "NULL", row['osgrdind'], row['ctry'][0], current]
            ONSPD_bi.addRow(lines)
    print "Records read: " + str(nrecs)
    csvfile.close()
ONSPD_bi.close() 
dbConn.commit()

print "Writing changes to database"
nrecs = 0
nwrit = 0
for term_pc in ret_pcds:
    nrecs += 1
    query = "SELECT `pcds` FROM `ONSPD` WHERE `current` = '1' AND `EA` = '" + term_pc[1] + "' AND `NO` = '" + term_pc[2] + "';"
    cur.execute(query)
    if (nrecs % 10000) == 0:
        print "Changes read: " + str(nrecs) + " written: " + str(nwrit)
    if cur.rowcount == 1:
        nwrit += 1
        for row in cur.fetchall():
           change_bi.addRow([row[0],term_pc[0]])
change_bi.close() 
dbConn.commit()
dbConn.close()

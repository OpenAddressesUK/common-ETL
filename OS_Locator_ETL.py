# 
# Open addresses ETL Common Library
# Open addresses Ordance Survey Locator Opendata ETL tool
#
#
# Version       1.0 (Python) in progress
# Author        John Murray
# Licence       CC By SA
#
# Purpose       Parse, validate and extract elements from UK addresses
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

query = "TRUNCATE TABLE  `OS_Locator`;"
cur.execute(query)

fields = ["Name", "Classification", "Centx", "Centy", "Minx", "Maxx", "Miny", "Maxy", "Settlement", "Locality", "Cou_Unit", "Local Authority", "Tile_10k", "Tile_25k", "Source"]

# basequery = "INSERT INTO OS_Locator(`Name`, `Classification`, `Centx`, `Centy`, `Minx`, `Maxx`, `Miny`, `Maxy`, `Settlement`, `Locality`, `Cou_Unit`, `Local Authority`, `Tile_10k`, `Tile_25k`, `Source`) "

bi = BulkInsert(cur,"OS_Locator",fields)

nrecs = 0

for file in glob.glob("OS*.txt"):
    print file

    csvfile = open(file, 'rb')
    reader = csv.reader(csvfile, delimiter=':', quoting=csv.QUOTE_NONE)
    
    for row in reader:
        nrecs += 1
        # print row
        if (nrecs % 10000) == 0:
            print "Records read: " + str(nrecs)
        bi.addRow(row)
    
        # query = basequery + "VALUES(" + string.join(["'" + field.replace("'","\\'") + "'" for field in row],",") + ");"
        # print query
        # cur.execute(query)

print "Records read: " + str(nrecs)        
bi.close() 
dbConn.commit()
dbConn.close()

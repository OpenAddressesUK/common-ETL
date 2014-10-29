# 
# Open addresses ETL Common Library
# Open addresses Extract Point From Point Collection Shapefile
#
#
# Version       1.0 (Python) in progress
# Author        John Murray
# Licence       MIT
#
# Purpose       Extract points and attributes from shapefile
#

import ConfigParser
import shapefile
import datetime
import glob
import unicodedata

from extract_shape_points import *
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

query = "TRUNCATE TABLE  `Settlements`;"
cur.execute(query)

Sett_fields = ["OS_Code", "Type", "Name", "Cym_Name", "Admin", "Cym_Admin", "Easting", "Northing"]

Sett_bi = BulkInsert(cur,"Settlements",Sett_fields)

for file in glob.glob("*.shp"):
    for p in getPoints(file):
        if p[1]['LEGEND'][0] != 'L':
            lines = [p[1]['CODE'], p[1]['LEGEND'][0]]
            # Convert escape sequences to Unicode and strip accents
            name = p[1]['NAME'].decode('ISO-8859-1').encode('ascii','ignore')
            admin = p[1]['ADMIN_NAME'].decode('ISO-8859-1').encode('ascii','ignore')
            if "/" in name:    # Welsh or Gaelic alternative
                lines.extend(name.split("/"))
            else:
                lines.extend([name,"NULL"])
            if "/" in admin:  # Welsh or Gaelic alternative
                lines.extend(admin.split("/"))
            else:
                lines.extend([admin,"NULL"])
            lines.extend(p[0])
            Sett_bi.addRow(lines)

Sett_bi.close() 
dbConn.commit()

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

import shapefile
import datetime

def getPoints(file):
    out = []
    sf = shapefile.Reader(file)
    points = sf.shapes()
    records = sf.records()
    fields = sf.fields
    for i in range(0,len(points)):
        if points[i].shapeType == 1:  # We only want points
            attributes = {}
            for j in range(0,len(records[i])):
                if fields[j+1][1] == 'C':   # Character field
                    attributes[fields[j+1][0]] = records[i][j].strip()
                elif fields[j+1][1] == 'N': # Numeric field
                    attributes[fields[j+1][0]] = records[i][j]
                elif fields[j+1][1] == 'D': # Date field
                    attributes[fields[j+1][0]] = str(datetime.date(records[i][j][0],records[i][j][1],records[i][j][2]))
            out.append([[points[i].points[0][0], points[i].points[0][1]],attributes])
    return out

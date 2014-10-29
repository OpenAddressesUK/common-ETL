#
# Open addresses ETL Common Library
# 
# Bulk Insert Class
#
# Version       1.0 (Python) in progress
# Author        John Murray
# Licence       MIT
#
# Purpose       Bulk insert items into a MySQl or MariaDB table
#
# Arguments:    database cursor, table name, list of fields, max =  maximum buffer (2000), ignore = ingore duplicate keys (false)
#

import MySQLdb
import string

class BulkInsert:

    def __init__(self, cur,table,fields,max=2000,ignore=False):        # Instantiation - pass database
        self.max_rows = max
        self.cursor = cur
        self.fields = fields
        self.table = table
        if ignore:
            self.type = "IGNORE "
        else:
            self.type = ""
        self.nrecs = 0
        self.bufrecs = 0
        self.values = []
        self.prefix = "INSERT "+self.type+"INTO `"+self.table+"` (" 
        self.prefix += string.join(["`" + field + "`" for field in fields],",")
        self.prefix += ") VALUES "
        
    def close(self):
        if self.bufrecs > 0:
            self.writeData()
            
    def addRow(self,row):
        self.values.append(row)
        self.nrecs += 1
        self.bufrecs += 1
        if (self.nrecs % self.max_rows) == 0:
            self.writeData()

    def writeData(self):
        query = self.prefix
        for i in range(0,len(self.values)):
            if i > 0:
                query += ", "
            query += "("
            for j in range(0,len(self.fields)):
                if j > 0:
                    query += ", "
                if isinstance(self.values[i][j], (int, long, float, complex)):  # Is numeric
                    query += "'" + str(self.values[i][j]) + "'"                
                elif self.values[i][j] == "NULL":
                    query += "NULL"
                elif self.values[i][j][0:12] == "GeomFromText":
                    query += self.values[i][j]
                else:
                    query += "'" + self.values[i][j].replace("'","\\'") + "'"
            query += ")"
        query += ";"
        self.cursor.execute(query)
        self.values = []
        self.bufrecs = 0

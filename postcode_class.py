#
# Open addresses ETL Common Library
# 
# Postcode Parser Class
#
# Version       1.0 (Python) in progress
# Author        John Murray
# Licence       CC By SA
#
# Purpose       Parse, validate and format full and partial UK postcodes
#

import re
from pprint import pprint

class Postcode:

    def __init__(self, postcode):   # Instantiation - takes postcode as a string argument
        self.postcode = postcode    # store the raw postcode
        self.area = ''              # Initialise area to null string
        self.district = ''          # Initialise district to null string
        self.suffix = ''            # Initialise suffix to null string
        self.sector = ''            # Initialise sector to null string
        self.walk = ''              # Initialise walk to null string
        self.level = 0              # Initialise the level to 0 (invalid)
        self.amended = 0            # Initialise amended 
        self.error = 0              # Initialise error code
        if len(postcode) == 0:      # Null string
            self.error = 1          # Set error flag to 1 (missing postcode)
            return                  # Do nothing
        if len(self.postcode) > 2 and self.postcode[0].isdigit():   # If at least 2 characters and starts with digit
            if self.postcode[0] == '0' and self.postcode[1] in ['L', 'X']:  # If starts with zero
                self.postcode = 'O' + self.postcode[1:] # Change to letter 'O'
                self.amended = 1    # Set amended flag to 1 (1st character changed from 0)
            if self.postcode[0] == '1' and self.postcode[1] in ['G', 'P', 'V']:  # If starts with one
                self.postcode = 'I' + self.postcode[1:] # Change to letter 'I'
                self.amended = 2    # Set amended flag to 2 (1st character changed from 1)
            if self.postcode[0] == '2' and self.postcode[1] == 'E': # If starts with two
                self.postcode = 'Z' + self.postcode[1:] # Change to letter 'Z'
                self.amended = 3    # Set amended flag to 3 (1st character changed from 2)
            if self.postcode[0] == '5':  # If starts with five
                self.postcode = 'S' + self.postcode[1:] # Change to letter 'S' 
                self.amended = 4    # Set amended flag to 4 (1st character changed from 5)
            if self.postcode[0] == '8':  # If starts with five
                self.postcode = 'B' + self.postcode[1:] # Change to letter 'S' 
                self.amended = 5    # Set amended flag to 5 (1st character changed from 8)
        if len(self.postcode) > 1 and self.postcode[1] == 0:    # If at least 2 characters and 2nd character is zero
            self.postcode = self.postcode[0] + 'O' + self.postcode[1:] # Change to letter 'O'
            self.amended = 6    # Set amended flag to 1 (2nd character changed from 0)
        if len(postcode) > 2 and postcode[0:2].upper() == 'CRO':    # If begins with legacy postcode CRO
            self.postcode = 'CR0' + self.postcode[3:]  # Change to letter 'CR0' 
            self.amended = 7        # Set amended flag to 7 (Legacy postcode CRO)        
        components = re.findall(r"[^\W\d_]+|\d+", self.postcode) # Split alpha and numeric components of the string and sicard dpaces
        c = len(components)         # Set the number if components
        if c >= 1:                  # Check first component if present
            if components[0].isalpha(): # Check 1st component is alpha    
                self.area = components[0]   # Store it as area
                self.level = 1      # Set the level to 1 (area)
            else:                   # Invalid postcode
                self.error = 2      # Set error flag to 2 (invalid first character)
                return              # Do nothing
        if c >= 2:                  # Check 2nd component if present
            if components[1].isdigit(): # Check second component is numeric
                if int(components[1]) < 100:    # If it's less than 100, assume it's a district
                    self.district = components[1]   # Store it as district
                    self.level = 2  # Set the level to 2 (district) 
                else:               # If it's greater than 100, assume sector is included
                    self.district = str(int(components[1])/10)  # Divide by 10 and take the dividend 
                    self.sector = str(int(components[1])%10)    # Divide by 10 and take the remainder
                    self.level = 3  # Set the level to 3 (sector)  
            else:
                self.error = 3      # Set error flag to 3 (invalid district)
                return              # Do nothing
        if c >= 3:                  # Check 3rd component if present
            if components[2].isdigit(): # If it's number
                self.sector = components[2] # Store it as sector
                self.level = 3      # Set the level to 3 (sector) 
            else:                   # Is alphabetic          
                if len(components[2]) == 1: # If single character assume it's a district suffix (London only)
                    self.suffix = components[2]     # Store it as suffix
                    self.level = 2  # Set the level to 2 (district) 
                else:               # Otherwise assume it's a walk 
                    self.district = str(int(components[1])/10)  # Split the district
                    self.sector = str(int(components[1])%10)    # Derive the sector
                    self.walk = components[2]   # Store as walk component
                    self.level = 5  # Set the level to 5 (fuil postcode)
        if c >= 4:                  # Check 4th component if present.
            if components[3].isdigit(): # If numeric  
                self.sector = components[3] # Store it as sector
                self.level = 3      # Set the level to 3 (sector)
            elif self.level == 3:   # Ensure sector is set
                if len(components[3]) == 1: # If single character, assume sub-walk
                    self.walk = components[3]   # Store as walk
                    self.level = 4  # Set the level to 4 (sub-walk)    
                else:               # Take as walk
                    self.walk = components[3]   # Store as walk
                    self.level = 5  # Set the level to 5 (fuil postcode)           
        if c >= 5:                  # Check 4th component if present.
            if components[4].isalpha() and self.level == 3: # Check it's alphabetic
                if len(components[4]) == 1: # If single character, assume sub-walk
                    self.walk = components[4]   # Store as walk
                    self.level = 4  # Set the level to 4 (sub-walk)  
                else:               # Assume full postcode
                    self.walk = components[4]   # Store as walk
                    self.level = 5  # Set the level to 5 (fuil postcode)  

    def getPostcode(self, format):  # Output a formatted postcode
        if self.level < 4:          # If incomplete
            return ''               # Do nothing
        if format == "U":           # Unformatted (no space)
            return self.area + self.district + self.suffix + self.sector + self.walk
        if format == "S":           # Single intervening space
            return self.area + self.district + self.suffix + ' ' + self.sector + self.walk
        if format == "7" or format == "8":  # Fixed length, left & right justified
            return (self.area + self.district + self.suffix).ljust(int(format)-3) + self.sector + self.walk
        if format == "B":           # Sort format with space padding
            return (self.area).ljust(2) + (self.district + self.suffix).zfill(2) + self.sector + self.walk
        if format == "H":           # Sort format with hyphen padding
            return (self.area).ljust(2,'-') + (self.district + self.suffix).zfill(2) + self.sector + self.walk
        else:                       # Default - return raw
            return self.postcode
            
    def getSector(self, format):    # Output a formatted postcode sector
        if self.level < 3:          # If incomplete
            return ''               # Do nothing
        if format == "U":           # Unformatted (no space)
            return self.area + self.district + self.suffix + self.sector
        if format == "S":           # Single intervening space
            return self.area + self.district + self.suffix + ' ' + self.sector
        if format == "5" or format == "6":  # Fixed length, left & right justified
            return (self.area + self.district + self.suffix).ljust(int(format)-3) + self.sector
        if format == "B":           # Sort format with space padding
            return (self.area).ljust(2) + (self.district + self.suffix).zfill(2) + self.sector
        if format == "H":           # Sort format with hyphen padding
            return (self.area).ljust(2,'-') + (self.district + self.suffix).zfill(2) + self.sector
        return ''                   # Default - return raw
        
    def getDistrict(self, format):  # Output a formatted postcode district
        if self.level < 2:          # If incomplete
            return ''               # Do nothing
        if format == "B":           # Sort format with space padding
            return (self.area).ljust(2) + (self.district + self.suffix).zfill(2)
        if format == "H":           # Sort format with hyphen padding
            return (self.area).ljust(2,'-') + (self.district + self.suffix).zfill(2)
        return self.area + self.district + self.suffix  # Default
        
    def getArea(self, format):      # Output a formatted postcode district
        if self.level < 1:          # If incomplete
            return ''               # Do nothing
        if format == "B":           # Sort format with space padding
            return (self.area).ljust(2)
        if format == "H":           # Sort format with hyphen padding    
            return (self.area).ljust(2,'-')
        return self.area            # Default

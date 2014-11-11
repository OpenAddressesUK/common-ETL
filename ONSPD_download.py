import traceback
import urllib2
import zipfile
import datetime
import os

releases = [
    'NOV',
    'AUG',
    'MAY',
    'FEB'
]

year = datetime.datetime.now().year

file = None
filename = None
while file == None:
    for release in releases:
        url = "https://geoportal.statistics.gov.uk/Docs/PostCodes/ONSPD_{0}_{1}_csv.zip".format(release,year)
        try:
            release = "ONSPD_{0}_{1}".format(release,year)
            file = urllib2.urlopen(url)
            break
        except:
            None
    year -= 1

output = open(release + "_csv.zip",'wb')
output.write(file.read())
output.close()

with zipfile.ZipFile(release + "_csv.zip", 'r') as datazip:
    file = datazip.open("Data/{0}_UK.csv".format(release))
    output = open(release + ".csv",'wb')
    output.write(file.read())
    output.close()
    
os.remove(release + "_csv.zip")
import urllib2
import zipfile
import os

filenames = [
    'BasicCompanyData-2014-11-01-part1_5.zip',
    'BasicCompanyData-2014-11-01-part2_5.zip',
    'BasicCompanyData-2014-11-01-part3_5.zip',
    'BasicCompanyData-2014-11-01-part4_5.zip',
    'BasicCompanyData-2014-11-01-part5_5.zip'
]

for filename in filenames:
    url = 'http://download.companieshouse.gov.uk/' + filename
    file = urllib2.urlopen(url)
    output = open(filename,'wb')
    output.write(file.read())
    output.close()
    with zipfile.ZipFile(filename, 'r') as datazip:
        datazip.extractall()
    os.remove(filename)

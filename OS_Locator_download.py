import urllib2

filenames = [
    "OS_Locator2014_2_OPEN_xaa.txt",
    "OS_Locator2014_2_OPEN_xab.txt",
    "OS_Locator2014_2_OPEN_xac.txt",
    "OS_Locator2014_2_OPEN_xad.txt"
]

for filename in filenames:
    try:
        url = "http://openaddressesuk.org/OS_Locator/" + filename
        file = urllib2.urlopen(url)
        output = open(filename,'wb')
        output.write(file.read())
        output.close()
    except:
        None
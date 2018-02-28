import datetime
from datetime import date, time, timedelta
import urllib.request
import re
import os

logurl = "https://s3.amazonaws.com/tcmg476/http_access_log" 
logfile = "locallog.txt"

#downloads file if file is not already downloaded
def getFile():
    if not os.path.exists(logfile):
        print("Downloading log file. Please wait.")
        urllib.request.urlretrieve(logurl, "locallog.txt")
    else:
        print("File is downloaded, parsing now.")

#parses through file
def parseFile():
    openlog = open("locallog.txt")
    
    totalrequests = 0
    errorcount = 0
    errors = []    
    monthcount = {"Jan": 0, "Feb": 0, "Mar": 0, "Apr": 0, "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0, "Dec": 0}

    for line in openlog:
        totalrequests += 1
        lineparts = re.split(".*\[([^:]*):(.*) \-[0-9]{4}\] \"([A-Z]+) (.+?)( HTTP.*\"|\") ([2-5]0[0-9]) .*", line)
        if len(lineparts) >= 7:
            #regex worked
            print(lineparts)
        else:
            #regex did not work
            errorcount += 1
            print("Error parsing line: Line added to errors list")
            errors.append(line)
    
    print("Over the time period represented in the log there were ", totalrequests, "requests.")


#main method
def main():
    getFile()
    parseFile()

#runs program
if __name__ == "__main__":
    main()
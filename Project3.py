import datetime
from datetime import date, time, timedelta
import urllib.request
import re
import os

logurl = "https://s3.amazonaws.com/tcmg476/http_access_log" 
logfile = "locallog.log"


#downloads file if file is not already downloaded
def getFile():
    if not os.path.exists(logfile):
        print("Downloading log file. Please wait.")
        urllib.request.urlretrieve(logurl, "locallog.log")
    else:
        print("File is downloaded, parsing now.")

#parses through file
def parseFile():
    openlog = open("locallog.log", "w")
    
    totalrequests = 0
    errors = []

    for line in openlog:
        totalrequests += 1
        lineparts = re.split(".*\[([^:]*):(.*) \-[0-9]{4}\] \"([A-Z]+) (.+?)( HTTP.*\"|\") ([2-5]0[0-9]) .*", openlog)
    
    print("Over the time period represented in the log there were ", totalrequest, "requests.")


#main method
def main():
    getFile()
    parseFile()

#runs program
if __name__ == "__main__":
    main()
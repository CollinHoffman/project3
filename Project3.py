import datetime
from datetime import date, time, timedelta
import urllib.request
import os

logurl = "https://s3.amazonaws.com/tcmg476/http_access_log" 
logfile = "log.txt"

#regex for later use ".*\[([^:]*):(.*) \-[0-9]{4}\] \"([A-Z]+) (.+?)( HTTP.*\"|\") ([2-5]0[0-9]) .*"

#downloads file if file is not already downloaded
def getFile():
    if not os.path.exists(logfile):
        print("Downloading log file. Please wait.")
        urllib.request.urlretrieve(logurl, "log.txt")
    #if file exists, the file is opened.
    else:
        file=open("log.txt")


def parseFile():


def main():
    getFile()
    parseFile()


if __name__ == "__main__":
    main()
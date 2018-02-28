from datetime import datetime, date, time, timedelta
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

#parses through file
def parseFile():
    print("File is downloaded, parsing now.")
    openlog = open("locallog.txt")
    
    totalrequests = 0
    errorcount = 0
    errors = []    
    monthcount = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0} #months of the year starting with january at 1
    daycount = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0} #days of the week starting with 0 as monday
    failcount = 0
    redirectcount = 0
    successcount = 0

    #splits the next read line into usable parts
    for line in openlog:
        totalrequests += 1
        lineparts = re.split(".*\[([^:]*):(.*) \-[0-9]{4}\] \"([A-Z]+) (.+?)( HTTP.*\"|\") ([2-5]0[0-9]) .*", line)
        if len(lineparts) >= 7:
            #regex worked
            #day and month counter
            dt = datetime.strptime(lineparts[1], "%d/%b/%Y")
            daycount[dt.weekday()] += 1
            monthcount[dt.month] += 1

            #status code counters
            if lineparts[7] == '200':
                successcount += 1
            elif lineparts[7] == '300':
                redirectcount += 1
            else:
                failcount += 1
        else:
            #regex did not work
            errorcount += 1
            errors.append(line)
    
    print("Over the time period represented in the log there were ", totalrequests, "requests and ", round(((errorcount/total)*100),2),"percent of the requests were faulty")
    print("There were ", successcount, " successful request, ", failcount, " failed requests, and ", redirectcount, " redirected requests.")

    #print the amount of logs for each day
    for d in daycount:
        print("There were ", daycount[d], " requests on the day ", d, " over the period represented.")

    #print the amount of logs for each month
    for m in monthcount:
        print("There were ", monthcount[m], " requests on the month ", m, " over the period represented.")


    openlog.close()


#main method
def main():
    getFile()
    parseFile()

#runs program
if __name__ == "__main__":
    main()
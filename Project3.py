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
    filecount = {"index.html": 0}

    #dictionary of month file names
    monthfile = {1: "Jan.txt", 2: "Feb.txt", 3: "Mar.txt", 4: "Apr.txt", 5: "May.txt", 6: "Jun.txt", 7: "Jul.txt", 8: "Aug.txt", 9: "Sep.txt", 10: "Oct.txt", 11: "Nov.txt", 12: "Dec.txt"}

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
            
            #writes the line to proper month file
            if not os.path.exists(monthfile[dt.month]):
                file = open(monthfile[dt.month], "w")
                file.write(line)
                file.close()
            else:
                file = open(monthfile[dt.month], "a")
                file.write(line)
                file.close()

            #status code counters
            if lineparts[7] == '200':
                successcount += 1
            elif lineparts[7] == '300':
                redirectcount += 1
            else:
                failcount += 1

            #counts most called files
            if lineparts[4] in filecount:
                filecount[lineparts[4]] += 1
            else:
                filecount[lineparts[4]] = 1
        else:
            #regex did not work
            errorcount += 1
            errors.append(line)
    
    print("Over the time period represented in the log there were ", totalrequests, "requests and ", round(((errorcount/totalrequests)*100),2),"percent of the requests were faulty")
    print(round(((successcount/totalrequests)*100),2)," percent of requests were successful, ", round(((failcount/totalrequests)*100),2), " percent of requests failed, and ", round(((redirectcount/totalrequests)*100),2), " percent of requests were redirected.")

    #print the amount of logs for each day
    for d in daycount:
        print("There were ", daycount[d], " requests on the day ", d, " over the period represented.")

    #print the amount of logs for each month
    for m in monthcount:
        print("There were ", monthcount[m], " requests on the month ", m, " over the period represented.")

    #finds the most request file
    mostrequested = None
    mostcount = filecount[2]
    for filer, count in filecount.items():
        if count > mostcount:
            mostrequested = filer
            mostcount = filecount[filer]
    print("The most requested file was ", mostrequested, "with ", mostcount, "requests.")

    leastrequested = None
    leastcount = filecount[2]
    for filer, count in filecount.items():
        if count < leastcount:
            leastrequested = filer
            leastcount = filecount[filer]
    print("The least requested file was ", leastrequested, "with ", leastcount, "requests.")

    #closes all open files
    openlog.close()


#main method
def main():
    getFile()
    parseFile()

#runs program
if __name__ == "__main__":
    main()
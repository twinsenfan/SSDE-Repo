__author__ = 'tfan'

import time
import os
from datetime import datetime
import sys

#Variable holds starting time of script
TimeLowerboundary = datetime.now()

#variable holds the upper limit of the incident time when query
TimeUpperboundary = 0

#Variable holds total running time
Totalruntime = datetime.now()

#Variable holds number of iteration
IterationNum = 0

#Define log file checking function
def Logfilechecking (str):

    if os.path.exists('./Scriptlog.log') == False:

        #Create a log file if does not exist, indicate script run for 1st time
        Log_file = open('Scriptlog.log','w')
        text = "%s -- New log file created" %TimeLowerboundary
        print ("File does not exist, creating new log file")
        print (text)
        Log_file.writelines(text)
        text = "\n%s -- Script started first time" %TimeLowerboundary
        Log_file.writelines(text)
        Log_file.close()

    else:

        #Log file exists, writing script start time
        Log_file = open('Scriptlog.log','a')
        text = "\n%s -- Script started" %TimeLowerboundary
        Log_file.writelines(text)
        print (text)
        Log_file.close()

#End of log file checking function

#call for function to check the log file, pass current time as parameter
Logfilechecking(TimeLowerboundary);

#Infite loop that fire up the query in a configurable interval, changing the sleep timer(in sec)
while True:
    try:
        #To sleep 5 seconds
        time.sleep(5)
        TimeUpperboundary = datetime.now()

        #Print out time interval, replace the SQL query here
        print (TimeLowerboundary, TimeUpperboundary)

        #Re-assign low with upper value to move on to next iteration
        TimeLowerboundary = TimeUpperboundary

        #Keep record of number of loop
        IterationNum += 1

    except KeyboardInterrupt:
        print ("Ctrl-C detected, script terminated.")
        Log_file = open('Scriptlog.log','a')
        text = "\n%s -- Script terminated by Ctrl-C" %TimeLowerboundary
        Log_file.writelines(text)
        text = "\n%s -- Script fired up %s times in %s " %(TimeLowerboundary ,IterationNum, TimeUpperboundary - Totalruntime)
        Log_file.writelines(text)
        print ("Script fired up %s times in %s " %(IterationNum, TimeUpperboundary - Totalruntime))
        Log_file.close()
        sys.exit()


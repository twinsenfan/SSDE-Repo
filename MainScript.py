__author__ = 'tfan'

import pypyodbc
import time
import os
from datetime import datetime
import sys

#Temp variables to hold connection string
Server = '10.239.117.65'
Username = 'sa'
Password = 'websense#123'

#User configurable setting
#Variable holds delay timer in seconds between each iteration
DelayTimer = 30
#No other variables should be changed by user

#Variable holds starting time of script
TempTimelower = datetime.now()
TimeLowerboundary = TempTimelower.strftime('%Y-%m-%d %H:%M:%S')

#variable holds the upper limit of the incident time when query
TimeUpperboundary = 0

#Variable holds total running time
TempTotalruntime = datetime.now()
Totalruntime = TempTotalruntime.strftime('%Y-%m-%d %H:%M:%S')

#Variable holds number of iteration
IterationNum = 0

#Define log file checking function
def Logfilechecking (str):

    if os.path.exists('./Scriptlog.log') == False:

        #Create a log file if does not exist, indicate script run for 1st time
        Log_file = open('Scriptlog.log','w')
        text = "%s -- New log file created" %str
        print ("File does not exist, creating new log file")
        print (text)
        Log_file.writelines(text)
        text = "\n%s -- Script started first time" %str
        Log_file.writelines(text)
        Log_file.close()

    else:

        #Log file exists, writing script start time
        Log_file = open('Scriptlog.log','a')
        text = "\n%s -- Script started" % str
        Log_file.writelines(text)
        print (text)
        Log_file.close()
#End of log file checking function

#Define log file insert function, this will write query result to log file
def Logfilewrite (str):

        Log_file = open('Scriptlog.log','a')
        text = "\n%s -- Script started" % str
        Log_file.writelines(text)
        print (text)
        Log_file.close()
#End of log file write function

#Defination of the DBQuery function with passing parameters, SQL IP, Username and password
def SQLQuery (arg1, arg2, arg3, arg4, arg5):
    #Variable holds the name of online_active partition
    partition = 0

    # Get a connection to MSSQL ODBC DSN via pypyodbc, and assign it to conn
    conn= pypyodbc.connect(driver='{SQL Server}', server='%s' % arg1, database='wbsn-data-security', uid='%s' % arg2, pwd='%s' % arg3)

    # Give me a cursor so I can operate the database with the cursor
    cur = conn.cursor()

    # Select current active-online partition
    cur.execute('''select PARTITION_INDEX from dbo.PA_EVENT_PARTITION_CATALOG WHERE STATUS='ONLINE_ACTIVE' ''')

    for d in cur.description:
        print (d[0], end=" ")

    for row in cur.fetchall():
        for field in row:
            Partition = field
            #print (field, end=" ")
            print (Partition)

        print ('')



    cur.execute('''
         SELECT [APP_version]
                ,PA_EVENTS_%s.ID
                ,[STATUS]
                ,[ACTION_TYPE]
                ,[DESTINATIONS]
                ,[ATT_NAMES]
                ,[SUBJECT]
                ,PA_MNG_USERS.COMMON_NAME
                ,[POLICY_CATEGORIES]
                ,[ANALYZED_BY]
                ,[INSERT_DATE]

          FROM dbo.PA_EVENTS_%s, [dbo].[PA_MNG_USERS]
          WHERE PA_EVENTS_%s.SOURCE_ID = PA_MNG_USERS.ID AND
                dbo.PA_EVENTS_%s.INSERT_DATE <  '%s'AND
                dbo.PA_EVENTS_%s.INSERT_DATE >  '%s' ''' % (Partition, Partition, Partition, Partition,arg5,Partition, arg4))

    # Print the table headers (column descriptions)
    for d in cur.description:
        print (d[0], end=" ")

    # Start a new line
    print ('')

    # Print the table, one row per line
    for row in cur.fetchall():
        for field in row:
            print (field, end=" ")

        print ('')

    # I have done all the things, you can leave me and serve for others!

    cur.close()
    conn.close()
    return
#End of SQLQuery

#call for function to check the log file, pass current time as parameter
Logfilechecking(TimeLowerboundary);

#Infite loop that fire up the query in a configurable interval, changing the sleep timer(in sec)
while True:
    try:
        #To sleep 5 seconds
        time.sleep(DelayTimer)

        TempTimeUpper = datetime.now()
        TimeUpperboundary=TempTimeUpper.strftime('%Y-%m-%d %H:%M:%S')

        #Print out time interval, replace the SQL query here
        print (TimeLowerboundary, TimeUpperboundary)

        #Calling SQL query to output content
        SQLQuery(Server,Username,Password, TimeLowerboundary, TimeUpperboundary)

        #Re-assign low with upper value to move on to next iteration
        TimeLowerboundary = TimeUpperboundary

        #Keep record of number of loop
        IterationNum += 1

    except KeyboardInterrupt:
        print ("Ctrl-C detected, script terminated.")
        Log_file = open('Scriptlog.log','a')
        text = "\n%s -- Script terminated by Ctrl-C" %TimeLowerboundary
        Log_file.writelines(text)
        text = "\n%s -- Script fired up %s times, terminated at %s " %(TimeLowerboundary, IterationNum, TimeUpperboundary)
        Log_file.writelines(text)
        print("Script fired up %s times, terminated at %s " %(IterationNum,TimeUpperboundary))
        Log_file.close()
        sys.exit()




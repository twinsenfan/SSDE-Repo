__author__ = 'tfan'

import pypyodbc
import time
import os
from datetime import datetime
import sys
import socket
import getpass
from datetime import date
from datetime import timedelta

#Temp variables to hold connection string
Server = ''
Username = ''
Password = ''
Range = ''

#Variable holds incident ID
incidentID = ''


#Variable holds total number of incident processed
Totalincident = 0

#Variable holds starting time of script
TimeUpperboundary = date.today()

#variable holds the upper limit of the incident time when query
TimeLowerboundary = ''

#Define log file checking function
def Logfilechecking (str):

    if os.path.exists('./Scriptlog.log') == False:

        #Create a log file if does not exist, indicate script run for 1st time
        Log_file = open('Scriptlog.log','w')
        text = "%s -- New log file created" %str
        print ("File does not exist, creating new log file")

        #[Debug]: enable logging debug
        #print (text)
        Log_file.writelines(text)
        text = "\n%s -- Script started first time" %str
        Log_file.writelines(text)
        Log_file.close()

    else:

        #Log file exists, writing script start time
        Log_file = open('Scriptlog.log','a')
        text = "\n%s -- Script started" % str
        Log_file.writelines(text)

        #[Debug] Print text for debug purpose, turn off
        #print (text)

        Log_file.close()
#End of log file checking function

#Define log file insert function, this will write query result to log file, the input is a time stamp and string
def Logfilewrite (str1):

        Log_file = open('Scriptlog.log','a')
        text = "\n %s" % (str1)
        Log_file.writelines(text)
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

    #for d in cur.description:

        #[Debug]: print out column name
        #print(d[0], end=" ")

    for row in cur.fetchall():
        for field in row:
            Partition = field

            #print (field, end=" ")

            # [Debug]: print current partition name
            #print (Partition)

        print('')



    cur.execute('''
         SELECT PA_EVENTS_%s.ID
                ,PA_MNG_USERS.common_name
                ,[DESTINATIONS]
                ,[SUBJECT]
                ,[ATT_NAMES]
                ,[POLICY_CATEGORIES]
                ,CASE PA_EVENTS_%s.ACTION_TYPE
						WHEN 1 THEN 'Action=Audited'
						WHEN 100 THEN 'Action=Quarantined'
						WHEN 2 THEN 'Action=Blocked'
						WHEN 3 THEN 'Action=Encrypted'
 						WHEN 4 THEN 'Action=Released'
						WHEN 5 THEN 'Action=Run Command'
						WHEN 6 THEN 'Action=Permitted'
						WHEN 7 THEN 'Action=Notify'
						WHEN 8 THEN 'Action=Endpoint Confirm Abort'
						WHEN 9 THEN 'Action=Endpoint Confirm Continue'
						WHEN 10 THEN 'Action=Endpoint Run Command'
						WHEN 11 THEN 'Action=Drop attachments'
						WHEN 13 THEN 'Action=Encrypt with Password'
				END
                ,PA_RP_SERVICES.DESCRIPTION

          FROM dbo.PA_EVENTS_%s, [dbo].[PA_MNG_USERS], PA_RP_SERVICES
          WHERE PA_EVENTS_%s.status = 9 and PA_EVENTS_%s.SOURCE_ID = PA_MNG_USERS.ID AND
                dbo.PA_EVENTS_%s.INSERT_DATE <=  '%s'AND
                dbo.PA_EVENTS_%s.INSERT_DATE >=  '%s'AND PA_EVENTS_%s.SERVICE_ID = PA_RP_SERVICES.ID ''' % (Partition, Partition, Partition, Partition, Partition, Partition, arg5, Partition,arg4, Partition))

    # Print the table headers (column descriptions)
    for d in cur.description:
        # [Debug]: print out column header
        print(d[0], end=" ")

    # Start a new line
    print('')

    message = ''
    history = ''

    # Print the table, one row per line
    for row in cur.fetchall():
        n = 0


        for field in row:
            if n == 0:
                message = message  + 'IncidentID=%s' % field
                incidentID = field

            elif n == 1:
                message = message + ', src=%s' % field

            elif n == 2:
                message = message + ', dst=%s' % field

            elif n == 3:
               message = message  + ', subject=%s' % field

            elif n == 4:
                message = message  + ', trigger=%s' % field

            elif n == 5:
                message = message  + ', policy=%s' % field

            elif n == 7:
                message = message  + ', channel=%s' % field

            else:
                message = message  + ', %s' % field

            n += 1

            #[Debug] Uncomment this to debug each field to change output format
            #print(field)

        #[Debug]print out constructed message to screen, same as the one output to file
        print(message)

        #[Debug]: Write the entry to log file as well
        Logfilewrite(message)

        # Cursor to get the incident history
        Historycur = conn.cursor()

        Historycur.execute('''
         SELECT [Event_ID]
                ,[Task_performed]
                ,[Comments]
                ,[Admin_name]
                ,[Update_date]

          FROM dbo.PA_EVENT_History_%s
          WHERE Event_id = %s ''' % (Partition, incidentID))

        for line in Historycur.fetchall():
            j = 0

            for field in line:
                if j == 0:
                    history = history + 'History: %s, ' % field
                elif j < 4:
                    history = history + '%s, ' % field
                else:
                    history = history + '%s' % field

                j += 1

            #history = history  + ' '
            print(history)
            #[Debug]: Write the entry to log file as well
            Logfilewrite(history)

            history = ''

        #[Debug] print out number of record for each calling of SQL function
        #print('Value of j is ', j)

        message = ''
        Logfilewrite(message)

        print('')

    # I have done all the things, you can leave me and serve for others!

    cur.close()
    Historycur.close()
    conn.close()

#End of SQLQuery

#call for function to check the log file, pass current time as parameter
Logfilechecking(TimeLowerboundary)

#define command line validation
total = len(sys.argv)
#[Debug]: print out total number of args passed to command
#print ("The total numbers of args passed to the script: %d " % total)

#checking length of cmd string, exit and prompt syntax
if total != 5:
    print ("Error, incorrect Syntax!")
    print ("Usage: Script <SQL Server IP> <SQL Username> <Password> <Date Range> ")
    sys.exit()

else:
    #Ask for password when syntax is correct and continue the rest of program
    Server = str(sys.argv[1])
    Username =str(sys.argv[2])
    Password = str(sys.argv[3])
    #Password = getpass.getpass(prompt='Enter password for %s: ' % str(sys.argv[3]))
    Range = int(sys.argv[4])

    #[Debug]: Print out password, this should be comment out
    #print('You entered:', Password)

    #Clear the screen
    os.system('cls')
    print('Syslog script started:')


    #calculate current date
    TimeUpperboundary = date.today()

    #calcualte date by minus the input interval from command line
    TimeLowerboundary=date.today() - timedelta(Range)

    #[DEBUG]: Print out start time and end time
    print('Time:' , TimeLowerboundary, TimeUpperboundary)

    #Calling SQL query to output content
    SQLQuery(Server, Username, Password, TimeLowerboundary, TimeUpperboundary)

    #Print total incident processed in this loop
    #print('Total incident processed: ', Totalincident)






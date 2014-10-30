__author__ = 'tfan'

import pypyodbc
import datetime
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

    if os.path.exists('./Output.csv') == False:

        #Create a log file if does not exist, indicate script run for 1st time
        Log_file = open('Output.csv', 'w')
        #text = "%s -- New log file created" %str
        #print ("File does not exist, creating new log file")

        #[Debug]: enable logging debug
        #print (text)
        #Log_file.writelines(text)
        #text = "\n%s -- Script started" %str
        #Log_file.writelines(text)

        #text = "\n%s Incident ID, Date-Time, History, Comments, History Performed,Source, Destination, Action, Channel " %str
        #Log_file.writelines(text)

        Log_file.close()

    else:

        #Log file exists, writing script start time
        Log_file = open('Output.csv','a')
        #text = "\n%s -- Script started" % str
        #Log_file.writelines(text)

        #text = "\n%s Incident ID, Date-Time, History, Comments, History Performed, Source, Destination, Action, Channel " %str
        #Log_file.writelines(text)

        #[Debug] Print text for debug purpose, turn off
        #print (text)

        Log_file.close()
#End of log file checking function

#Define log file insert function, this will write query result to log file, the input is a time stamp and string
def Logfilewrite (str1):

        Log_file = open('Output.csv','a')
        text = "\n %s" % (str1)
        Log_file.writelines(text)
        Log_file.close()
#End of log file write function

#Defination of the DBQuery function with passing parameters, SQL IP, Username and password
def SQLQuery (arg1, arg2, arg3, arg4, arg5):
    #Variable holds the name of online_active partition
    partition = 0
    tempstring = ''

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
                ,DETECT_DATE_TS
                ,DETECT_DATE_TZ
                ,PA_MNG_USERS.common_name
                ,POLICY_CATEGORIES
                ,PA_RP_SERVICES.DESCRIPTION
                ,[DESTINATIONS]
                ,CASE SENSITIVITY_ID
                        WHEN 1 THEN 'High'
                        WHEN 2 THEN 'Medium'
                        WHEN 3 THEN 'Low'
                 END

                ,CASE PA_EVENTS_%s.ACTION_TYPE
						WHEN 1 THEN 'Audited'
						WHEN 100 THEN 'Quarantined'
						WHEN 2 THEN 'Blocked'
						WHEN 3 THEN 'Encrypted'
 						WHEN 4 THEN 'Released'
						WHEN 5 THEN 'Run Command'
						WHEN 6 THEN 'Permitted'
						WHEN 7 THEN 'Notify'
						WHEN 8 THEN 'Endpoint Confirm Abort'
						WHEN 9 THEN 'Endpoint Confirm Continue'
						WHEN 10 THEN 'Endpoint Run Command'
						WHEN 11 THEN 'Drop attachments'
						WHEN 13 THEN 'Encrypt with Password'
				 END
                ,TOTAL_MATCHES
                ,TOTAL_SIZE
                ,CASE STATUS
                      WHEN 1 THEN 'New'
                      WHEN 3 THEN 'In Process'
                      WHEN 5 THEN 'Closed'
                 END
                ,PA_REPO_USERS.Long_Name

          FROM dbo.PA_EVENTS_%s, [dbo].[PA_MNG_USERS], PA_RP_SERVICES, PA_REPO_USERS
          WHERE PA_EVENTS_%s.SOURCE_ID = PA_MNG_USERS.ID AND PA_MNG_USERS.GUID = PA_REPO_USERS.ID AND
                dbo.PA_EVENTS_%s.INSERT_DATE <=  '%s'AND
                dbo.PA_EVENTS_%s.INSERT_DATE >=  '%s'AND PA_EVENTS_%s.SERVICE_ID = PA_RP_SERVICES.ID ''' % (Partition, Partition, Partition, Partition, Partition, arg5, Partition,arg4, Partition))

    # Print the table headers (column descriptions)
    #for d in cur.description:
        # [Debug]: print out column header
        #print(d[0], end=" ")

    # Start a new line
    print('')

    message = ''

    # Print the table, one row per line
    for row in cur.fetchall():
        n = 0
        incidentID  = ''
        for field in row:

            #print('N is ', n)
            if n == 0:

                #print('Message 0 is ', message)
                message = message  + '%s' % field
                incidentID  = field
                #print('Field is ', field)
                #print('Message 0 result is ', message)

            elif n == 12:
                #Do something to remove the , and replace with " "
                #tempstring = field
                #print('Message 12 is ',message)
                message = message  + ', %s' % field.replace(",", " ")

            else:
                #print('Message else entry is ', message)
                message = message  + ', %s' % field
                #print('Field else is ', field)
                #print('Message else result is ', message)

            n += 1

            #[Debug] Uncomment this to debug each field to change output format
            #print(field)

        #[Debug]print out constructed message to screen, same as the one output to file
        #print(incidentID)
        #print(message)

        # Give me a cursor so I can operate the database with the cursor
        curGroup = conn.cursor()

        curGroup.execute('''
                        select
                        (Stuff ( ( Select ' - ' + PA_REPO_GROUPS.NAME from PA_REPO_GROUPS where ID in
				            (Select PA_REPO_ENTRY_GROUPS.GROUP_ID from PA_REPO_ENTRY_GROUPS where PA_REPO_ENTRY_GROUPS.ENTRY_ID =
                    					(Select GUID from PA_MNG_USERS where ID =
							                    (SELECT SOURCE_ID
								                        FROM [dbo].[PA_EVENTS_%s]
								                        where [dbo].[PA_EVENTS_%s].ID = %s
							                    )
					                    )
				            )FOR XML PATH('')) ,1,2,''))''' % (Partition, Partition, incidentID))

        #this is to append group name to the result
        for row1 in curGroup.fetchall():
            for field in row1:

                message = message  + ', %s' % field

            print(message)

        #[Debug]: Write the entry to log file as well
        Logfilewrite(message)

        #[Debug] print out number of record for each calling of SQL function
         #print('Value of j is ', j)

        #produce a new line in the log file to split each incident
        message = ''
        Logfilewrite(message)

        print('')

    # I have done all the things, you can leave me and serve for others!

    cur.close()
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
    print("Error, incorrect Syntax!")
    print("Usage: Script <SQL Server IP> <SQL Username> <Password> <Date Range> ")
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
    print('Incident output script started:')

    #calculate current date
    #this is the realy one passed to SQL to search data include today (actually today date + 2 so we have today's data)
    TimeUpperboundary = date.today() + (timedelta(2))

    #this is the one displayed in log and screen for the actual date
    tempTimeUpperboundary = date.today()

    #calcualte date by minus the input interval from command line
    TimeLowerboundary=date.today() - (timedelta(Range))

    #[DEBUG]: Print out start time and end time
    print('Incident interval', TimeLowerboundary, '---', tempTimeUpperboundary)
    text = 'Incident interval %s --- %s' % (TimeLowerboundary, tempTimeUpperboundary)
    Logfilewrite(text)

    text = "Incident ID, Incident Time,Incident Time Zone, Source, Policies, Channel,Destination, Severity, Action, Maximum Matches, Transaction Size, Status, OU, Group Membership"
    Logfilewrite(text)

    #Calling SQL query to output content
    SQLQuery(Server, Username, Password, TimeLowerboundary, TimeUpperboundary)








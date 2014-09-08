__author__ = 'tfan'

import pypyodbc
import time
import os
from datetime import datetime
import sys
import socket
import getpass

#Temp variables to hold connection string
Server = ''
Username = ''
Password = ''

#Variable holds the name of online_active partition
Partition = '20140824'

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
        text = "\n%s" % (str1)
        Log_file.writelines(text)
        Log_file.close()
#End of log file write function

#Defination of the DBQuery function with passing parameters, SQL IP, Username and password
def SQLQuery (arg1, arg2, arg3):

    # Get a connection to MSSQL ODBC DSN via pypyodbc, and assign it to conn
    conn= pypyodbc.connect(driver='{SQL Server}', server='%s' % arg1, database='wbsn-data-security', uid='%s' % arg2, pwd='%s' % arg3)

    # Give me a cursor so I can operate the database with the cursor
    cur = conn.cursor()

    cur.execute('''
         SELECT PA_EVENTS_%s.EXTERNAL_ID
                ,[STATUS]
                ,CASE PA_EVENTS_%s.ACTION_TYPE
						WHEN 1 THEN 'act=Audited'
						WHEN 100 THEN 'act=Quarantined'
						WHEN 2 THEN 'act=Blocked'
						WHEN 3 THEN 'act=Encrypted'
 						WHEN 4 THEN 'act=Released'
						WHEN 5 THEN 'act=Run Command'
						WHEN 6 THEN 'act=Permitted'
						WHEN 7 THEN 'act=Notify'
						WHEN 8 THEN 'act=Endpoint Confirm Abort'
						WHEN 9 THEN 'act=Endpoint Confirm Continue'
						WHEN 10 THEN 'act=Endpoint Run Command'
						WHEN 11 THEN 'act=Drop attachments'
						WHEN 13 THEN 'act=Encrypt with Password'
				END
				,PA_MNG_USERS.common_name
                ,[DESTINATIONS]
                ,[BREACH_CONTENT]
                ,[POLICY_CATEGORIES]
                ,PA_RP_SERVICES.DESCRIPTION

          FROM dbo.PA_EVENTS_%s, [dbo].[PA_MNG_USERS], [dbo].PA_RP_SERVICES
          WHERE PA_EVENTS_%s.SOURCE_ID = PA_MNG_USERS.ID AND PA_EVENTS_%s.SERVICE_ID = PA_RP_SERVICES.ID

                 ''' % (Partition,Partition, Partition, Partition, Partition))

    # Print the table headers (column descriptions)
    for d in cur.description:
        # [Debug]: print out column header
        print(d[0], end=" ")

    # Start a new line
    print('')

    message = 'CEF:0|Websense|Data Security|7.8|'

    j = 0

    # Print the table, one row per line
    for row in cur.fetchall():
        n = 0

        for field in row:
            #print(field)
            if n == 0 :
                message = message  + '%s|' % field

            elif n == 1:
                message = message  + 'DLP Incident|1|'

            elif n == 3:
                message = message  + ' dvc=%s ' % field

            elif n == 4:
                message = message  + 'duser=%s ' % field

            elif n == 5:
                message = message  + ' fname=%s ' % field

            elif n == 6:
                message = message  + ' cat=%s ' % field

            elif n == 7:
                message = message  + ' sourceServiceName=%s ' % field

            else:
                message = message  + '%s' % field

            #print(message + '%s' % field, end="|")
            #print(message)

            n += 1



        #[Debug]: Write the entry to log file as well
        Logfilewrite(message)
        #print(message)

        message = 'CEF:0|Websense|Data Security|7.8|'

        print('')

    # I have done all the things, you can leave me and serve for others!

    cur.close()
    conn.close()

#End of SQLQuery


#define command line validation
total = len(sys.argv)
#[Debug]: print out total number of args passed to command
print("The total numbers of args passed to the script: %d " % total)

#checking length of cmd string, exit and prompt syntax
if total != 4:
    print("Error, incorrect Syntax!")
    print("Usage: Script <SQL Server IP> <SQL Username> <Password>")
    sys.exit()

else:
    #Ask for password when syntax is correct and continue the rest of program
    Server = str(sys.argv[1])
    Username =str(sys.argv[2])
    Password = str(sys.argv[3])
    #Password = getpass.getpass(prompt='Enter password for %s: ' % str(sys.argv[3]))

    #[Debug]: Print out password, this should be comment out
    #print('You entered:', Password)

    #Clear the screen
    os.system('cls')

    #Calling SQL query to output content
    SQLQuery(Server, Username, Password)






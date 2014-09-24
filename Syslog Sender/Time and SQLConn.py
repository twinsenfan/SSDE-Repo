__author__ = 'tfan'

import pypyodbc
import time
from datetime import datetime

#Variable holds starting time of script
TimeLowerboundary = '2014-06-01 01:15:14'

#variable holds the upper limit of the incident time when query
TempUppertime = datetime.now()
TimeUpperboundary =TempUppertime.strftime('%Y-%m-%d %H:%M:%S')

Server = '10.239.117.65'
Username = 'sa'
Password = 'websense#123'

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


#    cur.execute('''
 #         SELECT [APP_version]
 #               ,PA_EVENTS_%s.ID
  #              ,[STATUS]
   #             ,[ACTION_TYPE]
    #            ,[DESTINATIONS]
     #           ,[ATT_NAMES]
      #          ,[SUBJECT]
       #         ,PA_MNG_USERS.COMMON_NAME
        #        ,[POLICY_CATEGORIES]
         #       ,[ANALYZED_BY]

          #FROM dbo.PA_EVENTS_%s, [dbo].[PA_MNG_USERS]
          #WHERE PA_EVENTS_%s.SOURCE_ID = PA_MNG_USERS.ID AND
                #dbo.PA_EVENTS_%s.LOCAL_DETECT_TS <  '2014-07-01 00:15:14'  AND
                #dbo.PA_EVENTS_%s.LOCAL_DETECT_TS >  '2014-02-01 00:15:14' '''
  #            %(Partition ,Partition ,Partition,Partition,Partition))

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
                ,[Local_detect_TS]

          FROM dbo.PA_EVENTS_%s, [dbo].[PA_MNG_USERS]
          WHERE PA_EVENTS_%s.SOURCE_ID = PA_MNG_USERS.ID AND
                dbo.PA_EVENTS_%s.LOCAL_DETECT_TS <  '%s'AND
                dbo.PA_EVENTS_%s.LOCAL_DETECT_TS >  '%s' ''' % (Partition, Partition, Partition, Partition,arg5,Partition, arg4) )

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

print (TimeLowerboundary, TimeUpperboundary)

SQLQuery(Server,Username,Password, TimeLowerboundary, TimeUpperboundary)
__author__ = 'tfan'

__author__ = 'Home'

import pypyodbc
import time
from datetime import datetime

i = datetime.now()
print (i.hour)

print (i.minute)

print ("Current date & time = %s" % i)

j = datetime.now()

print (j.strftime('%Y-%m-%d %H:%M:%S'))

#                  Get a connection to MSSQL ODBC DSN via pypyodbc, and assign it to conn

conn= pypyodbc.connect(driver='{SQL Server}', server='10.239.117.65', database='wbsn-data-security', uid='sa', pwd='websense#123')


#                  Give me a cursor so I can operate the database with the cursor

cur = conn.cursor()

#                  Select current active-online partition
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

      FROM dbo.PA_EVENTS_%s, [dbo].[PA_MNG_USERS]
      WHERE PA_EVENTS_%s.SOURCE_ID = PA_MNG_USERS.ID'''
      %(Partition ,Partition ,Partition))


#                  Print the table headers (column descriptions)

for d in cur.description:
    print (d[0], end=" ")


#                  Start a new line

print ('')


#                  Print the table, one row per line

for row in cur.fetchall():
    for field in row:
        print (field, end=" ")
    print ('')


#                  I have done all the things, you can leave me and serve for others!

cur.close()
conn.close()

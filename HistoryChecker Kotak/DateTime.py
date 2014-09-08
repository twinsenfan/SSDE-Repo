__author__ = 'Home'

import pypyodbc
import time
from datetime import datetime
from datetime import date
from datetime import timedelta

i = datetime.now()
print (i.hour)

print (i.minute)

print ("Current date & time = %s"%i)

#get date for past 20 days
j = date.today()-timedelta(20)

print (j)
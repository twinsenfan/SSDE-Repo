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
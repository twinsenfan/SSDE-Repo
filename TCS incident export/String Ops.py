import datetime
import time

__author__ = 'Home'

tempString = ''
Field = 'CN=Twinsen Fan,OU=TestOU1,OU=Domain Controllers,DC=TfanTestDomain,DC=com'

tempString = Field

Field = tempString.replace(",", " ")

print(Field)




TimeUpperboundary = datetime.datetime.now()

print(TimeUpperboundary )

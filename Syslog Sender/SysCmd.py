import sys
import getpass

total = len(sys.argv)
cmdargs = str(sys.argv)
print ("The total numbers of args passed to the script: %d " % total)
#print ("Args list: %s " % cmdargs)
# Pharsing args one by one

if total != 3:
    print ("Error, incorrect Syntax!")
    print ("Usage: Script.py <SQL Server IP> <Username>")
    sys.exit()
else:
    print("SQL Server: %s" % str(sys.argv[1]))
    print("Username: %s" % str(sys.argv[2]))
    p = getpass.getpass(prompt='Password for account %s: ' % str(sys.argv[2]))
    print('You entered:', p)

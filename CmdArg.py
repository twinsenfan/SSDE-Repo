import sys

total = len(sys.argv)
cmdargs = str(sys.argv)
print ("The total numbers of args passed to the script: %d " % total)
#print ("Args list: %s " % cmdargs)
# Pharsing args one by one

if total != 4:
    print ("Error, incorrect Syntax!")
    print ("Script.py <SQLServerIP> <Username> <Password>")
    sys.exit()
else:
    print ("SQL Server: %s" % str(sys.argv[1]))
    print ("Username: %s" % str(sys.argv[2]))
    print ("Password: %s" % str(sys.argv[3]))
    
    

__author__ = 'Home'

import argparse

parser = argparse.ArgumentParser(description='This is a demo script by nixCraft.')
parser.add_argument('-IP', '--SQL Server IP', help='SQL Server IP',required=True)
parser.add_argument('-Username', '--Username',help='Username for SQL account', required=True)
parser.add_argument('-Password', '--Password',help='Password for SQL account', required=True)

args = parser.parse_args()

## show values ##
print("Input file: %s" % args.IP )
print("Output file: %s" % args.Password)

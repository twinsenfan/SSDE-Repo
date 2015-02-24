__author__ = 'Home'


import xml.parsers.expat
import sys
from glob import glob


def parsefile(file):
    parser = xml.parsers.expat.ParserCreate()
    parser.ParseFile(open(file, "r"))

for arg in sys.argv[1:]:
    for filename in glob(arg):
        #try:
            parsefile(filename)
            print("%s is well-formed") % filename
        #except xml.parsers.expat.error:
         #   print("%s is NOT well-formed! %s") % filename

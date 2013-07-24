#!/usr/bin/env python
# This script pulls all target urls from HTTPS-Everywhere Rulesets. 
# It does not print any domain names containing *, any containing "www." 
# (which is taken care of by the mochitest), and all rulesets that 
# are already deactivated by designation as "default_off" or
# mixed content

import xml.parsers.expat
import glob
import os
import sys

if __name__ == '__main__':
    #checks for correct number of user arguments
    if len(sys.argv) != 2 :
        print "Usage: {0} [https-everywhere git repository directory]".format(sys.argv[0])
        sys.exit()

    dir = sys.argv[1]

    #checks for valid path name
    if not os.path.exists(os.path.dirname(dir)):
        print "Please submit valid path: {0} [https-everywhere git repository directory]".format(sys.argv[0])
        sys.exit()

    #change the path below as relevant
    # os.chdir("/Users/lisayao/https-everywhere/src/chrome/content/rules")

    #changes directory to user input
    os.chdir(dir)

    num = 0

    #prints the name of the file and the url for each target tag
    for files in glob.glob("*.xml"):
        fo = open(files, "r")
        text = fo.read()
        global array
        array = []

        #this is a strategy to check for already disabled rulesets. 
        #A little wonky and hackish, I know, but global variables weren't behaving
        global array2
        array2 = []

        def start_element(name, attrs):
            global num
            # exec 'checkable = 1' in globals()
            if name == "ruleset":
                for n in range(0, len(attrs)):
                    key = attrs.keys()[n]
                    value = attrs.values()[n]
                    if key == "default_off":
                        array2.append("{0},{1}".format(key,value))
                         # exec 'checkable = 0' in globals()
                        # print files, 'is default_off'
                    elif (key == "platform") and ('mixedcontent' in value):
                         array2.append("{0},{1}".format(key,value))
                         # exec 'checkable = 0' in globals()
                         # print files, 'is mixedcontent'
            
            if name == "target":
                # print 'Start element:', name, attrs
                for n in range(0, len(attrs)):
                    # putting this in a try block, because encoding errors throw exceptions
                    try:
                        domain = attrs.values()[n]
                        if '*' not in domain and 'www' not in domain:
                            array.append("{0},{1}".format(num, domain))
                            # print "{0},{1}".format(num, domain)
                            num += 1
                    except:
                        pass
                    # sometimes the stuff prints in unicode and we can escape it as below
                    # print attrs.keys()[n].encode("ascii"), attrs.values()[n].encode("ascii")
        
        p = xml.parsers.expat.ParserCreate()

        p.StartElementHandler = start_element

        p.Parse(text, 1)

        #if array containing already disabled rulesets is empty, then print the domains. Else don't do anything
        if array2 == []:
            for item in array:
                print item

        fo.close()

#!/usr/bin/python
#This script pulls all target urls from HHTPS-Everywhere Rulesets.

import xml.parsers.expat
import glob
import os
import sys

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

	def start_element(name, attrs):
		global num
		if name == "target":
			# print 'Start element:', name, attrs
			for n in range(0, len(attrs)):
				# putting this in a try block, because encoding errors throw exceptions
				try:
					domain = attrs.values()[n]
					if '*' not in domain:
						print "{0},{1}".format(num, domain)
						num += 1
				except:
					pass
				# sometimes the stuff prints in unicode and we can escape it as below
				# print attrs.keys()[n].encode("ascii"), attrs.values()[n].encode("ascii")
		
	p = xml.parsers.expat.ParserCreate()

	p.StartElementHandler = start_element

	p.Parse(text, 1)

	fo.close()

#This script pulls all target urls from HHTPS-Everywhere Rulesets.

import xml.parsers.expat
import glob
import os

#change the path below as relevant
os.chdir("/Users/lisayao/https-everywhere/src/chrome/content/rules")

#prints the name of the file and the url for each target tag
for files in glob.glob("*.xml"):
	fo = open(files, "r")
	text = fo.read()	

	def start_element(name, attrs):
		if name == "target":
			# print 'Start element:', name, attrs
			for n in range(0, len(attrs)):
				print fo.name, attrs.values()[n]
				# sometimes the stuff prints in unicode and we can escape it as below
				# print attrs.keys()[n].encode("ascii"), attrs.values()[n].encode("ascii")
		
	p = xml.parsers.expat.ParserCreate()

	p.StartElementHandler = start_element

	p.Parse(text, 1)

	fo.close()

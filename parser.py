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

class HTTPSERuleParser:
    def __init__(self, httpse_dir):
        #checks for valid path name
        rules_dir = httpse_dir+'/src/chrome/content/rules'
        if not os.path.exists(os.path.dirname(rules_dir)):
            print "Please submit valid path: {0} [https-everywhere git repository directory]".format(sys.argv[0])
            return

        #changes directory to user input
        os.chdir(rules_dir)

        self.num = 0
        self.domains = []

        #prints the name of the file and the url for each target tag
        for filename in glob.glob("*.xml"):
            text = open(filename, "r").read()

            self.disabled_by_default = False
            self.domains_for_this_rule = []

            p = xml.parsers.expat.ParserCreate()
            p.StartElementHandler = self.start_element
            p.Parse(text, 1)

            #if the rule isn't disabled, add domains to self.domains
            if not self.disabled_by_default and len(self.domains_for_this_rule) > 0:
                self.domains += self.domains_for_this_rule

        # dedupe and sort the domains
        deduped_domains = []
        for domain in self.domains:
            if domain not in deduped_domains:
                deduped_domains.append(domain)
        deduped_domains.sort()

        i = 0
        for domain in deduped_domains:
            # putting this in a try block, because encoding errors throw exceptions
            try:
                print "{0},{1}".format(i, domain)
                i += 1
            except:
                pass
    
    def start_element(self, name, attrs):
        # exec 'checkable = 1' in globals()
        if name == "ruleset":
            for n in range(0, len(attrs)):
                key = attrs.keys()[n]
                value = attrs.values()[n]
                if key == "default_off":
                    self.disabled_by_default = True
                elif (key == "platform") and ('mixedcontent' in value):
                    self.disabled_by_default = True
        
        if name == "target":
            # print 'Start element:', name, attrs
            for n in range(0, len(attrs)):
                domain = attrs.values()[n]
                if '*' not in domain and 'www' not in domain:
                    self.domains_for_this_rule.append(domain)
            
if __name__ == '__main__':
    #checks for correct number of user arguments
    if len(sys.argv) != 2 :
        print "Usage: {0} [https-everywhere git repository directory]".format(sys.argv[0])
        sys.exit()

    httpse_dir = sys.argv[1]
    HTTPSERuleParser(httpse_dir);


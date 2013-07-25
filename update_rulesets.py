#!/usr/bin/env python

import sys, os, glob, re
import xml.etree.ElementTree as ET

class HTTPSERuleUpdater:
    def __init__(self, httpse_dir, domains_filename):
        # checks for valid path name
        rules_dir = httpse_dir+'/src/chrome/content/rules'
        if not os.path.exists(os.path.dirname(rules_dir)):
            print "Please submit valid path: {0} [https-everywhere git repository directory] [mixed content domains file]".format(sys.argv[0])
            return
        
        # checks for domains filename
        if not os.path.exists(domains_filename):
            print "Please submit valid domains filename: {0} [https-everywhere git repository directory] [mixed content domains file]".format(sys.argv[0])
            return

        # load domains, skipping blank lines and removing the trailing \n
        domains = []
        for domain in open(domains_filename, 'r').readlines():
            if domain.strip() != '':
                domains.append(domain.strip())

        # map the domains to XML filenames
        rulesets = {}
        os.chdir(rules_dir)
        for filename in glob.glob("*.xml"):
            targets = []
            tree = ET.parse(filename)
            root = tree.getroot()
            for elem in root.iter():
                if elem.tag == 'target':
                    for domain in domains:
                        if domain in elem.attrib['host']:
                            rulesets[domain] = filename
        
        # update the ruleset xml files
        for domain in rulesets:
            filename = rulesets[domain]
            print 'Fixing rule {0}'.format(filename)

            new_xml = ''
            xml_lines = open(filename, 'r').readlines()
            for line in xml_lines:
                if "<ruleset" in line:
                    if "platform=" in line:
                        line = re.sub(r'<ruleset (.*) platform="(.*)"(.*)>', r'<ruleset \1 platform="\2 mixedcontent"\3>', line)
                    else:
                        line = re.sub(r'<ruleset (.*)>', r'<ruleset \1 platform="mixedcontent">', line)

                    if 'mixedcontent' not in line:
                        print 'Something went wrong with rule {0}'.format(filename)
                new_xml += line

            # save the xml file again
            open(filename, 'w').write(new_xml)

if __name__ == '__main__':
    # checks for correct number of user arguments
    if len(sys.argv) != 3 :
        print "Usage: {0} [https-everywhere git repository directory] [mixed content domains file]".format(sys.argv[0])
        sys.exit()

    httpse_dir = sys.argv[1]
    domains_filename = sys.argv[2]

    HTTPSERuleUpdater(httpse_dir, domains_filename)

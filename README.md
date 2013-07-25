HTTPS-E Mixed Content Code
==========================

parser.py looks through all of the HTTPS Everywhere rules and makes a list of domain names to use in the Firefox MCB mochitest. Usage:

    ./parser.py [path to https-everywhere git repo] > domains.csv

update_rulesets.py takes a list of domain names that trigger the MCB and it updates all the associated HTTPS-E rules XML files to include platform="mixedcontent". Usage:

    ./update_rulesets.py [https-everywhere git repository directory] [mixed content domains file]

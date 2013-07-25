HTTPS-E Mixed Content Code
==========================

parser.py looks through all of the HTTPS Everywhere rules and makes a list of domain names to use in the Firefox MCB mochitest. Usage:

    ./parser.py [path to https-everywhere git repo] > domains.csv

update_rulesets.py takes a list of domain names that trigger the MCB and it updates all the associated HTTPS-E rules XML files to include platform="mixedcontent". Usage:

    ./update_rulesets.py [https-everywhere git repository directory] [mixed content domains file]

Firefox mochitest output
------------------------

Output from the Firefox MCB mochitest from 0-I is in data/mochitest_mcb_output1.txt. This command strips it down to just the domains:

    cat mochitest_mcb_output1.txt | grep "Mixed Content Doorhanger appeared" | cut -d"|" -f3 | cut -d"/" -f3 | sed s/^www.//g | sort -u

That's saved in data/mcb_domains.txt.

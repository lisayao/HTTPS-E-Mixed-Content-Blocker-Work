#!/bin/bash
echo Mochiscript is starting...
rm /Users/lisayao/Desktop/mochilog.txt
HTTPSE_PATH="/Users/lisayao/https-everywhere/"
CSV_PATH="/Users/lisayao/Desktop/Github/HTTPS-E-Mixed-Content-Work/urls"
cd $CSV_PATH
rm *
cd /Users/lisayao/Desktop/Github/HTTPS-E-Mixed-Content-Work
python parser2.py $HTTPSE_PATH 500 $CSV_PATH


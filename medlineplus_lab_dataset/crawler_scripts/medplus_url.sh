#!/usr/bin/env bash

: 'Requirements:
wget
grep
coreutils
'

#URL address
url="https://medlineplus.gov/lab-tests/"

#Get the url
wget $url -q -O /tmp/index-labs.html

#Select lab-test contained lines
grep 'https:\/\/medlineplus.gov\/lab-tests\/' /tmp/index-labs.html > /tmp/index-labs.txt

#Extract labs
grep -o -P '(?<=href=\").*(?=\")' /tmp/index-labs.txt > /tmp/labs-redundant.txt

#Remove redundant lines
tail -n +5 /tmp/labs-redundant.txt > /tmp/labs.txt 

#Select only unique URLs
sort /tmp/labs.txt | uniq > ../urls/medlineplus_lab_urls.txt

#Show medicines urls
cat ../urls/medlineplus_lab_urls.txt

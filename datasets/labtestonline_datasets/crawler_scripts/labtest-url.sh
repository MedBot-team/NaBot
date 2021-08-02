#!/usr/bin/env bash

: 'Requirements:
wget
grep
sed
coreutils
'

#URL address
url="https://labtestsonline.org/tests-index"
#Get the url
wget $url -q -O /tmp/index.html
#Select tests contained lines
grep "href=\"\/tests\/" /tmp/index.html > /tmp/lab-tests-redundant.txt
#Extract tests paths
grep -o -P '(?<=href=").*?(?=")' /tmp/lab-tests-redundant.txt > /tmp/lab-tests.txt
#Select only unique URLs
sort -n /tmp/lab-tests.txt | uniq > ../urls/lab-tests-urls.txt 
#Concatinate url domain to test paths 
sed 's/^/https:\/\/labtestsonline.org/' -i ../urls/lab-tests-urls.txt 

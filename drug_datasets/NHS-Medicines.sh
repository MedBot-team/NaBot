#!/usr/bin/env bash

: 'Requirements:
wget
grep
sed
coreutils
'

#URL address
url="https://www.nhs.uk/medicines/"

#Get the url
wget $url -q -O /tmp/index-nhs.html

#Select medicines contained lines
grep "href=\"\/medicines" /tmp/index-nhs.html > /tmp/medicines-lines-redundant.txt

#Remove redundant lines
grep -v "#" /tmp/medicines-lines-redundant.txt > /tmp/medicines-lines.txt 

#Extract medicines paths
grep -o -P '(?<=href=").*(?=">)' /tmp/medicines-lines.txt > /tmp/medicines-paths.txt

#Concatinate url domain to medicine paths 
sed -e 's/^/https:\/\/www.nhs.uk/' /tmp/medicines-paths.txt > nhs-medicines-urls.txt

#Show medicines urls
cat nhs-medicines-urls.txt

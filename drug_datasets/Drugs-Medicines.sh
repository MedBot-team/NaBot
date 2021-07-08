#!/usr/bin/env bash

: 'Requirements:
wget
grep
sed
coreutils
'

#URL address
url="https://www.drugs.com/alpha/"

#For loop in all alphabets and "0-9"
for i in {a..z} 0-9; do
	#Get the url
	wget $url$i.html -q -O /tmp/index-drugs-$i.html
	
	#Select medicines contained lines
	grep -o -P "(?<=a href=').*(?=</a></li>)" /tmp/index-drugs-$i.html > /tmp/medicines-lines-redundant-$i.txt

	#Remove redundant lines
	tail -n +10 /tmp/medicines-lines-redundant-$i.txt | head -n -4 > /tmp/medicines-lines-$i.txt 

	#Extract medicines paths
	grep -o -P "(?<=\/).*(?='>)" /tmp/medicines-lines-$i.txt > /tmp/medicines-paths-$i.txt

	#Concatinate url domain to medicine paths 
	sed -e 's/^/https:\/\/www.drugs.com\//' /tmp/medicines-paths-$i.txt >> /tmp/drugs-medicines-urls.txt
done

#Select only unique URLs
sort /tmp/drugs-medicines-urls.txt | uniq -u > drugs-medicines-urls.txt 

#Show medicines urls
cat drugs-medicines-urls.txt


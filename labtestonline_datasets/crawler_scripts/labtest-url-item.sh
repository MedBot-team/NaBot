#!/usr/bin/env bash

: 'Requirements:
wget
grep
sed
coreutils
'

# Make url_items directory to store url-item pairs
mkdir -p ../urls/url_items

# Read lab-tests-urls.txt line by line
while IFS= read -r url; do
    # Print URL 
    echo $url
    # Get the URL
    wget $url -q -O /tmp/index.html
    # Select field-item and h3 tag texts. (Consist of "items title" and "also known as" parts in the URL)
    grep -o -P -- '(?<=div class=\"field-item\">)(.*?)(?=<\/div)|(?<=h3>).*(?=<\/h3)' /tmp/index.html > /tmp/item.txt
    # Store items in the file with lab-test name
    grep -v "^<" /tmp/item.txt > ../urls/url_items/${url#https:\/\/labtestsonline.org\/tests\/*}.txt 
done < ../urls/lab-tests-urls.txt

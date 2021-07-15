import scrapy
import re
from bs4 import BeautifulSoup

class FirstSpider(scrapy.Spider):
    name = 'first5'


    # start_urls = ['https://medlineplus.gov/druginfo/meds/a681004.html']
    # start_urls = ['https://medlineplus.gov/druginfo/drug_Aa.html']
    start_urls = ['https://medlineplus.gov/druginformation.html']

    def parse(self, response):
        # pass
        print('=' * 100)
        # print(response.xpath('//h1/text()').get())
        # print(response.xpath('//h2/text()').get())


        next_pagee = response.xpath('//nav/div/div/ul/li/a/@href').getall()
        # print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        print(next_pagee)
        for j in next_pagee:
            if j is not None:
                # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&')
                # print(response.follow(j))
                self.Link = response.follow(j)

                self.Link = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', str(self.Link))[0]
                Link_1 = self.Link
                print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
                # yield response.follow(j, callback=self.postpagepars)
                yield scrapy.Request(url=Link_1, callback=self.postpagepars1)
                # yield scrapy.Request(url=response.follow(i) , callback=self.postpagepars)


    def postpagepars1(self, response):

        print("LLEEEEEEEEN: ", len(response.xpath('//article/ul/li/a/@href').getall()))

        next_page = response.xpath('//article/ul/li/a/@href').getall()
        for i in next_page:
            if i is not None:
                print(response.follow(i))
                self.Link = response.follow(i)
                self.Link = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', str(self.Link))[0]
                Link_2 = self.Link
                # yield response.follow(i, callback=self.postpagepars)
                yield scrapy.Request(Link_2, callback=self.postpagepars)

    def postpagepars(self, response):

        print("INJJJJJJJJJJJJJJJJJJJA:   ", response.url)

        for i  in (response.xpath('//section').getall()):

            h2 =""
            p  =""
            h3 =""
            li =""
            total = ""


            soup = BeautifulSoup(i, "html.parser")
            for tag in soup.find_all() :

                if tag.name == 'h2':
                    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                    # print(tag.text)
                    h2 = tag.text

                if tag.name == 'p':
                    # print(tag.text)
                    p = tag.text
                    total = total + p

                if tag.name == 'h3':
                    # print(tag.text)
                    h3 = tag.text
                    total = total + h3

                if tag.name == 'li':
                    # print(tag.text)
                    li = tag.text
                    total = total + li

            yield {
                'Link' : response.url,  #re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', str(self.Link))[0] ,
                'title': h2 ,
                'text' : total ,
            }


        print('=' * 100)

#####
#scrapy genspider first http://quotes.toscrape.com/
#scrapy crawl first
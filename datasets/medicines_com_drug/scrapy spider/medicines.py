import scrapy
import time
import re

class MedicinesSpider(scrapy.Spider):
    name = 'medicines'
    allowed_domains = ['medicines.org.uk']
    start_urls = ['https://www.medicines.org.uk/emc/browse-ingredients/']
    def parse(self, response):
        self.main_url = 'https://www.medicines.org.uk'
        print('='*50)
        # print(response.xpath('//ul/li/a/@href').getall())
        for url in response.xpath('//ul[@class="browse"]/li/a/@href').getall():
            yield scrapy.Request(url=self.main_url+url, dont_filter=True, callback=self.ingredientspagepars)
            # break

    def ingredientspagepars(self, response):
        for url in response.xpath('//a[@class="key"]/@href').getall():
            yield scrapy.Request(url=self.main_url+url, dont_filter=True, callback=self.listpagepars)
            # time.sleep(0.5)
            # break

    def listpagepars(self, response):
        # time.sleep(0.5)
        for box in response.xpath('//div[@id="browse-results"]/div').getall():
            drug_name = scrapy.selector.Selector(text=box).xpath('//h2/a/text()').get()
            drug_url = self.main_url+scrapy.selector.Selector(text=box).xpath('//h2/a/@href').get()

            ingredients = scrapy.selector.Selector(text=box).xpath('//h3/text()').get()
            company_name = scrapy.selector.Selector(text=box).xpath('//h4/a/text()').get()
            company_url = self.main_url+scrapy.selector.Selector(text=box).xpath('//h4/a/@href').get()

            pages = {}
            for row in scrapy.selector.Selector(text=box).xpath('//ul/li').getall():
                pages[scrapy.selector.Selector(text=row).xpath('//a/text()').get()] = \
                    self.main_url+scrapy.selector.Selector(text=row).xpath('//a/@href').get()

            # print("drug_name: {} | url: {} | ingredients: {} | company_name: {} | company_url: {} | pages: {}".format(drug_name, drug_url, ingredients, \
            #                                                                                         company_name, company_url, pages))

            yield scrapy.Request(url=drug_url, dont_filter=True, callback=self.drugpagepars, cb_kwargs={'url': drug_url, 'drug_name': drug_name,
                                                                                            'ingredients': ingredients, 'company_name':company_name,
                                                                                            'company_url': company_url, 'drug_pages': pages})

    def drugpagepars(self, response, url, drug_name, ingredients, company_name, company_url, drug_pages):
        if response.xpath('//ul[@id="tab-prod"]//a/text()').get() == 'SmPC':
            smpc = response.xpath('//div[@class="smpc"]/child::node()')
            flag = False
            row_body = {}
            head_one = ''
            value = ''

            for line in smpc:
                if line.xpath('@class').get() == 'sectionHeaderTop' and flag:
                    row_body[head_one] = value
                    head_one = ''
                    value = ''
                    flag = False

                if line.xpath('@class').get() == 'sectionHeaderTop' and not flag:
                    flag = True
                    head_one = line.xpath('text()').get()
                elif flag:
                    value += self.clean('\n'.join(line.xpath('descendant::text()').getall())) + '\n'
            row_body[head_one] = value
            row_keys = list(row_body.keys())

            flag = False
            body = {}
            head_one = ''
            value = ''
            for line in smpc:
                if line.xpath('@class').get() == 'sectionHeaderTop' or line.xpath('@class').get() == 'sectionHeader2ndLevel'\
                        and flag:
                    body[head_one] = value
                    head_one = ''
                    value = ''
                    flag = False

                if line.xpath('@class').get() == 'sectionHeaderTop' or line.xpath('@class').get() == 'sectionHeader2ndLevel'\
                        and not flag:
                    flag = True
                    head_one = line.xpath('text()').get()
                elif flag:
                    value += self.clean('\n'.join(line.xpath('descendant::text()').getall())) + '\n'
            body[head_one] = value
            body_keys = list(body.keys())
            # for key, value in zip(body.keys(), body.values()):
            #     if "\t\t\n\t\t\t\t\t\n" in value:
            #         print("key: ", key, " | url: ", url)

            legal_lategory = response.xpath('//div[@class ="row detail"]/div[3]/p/text()').get()
            last_updated_on_emc = response.xpath('//div[@id="sidebar"]//h3[1]/span/text()').get()

            yield {
                "url": url,
                "drug_name": drug_name,
                "ingredients": ingredients,
                "company_name": company_name,
                "company_url": company_url,
                "drug_pages": drug_pages,
                "row_body": row_body,
                "row_keys": row_keys,
                "body": body,
                "body_keys": body_keys,
                "Legal_Category": legal_lategory,
                "last_updated_on_emc": last_updated_on_emc
            }

    def clean(self, text):
        text = re.sub('[\n]+', '\n', text)
        text = text.strip()
        return text
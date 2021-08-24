import scrapy
import time
import re


class CancerresearchukSpider(scrapy.Spider):
    name = 'cancerresearchuk'
    allowed_domains = ['www.cancerresearchuk.org']
    start_urls = ['https://www.cancerresearchuk.org/about-cancer/cancer-in-general/treatment/cancer-drugs/drugs/']

    def parse(self, response):
        c = 0
        for url in (response.xpath('//*[@id="sortable-list"]/div//a/@href')).getall():
            c += 1
            print('=' * 50, str(c))
            yield scrapy.Request(url=url, dont_filter=True, callback=self.drugpagepars, cb_kwargs={'url': url})
            # time.sleep(1)
            # break

    def drugpagepars(self, response, url):
        # time.sleep(0.5)
        drug_name = response.xpath('//article//h1/text()').get()
        article = response.xpath('//article/child::node()')
        flag = False
        body = {}
        key = ''
        value = ''

        for line in article:
            if self.clean(line.get()):
                if line.xpath('name()').get() == 'h2' and flag:
                    # print(key , ' |', self.clean(value))
                    body[key] = self.clean(value)
                    key = ''
                    value = ''
                    flag = False

                if line.xpath('name()').get() == 'h2' and not flag:
                    flag = True
                    key = self.clean(line.xpath('text()').get())
                elif line.xpath('name()').get() == 'header' and not flag:
                    flag = True
                    key = 'explain drug name'
                elif flag:
                    if str(line.xpath('@class').get()) != "more-information":
                        value = value + self.clean('\n'.join(line.xpath('descendant::text()').getall())) + '\n'
        yield {
            'url': url,
            'drug_name': drug_name,
            'body': body
        }

    def clean(self, text):
        text = re.sub('[\n]+', '\n', text)
        text = text.strip()
        return text

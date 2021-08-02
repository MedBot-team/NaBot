import re
import json
import requests
from tqdm import tqdm


class url_item_parser():
    def __init__(self, url_input):
        super().__init__()

        with open(url_input, 'r') as file:
            self.urls = [line.strip() for line in file]

        self.drugs_url = dict()

    def parser(self):
        for url in tqdm(self.urls):
            lab_test = url.split('.')[-1].split('/')[-1]
            r = requests.get(url)

            items_redundant = re.findall(
                '(?<=div class=\"field-item\">)(.*?)(?=<\/div)|(?<=h3>).*(?=<\/h3)', r.text)

            items = [item for item in items_redundant if re.findall(
                '^(?!<div).*$', item) and item != '' and 'href' not in item]
            self.drugs_url.update({lab_test: items})

    def save_dict(self, outname):
        with open(outname, 'w') as outfile:
            json.dump(self.drugs_url, outfile)


def main():
    url_item_lt = url_item_parser('../urls/lab-tests-urls.txt')
    url_item_lt.parser()
    url_item_lt.save_dict('../urls/labtest_url_items.json')


if __name__ == '__main__':
    main()

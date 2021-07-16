import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup


class labtestonline_parser():
    def __init__(self, urls_list, items_static):
        super().__init__()
        self.item_df = pd.read_csv(items_static)

        with open(urls_list, 'r') as file:
            self.urls = [line.strip() for line in file]

    def __item_list(self, num):
        items = ['Also Known As']
        items += list(self.item_df[:num]['item'])
        return items

    def __labtest_name(self, url):
        labtest = url.split('.')[-1].split('/')[-1]
        return labtest

    def __aka_check(self, soup):
        aka_list = ''
        if soup.find_all('div', string="Also Known As"):
            aka_list = [tag.get_text() for tag in soup.find_all(
                'div', string="Also Known As")[0].next_sibling.next_sibling if tag != '\n']
        return aka_list

    def __get_text(self, soup, items, lab_test, df):
        for item in items[1:]:
            if soup.find_all('div', text=item):
                tag = soup.find_all('div', text=item)[0].next.next

                while tag == '\n':
                    tag = tag.next

                df[item][lab_test] = tag.text
        return df

    def parser(self, num):
        items = self.__item_list(num)
        lab_tests = [self.__labtest_name(url) for url in self.urls]
        labtest_df = pd.DataFrame('', columns=items, index=lab_tests)

        for url in tqdm(self.urls):
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            lab_test = url.split('.')[-1].split('/')[-1]
            labtest_df['Also Known As'][lab_test] = self.__aka_check(soup)
            labtest_df = self.__get_text(soup, items, lab_test, labtest_df)
        return labtest_df

    def df_write(self, labtest_df, out_name):
        labtest_df.reset_index(inplace=True)
        labtest_df.rename({'index': 'Lab test'}, axis=1, inplace=True)
        labtest_df.to_csv(out_name, index=False)


def main():
    lt_parser = labtestonline_parser('../urls/lab-tests-urls.txt',
                                     '../dataset_statics/url_item_static.csv')
    labtest_df = lt_parser.parser(10)
    lt_parser.df_write(labtest_df, '../dataset_files/labtest_dataset.csv')
    print(labtest_df)


if __name__ == '__main__':
    main()

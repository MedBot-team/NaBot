"""
Drugs.com parser
To obtain extra information from the input drugs list
"""

# Import necessary modules
import json
import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup


# Drugs.com parser class
class drugs_dot_com():
    # Class initialization
    def __init__(self):
        # Document parts
        self.columns = ['before-taking',
                        'directions',
                        'fda-approval',
                        'patient-counseling',
                        'pregnancy',
                        'storage']

    # Initialization of drugs dataframe
    def __drugs_df_init(self, urls):
        # List of medicines
        medicines = [self.__get_med_name(url) for url in urls]
        # Constructing dataFrame with empty values
        df = pd.DataFrame("",
                          index=medicines,
                          columns=self.columns)
        return df

    # Get medicine name from its URL
    def __get_med_name(self, url):
        medicine = url.split('.')[-2].split('/')[-1]
        return medicine

    # Get all tags with desired id in the URL
    def __get_id_items(self, url, item):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        tag = soup.find_all(attrs={'id': item})[0]
        return tag

    # Update drug dataframe with tag values
    def __drugs_df_update(self, df, medicine, item, tag):
        while tag.next_sibling.name not in ['div', 'h2']:
            tag = tag.next_sibling
            try:
                df.loc[medicine][item] += tag.text + '\n'
            except AttributeError:
                continue

    # Write drugs dataframe to a comma-separated values file
    def __drugs_df_write(self, df, name):
        df.reset_index(inplace=True)
        df.columns = ['medicine'] + self.columns
        df.sort_values(by=['medicine'], inplace=True)
        df.to_csv(name, index=False)

    # Generate list of items per medicine URL
    def __url_item_list_reader(self, url_item_file):
        return json.load(open(url_item_file))

    # Parsing drugs.com site
    def drugs_parser(self, url_file, url_item_file, dataset_name):
        dic = self.__url_item_list_reader(url_item_file)

        with open(url_file, 'r') as file:
            urls = [line.strip() for line in file]

        df = self.__drugs_df_init(urls)

        for item in self.columns:
            for url in tqdm(dic[item]):
                medicine = self.__get_med_name(url)
                tag = self.__get_id_items(url, item)
                self.__drugs_df_update(df, medicine, item, tag)

        self.__drugs_df_write(df, dataset_name)
        return df

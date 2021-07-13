"""
Drugs.com parser
To obtain information from the input drugs list
"""

# Import necessary modules
import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup


# Drugs.com parser class
class drugs_dot_com():
    # Class initialization
    def __init__(self):
        super().__init__()
        # Document parts
        self.columns = ['medicine',
                        'vitamin',
                        'before-taking',
                        'cautions',
                        'contraindications',
                        'directions',
                        'dosage',
                        'faq',
                        'fda-approval',
                        'interactions',
                        'patient-advice',
                        'patient-counseling',
                        'patient-education',
                        'pharmacokinetics',
                        'pharmacology',
                        'pregnancy',
                        'preparations',
                        'side-effects',
                        'storage',
                        'uses',
                        'warnings',
                        'what-to-avoid']

    # Check if the medicine is a vitamin or not
    def __vitamin_check(self, url):
        if 'mtm' in url.split('/'):
            return True
        return False

    # Initialization of drugs dataframe
    def __drugs_df_init(self, urls):
        # List of medicines
        medicines = [self.__get_med_name(url) for url in urls]
        # Constructing dataFrame with empty values
        df = pd.DataFrame("",
                          index=range(len(medicines)),
                          columns=self.columns)
        return df

    # Get medicine name from its URL
    def __get_med_name(self, url):
        medicine = url.split('.')[-2].split('/')[-1]
        return medicine

    # Get all tags with ddc-anchor-offset class in the URL
    def __get_ddc_items(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        items = soup.find_all(attrs={'class': 'ddc-anchor-offset'})[:6]
        return items

    # Check if tag is NavigableString or not
    def __navigablestring_check(self, tag):
        text = ''
        while not hasattr(tag.next, 'get'):
            # text += tag.next
            tag = tag.next
        return tag, text

    # Update drug dataframe with tag values
    def __drugs_df_update(self, df, index, items):
        for item in items:
            tag, _ = self.__navigablestring_check(item)
            # Get a text till reaching the next part
            while tag.next.get('id') not in self.columns + ['moreResources'] and tag.next.text != 'Further information':
                # Get all texts after the desired tag
                df.loc[index][item.get('id')] = df.loc[index][item.get(
                    'id')] + tag.next.text + '\n'
                # Update tag and check if it is NavigableString or not
                tag, text = self.__navigablestring_check(tag.next)
                df.loc[index][item.get('id')] = df.loc[index][item.get(
                    'id')] + text
        return df

    # Write drugs dataframe to a comma-separated values file
    def __drugs_df_write(self, df, name):
        df.sort_values(by=['medicine'], inplace=True)
        df.to_csv(name, index=False)

    # Parsing drugs.com site
    def drugs_parser(self, url_file_name, dataset_name):
        with open(url_file_name, 'r') as file:
            urls = [line.strip() for line in file]

        df = self.__drugs_df_init(urls)

        for med_i, url in enumerate(tqdm(urls)):
            df.loc[med_i]['medicine'] = self.__get_med_name(url)
            df.loc[med_i]['vitamin'] = self.__vitamin_check(url)
            items = self.__get_ddc_items(url)
            df = self.__drugs_df_update(df, med_i, items)
        
        print(df)
        self.__drugs_df_write(df, dataset_name)
        return df

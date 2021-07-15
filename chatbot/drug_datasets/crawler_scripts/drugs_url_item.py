import json
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

# Item extractor class
class item_extractor():
    # Class initialization
    def __init__(self, url_list):
        super().__init__()
        # Reading input file
        with open(url_list, 'r') as file:
            self.urls = [line.strip() for line in file]
        # Create an empty dictionary for storing URLs items list
        self.drugs_url = dict()

    # Extract items per list 
    def extract_item(self):
        for url in tqdm(self.urls):
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            # Get all tags with ddc-anchor-offset class in the URL
            items = soup.find_all(attrs={'class': 'ddc-anchor-offset'})
            # Update dictionary with list of items per URL
            for item in items:
                if item.get('id') in self.drugs_url.keys():
                    self.drugs_url[item.get('id')].append(url)
                else:
                    self.drugs_url[item.get('id')] = [url]
        return self.drugs_url

    # Save dictionary
    def save_dict(self, output_name):
        json.dump(self.drugs_url, open(output_name, "w"))


# Main function
def main():
    extractor = item_extractor('input-normal.txt')
    item_dic = extractor.extract_item()
    extractor.save_dict('drugs_url_items.json')
    print(item_dic.keys())


if __name__ == '__main__':
    main()

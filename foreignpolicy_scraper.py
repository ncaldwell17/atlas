from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
from datetime import datetime
import re

from quickstart import retrieve_values_as_dataframe
import spacy
nlp = spacy.load('en_core_web_sm')

# id and range for the geographic dataset
GEOTAG_ID = '19X7PwbLrKLGJySaFSHr5Pze-VRM-6l_9EOqXDu43T3k'
GEOTAG_RANGE = 'Sheet1!A1:E171'


class ForeignPolicyScraper(object):

    def __init__(self, link):
        self.html = soup(urlopen(link), 'html.parser')

        self.link = link
        self.title = self.html.find('h1', class_='hed').text
        self.subtitle = self.html.find('h2', class_='dek-heading').text
        self.date = self.get_date()
        self.author = re.sub('[\  \n]{2,}', '', self.html.find('span', class_='pre').parent.findNext('a').text)

        self.label = self.get_label()[0]

        try:
            self.country = self.get_label()[1]
        except IndexError:
            self.country = "unchecked"

    def get_date(self):
        date = self.html.find_all('time')[0].text

        def clean_date(_date):
            regex = re.sub(r'\n', '', _date)
            regex = re.sub(r',', '', regex)
            regex = re.sub(r'\s*..:..\s..', '', regex)
            return regex

        date = clean_date(date)
        date = datetime.strftime(datetime.strptime(date, '%B %d %Y'), '%m/%d/%Y')
        return date

    def get_label(self):

        geotag_df = retrieve_values_as_dataframe(GEOTAG_ID, GEOTAG_RANGE)

        def get_gpes(_string):
            # SpaCy's NER improves with less noise = strip out non-alphanumerics
            named_entities = nlp(re.sub(r'[^A-Za-z0-9]+', ' ', _string).lower())

            gpes = list()
            for entity in named_entities.ents:
                if entity.label_ == 'GPE' or entity.label_ == 'NORP':
                    gpes.append(entity.text)

            return gpes

        gpes = get_gpes(self.title)

        def verify_against(_gpe, _df):
            for col in list(_df.columns):
                if len(_df.loc[_df[col] == _gpe.capitalize()]) > 0:
                    return True
                else:
                    pass
            return False

        if len(gpes) is 0:
            return ['none']

        elif len(gpes) is 1:
            if verify_against(gpes[0], geotag_df):
                return ['single', gpes[0].capitalize()]
            else:
                return ['invalid']

        else:
            valid_gpes = []
            for gpe in gpes:
                if verify_against(gpe, geotag_df):
                    valid_gpes.append(gpe)
                else:
                    pass

            if len(valid_gpes) is 0:
                return ['invalid']
            elif len(valid_gpes) is 1:
                return ['single', valid_gpes[0].capitalize()]
            elif len(valid_gpes) > 1:
                return ['multiple']

    def __repr__(self):
        return f"Date {self.date}\n Title: {self.title} \n"

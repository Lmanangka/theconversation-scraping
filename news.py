from bs4 import BeautifulSoup
from tabulate import tabulate
import pyshorteners
import textwrap
import requests
import argparse

class Spider:
    def __init__(self, url):
        self.url = url
        self.header = {'user-agent': 'BOT'}

    def usr_input(self):
        parser = argparse.ArgumentParser(prog='news',
                        description='Web scraping articles title and podcasts\
                                title from The Conversation',
                                         epilog='Example: news.py -a')
        group_parser = parser.add_mutually_exclusive_group()
        group_parser.add_argument('-a', '--articles', action='store_true',
                                  help='Show articles title and link')
        group_parser.add_argument('-p', '--podcasts', action='store_true',
                                  help='Show podcasts title and link')
        return parser.parse_args()

    def get_data(self, articles=False, podcasts=False):
        short_url = pyshorteners.Shortener()
        if articles == True and podcasts == False:
            page = requests.get(self.url['articles'], headers=self.header).text
            soup = BeautifulSoup(page, 'html.parser')

            data = {'title':[], 'link':[]}
            articles = soup.find_all('div', class_='article--header', limit=10)
            for contents in articles:
                data['title'].append(textwrap.shorten(contents.h2.text.replace(u'\xa0', ' '), width=50, placeholder='...'))
                data['link'].append(short_url.tinyurl.short(f"https://theconversation.com{contents.h2.a['href']}"))
            return data

        elif articles == False and podcasts == True:
            page = requests.get(self.url['podcasts'], headers=self.header).text
            soup = BeautifulSoup(page, 'html.parser')

            data = {'title':[], 'link':[], 'date':[]}
            podcasts = soup.find_all('div', class_='grid-nine grid-last', limit=10)
            for contents in podcasts:
                data['title'].append(textwrap.shorten(contents.h3.text, width=50, placeholder='...'))
                data['link'].append(short_url.tinyurl.short(f"https://theconversation.com{contents.h3.a['href']}"))
                data['date'].append(contents.time.text)
            return data

    def display_data(self, data):
        return tabulate(data, headers='keys', tablefmt='double_grid')

if __name__ == "__main__":
    URLS = {'articles': 'https://theconversation.com/id',
           'podcasts': 'https://theconversation.com/id/podcasts/suarakademia'}
    spider = Spider(URLS)
    usr_input = spider.usr_input()
    data = spider.get_data(usr_input.articles, usr_input.podcasts)
    print(spider.display_data(data))

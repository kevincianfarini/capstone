import requests, warc, sys
from bs4 import BeautifulSoup


class WordPressBlog:
    def __init__(self, url):
        self.url = url
        self.page_number = 1

    def __iter__(self):
        return self

    def __next__(self):
        response = requests.get('%s/page/%d/' % (self.url, self.page_number))
        self.page_number += 1
        if response.status_code == 404:
            raise StopIteration
        return BeautifulSoup(response.content, 'html.parser')



def scrape_wordpress_article(url):
    pass

def scrape_wordpress_page(page):
    print('yay')

def scrape_wordpress_blog(url):
    for page in WordPressBlog(url):
        scrape_wordpress_page(page)

def scrape(url):
    if 'wordpress' in url:
        scrape_wordpress_blog(url)

if __name__ == '__main__':
    for line in sys.stdin:
        scrape(line)
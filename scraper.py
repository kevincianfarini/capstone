import requests, warc, sys
from bs4 import BeautifulSoup
from multiprocessing import Pool


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



def scrape_wordpress_article(title, content, footer):
    print(title)

def scrape_wordpress_page(page):
    def parse(text):
        parsed = {name: text.find(attrs={'class': 'entry-%s' % name}) for name in ['content', 'footer']}
        parsed['title'] = text.find_all('header', limit=2)[1].find('h1')
        return parsed

    for article in page.find_all('article'):
        link = article.find(attrs={'class': 'entry-title'}).find('a')
        if link:
            response = requests.get(link['href'])
            if response.status_code != 404:
                html = BeautifulSoup(response.content, 'html.parser')
                scrape_wordpress_article(**parse(html))
            else:
                print('404: %s' % link['href'])


def scrape_wordpress_blog(url):
    for page in WordPressBlog(url):
        scrape_wordpress_page(page)

def scrape(line):
    if 'wordpress' in line.strip():
        scrape_wordpress_blog(line.split('->')[0].strip())

if __name__ == '__main__':
    with open(sys.argv[1]) as input:
        if len(sys.argv) == 3 and sys.argv[2] == '--threaded':
            with Pool(5) as p:
                p.map(scrape, input.read().splitlines())
        else:
            for line in input:
                scrape(line)
            
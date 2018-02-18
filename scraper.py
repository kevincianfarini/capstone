import requests, warc, sys
from bs4 import BeautifulSoup
from multiprocessing import Pool


class BlogArchive:
    def __init__(self, name):
        if name is None:
            raise ValueError('Name Cannot be None')
        self.name = name
        self.articles = []

    def __str__(self):
        return '%s -> [%d]' % (self.name, len(self.articles))

    def __repr__(self):
        return str(self)


class ArticleArchive:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'meta':
                self.author = value.find(attrs={'class': 'byline'}).text.strip().split()[1]
                self.publication_date = value.find('time')['datetime']
            else:
                setattr(self, key, value.text)


    def __str__(self):
        return '%s -> (%s, %s)' % (self.title, self.author, self.publication_date)


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



def scrape_wordpress_article(blog, **kwargs):
    article = ArticleArchive(**kwargs)
    print(article)
    blog.articles.append(article)

def scrape_wordpress_page(blog, page):
    def parse(text):
        parsed = {name: text.find(attrs={'class': 'entry-%s' % name}) for name in ['content', 'meta']}
        parsed['title'] = text.find_all('header', limit=2)[1].find('h1')
        return parsed

    for article in page.find_all('article'):
        link = article.find(attrs={'class': 'entry-title'}).find('a')
        if link:
            response = requests.get(link['href'])
            if response.status_code != 404:
                html = BeautifulSoup(response.content, 'html.parser')
                scrape_wordpress_article(blog=blog, **parse(html))
            else:
                print('404: %s' % link['href'])

def scrape_wordpress_blog(url):
    content = requests.get(url).content
    blog_archive = BlogArchive(
        BeautifulSoup(content, 'html.parser').find('h1', attrs={'class': 'site-title'}).text
    )
    for page in WordPressBlog(url):
        scrape_wordpress_page(blog_archive, page)
    return blog_archive

def scrape(line):
    if 'wordpress' in line.strip():
        return scrape_wordpress_blog(line.split('->')[0].strip())

if __name__ == '__main__':
    with open(sys.argv[1]) as input:
        if len(sys.argv) == 3 and sys.argv[2] == '--threaded':
            with Pool(5) as p:
                print(p.map(scrape, input.read().splitlines()))
        else:
            for line in input:
                print(scrape(line))
            
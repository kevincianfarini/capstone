import requests, warc, sys
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool
from itertools import chain


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
            if key == 'author':
                try:
                    self.author = value.text.strip()
                except:
                    self.author = 'Unknown'
            else:
                setattr(self, key, value)

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


class BlogSpotBlog:
    def __init__(self, url):
        self.url = url

    def __iter__(self):
        return self

    def __next__(self):
        if self.url is None:
            raise StopIteration
        response = requests.get(self.url)
        page = BeautifulSoup(response.content, 'html.parser')
        older_posts = page.find('a', attrs={'id': 'Blog1_blog-pager-older-link'})
        if older_posts:
            self.url = older_posts['href']
        else:
            self.url = None
        return page


def wordpress(url, threaded):
    def scrape_wordpress_article(link):
        def parse(text):
            parsed = {name: text.find(attrs={'class': 'entry-%s' % name}) for name in ['content', 'meta']}
            parsed['title'] = text.find_all('header', limit=2)[1].find('h1')
            return parsed

        if link:
            response = requests.get(link['href'])
            if response.status_code != 404:
                html = BeautifulSoup(response.content, 'html.parser')
                parsed = parse(html)
                article = ArticleArchive(**{
                        'title': parsed['title'].text.strip(),
                        'publication_date': parsed['meta'].find('time')['datetime'],
                        'author': parsed['meta'].find('span', attrs={'class': 'author'}),
                        'content': parsed['content'].text
                    }
                )
                print(article)
                return article
            else:
                print('404: %s' % link['href'])

    def scrape_wordpress_page(page):
        return [
            scrape_wordpress_article(article.find(attrs={'class': 'entry-title'}).find('a')) for 
                article in page.find_all('article')
        ]

    def scrape_wordpress_blog(url, threaded):
        content = requests.get(url).content
        blog_archive = BlogArchive(
            BeautifulSoup(content, 'html.parser').find('h1', attrs={'class': 'site-title'}).text
        )

        if threaded:
            pages = list(WordPressBlog(url))
            with ThreadPool(len(pages)) as pool:
                articles = pool.map(scrape_wordpress_page, pages)
                blog_archive.articles.extend(list(chain(*articles)))
        else:
            for page in WordPressBlog(url):
                blog_archive.articles.extend(scrape_wordpress_page(page))

        return blog_archive

    return scrape_wordpress_blog(url, threaded)

def blogspot(url, threaded):
    def create_blog_archive(url):
        content = BeautifulSoup(requests.get(url).content, 'html.parser')
        title = content.find('h1', attrs={'class': 'title'})
        if title:
            return BlogArchive(title.text.strip())
        else:
            title = content.find('img', attrs={'id': 'Header1_headerimg'})['alt']
            return BlogArchive(title.strip())

    def scrape_blogspot_article(link):
        if link:
            page = BeautifulSoup(requests.get(link['href']).content, 'html.parser')
            article = ArticleArchive(**{
                'title': page.find('h3', attrs={'class': 'post-title'}).text.strip(),
                'publication_date': page.find('h2', attrs={'class': 'date-header'}).find('span').text.strip(),
                'author': page.find(attrs={'class': 'post-author'}).find('span'),
                'content': page.find(attrs={'class': 'entry-content'}),
            })
            print(article)
            return article
            
    def scrape_blogspot_page(page):
        return [
            scrape_blogspot_article(article.find('a')) for 
                article in page.find_all('h3', attrs={'class': 'post-title'})
        ]

    def scrape_blogspot_blog(url, threaded):
        blog_archive = create_blog_archive(url)

        if threaded:
            raise NotImplemented
        else:
            for page in BlogSpotBlog(url):
                blog_archive.articles.extend(scrape_blogspot_page(page))

    return scrape_blogspot_blog(url, threaded)

def scrape(line, threaded=False):
    if 'wordpress' in line.strip():
        return wordpress(line.split('->')[0].strip(), threaded)
    elif 'blogspot' in line.strip():
        return blogspot(line.split('->')[0].strip(), threaded)

if __name__ == '__main__':
    with open(sys.argv[1]) as input:
        for line in input:
                print(scrape(line, len(sys.argv) == 3 and sys.argv[2] == '--threaded'))
            
            
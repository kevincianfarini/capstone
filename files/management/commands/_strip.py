from bs4 import BeautifulSoup, Comment

def strip(blog):
    soup = BeautifulSoup(blog.body, 'html.parser')
    text = ' '.join([hit.strip() for hit in soup.findAll(string=True) if hit.parent.name != 'script' and not isinstance(hit, Comment)])
    for word in ['twitter', 'facebook', 'google']:
        text = text.replace(word, '')
    return text
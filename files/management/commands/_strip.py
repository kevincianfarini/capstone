from bs4 import BeautifulSoup, Comment
import re

def strip(blog):
    soup = BeautifulSoup(blog.body, 'html.parser')
    text = ' '.join([hit.strip() for hit in soup.findAll(string=True) if hit.parent.name != 'script' and not isinstance(hit, Comment)])
    for c in ['.', ',', '!', '?', ':', ';', '"', "'", '-', '~', '(', ')', '[', ']', '|', '/', '\\']:
        text = text.replace(c, ' ')
    text = re.sub(r"\s+advertisement\s+share", '', text)
    text = re.sub(r"\s+advertisements\s+share", '', text)
    text = text.replace('\n', '')
    return text
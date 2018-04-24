from django.core.management.base import BaseCommand, CommandError
from files.models import Blog, BlogPost
from bs4 import BeautifulSoup
from ._strip import strip
import os

class Command(BaseCommand):
    help = 'Export blogs as text files to ./export'

    def handle(self, *args, **kwargs):

        if not os.path.exists('./exported'):
            os.makedirs('./exported')

        with open('./exported/export.csv') as f:
            for blog in BlogPost.objects.all():
                f.write(
                    '%s, %s, %s, %s, %s\n' % (blog.title, blog.author, str(blog.pub_date), blog.source, strip(blog.body))
                )
            f.close()
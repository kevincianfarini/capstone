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

        for blog in BlogPost.objects.all():
            text_file = open('./exported/%d.txt' % blog.pk, 'w')
            text_file.write(strip(blog))
            text_file.close()
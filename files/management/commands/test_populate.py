from django.core.management.base import BaseCommand, CommandError
from files.models import Blog, BlogPost
from ._scraper import scrape


class Command(BaseCommand):
    help = 'scrape input file sites for blog posts'

    def add_arguments(self, parser):

        parser.add_argument(
            'sitefile',
            type=str
        )

        parser.add_argument(
            '--no-thread',
            action='store_true',
            dest='threaded',
            help='Run the population without multithreading'
        )

    def handle(self, *args, **kwargs):
        blogs = scrape(kwargs['sitefile'], not kwargs['threaded'])
        print(blogs)
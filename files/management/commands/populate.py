from django.core.management.base import BaseCommand, CommandError
from ._scraper import scrape

class Command(BaseCommand):
    help = 'scrape input file sites for blog posts'

    def add_arguments(self, parser):

        parser.add_argument(
            'sitefile',
            type=str
        )

        parser.add_argument(
            '--threaded',
            action='store_true',
            dest='threaded',
            help='Run the population in multithreaded mode'
        )

    def handle(self, *args, **kwargs):
        scrape(kwargs['sitefile'], kwargs['threaded'])
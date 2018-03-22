from django.core.management.base import BaseCommand, CommandError
from ._scraper import scrape
from files.models import Tag, Blog, BlogPost

class Command(BaseCommand):
    help = 'Reset the Database'

    def handle(self, *args, **kwargs):
        BlogPost.objects.all().delete()
        Blog.objects.all().delete()
        Tag.objects.all().delete()
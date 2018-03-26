from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'generate tags an existing database of blog posts'

    def handle(self, *args, **kwargs):
        raise NotImplementedError("Not Implemented")
        
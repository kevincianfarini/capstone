from django.core.management.base import BaseCommand, CommandError
from files.models import BlogPost, Tag
from ._strip import strip
import RAKE

class Command(BaseCommand):
    help = 'generate tags an existing database of blog posts'

    def handle(self, *args, **kwargs):
        r = RAKE.Rake(RAKE.SmartStopList())
        for blog in BlogPost.objects.all():
            cleaned = strip(blog)
            for t, w in filter(lambda tag: tag[1] >= 4.0, r.run(text=cleaned, maxWords=2)):
                tag, created = Tag.objects.get_or_create(name=t)
                blog.tags.add(tag)
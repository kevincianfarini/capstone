from django.core.management.base import BaseCommand, CommandError
from files.models import BlogPost, Tag
from ._strip import strip
import RAKE
from multiprocessing.pool import ThreadPool


class Command(BaseCommand):
    help = 'generate tags an existing database of blog posts'

    def handle(self, *args, **kwargs):
        def _tag(blog):
            r = RAKE.Rake(RAKE.SmartStopList())
            return (            
                blog,
                filter(lambda tag: tag[1] >= 4.0, r.run(text=strip(blog), maxWords=2))
            )
            
        with ThreadPool(8) as p:
            blog_tags = p.map(_tag, BlogPost.objects.all())
            print('db')
            for blog, tags in blog_tags:
                for tag, weight in tags:
                    t, created = Tag.objects.get_or_create(name=tag)
                    blog.tags.add(t)
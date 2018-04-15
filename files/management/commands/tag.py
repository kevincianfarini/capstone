from django.core.management.base import BaseCommand, CommandError
from files.models import BlogPost, Tag
from ._strip import strip
import RAKE
from multiprocessing.pool import ThreadPool
from django.db.models import Q

class Command(BaseCommand):
    help = 'generate tags an existing database of blog posts'

    def handle(self, *args, **kwargs):
        def _tag(blog):
            r = RAKE.Rake(RAKE.SmartStopList())
            return (            
                blog,
                [tag for tag, weight in filter(lambda tag: tag[1] >= 4.0, r.run(text=strip(blog), maxWords=2))]
            )
            
        with ThreadPool(8) as p:
            blog_tags = p.map(_tag, BlogPost.objects.all())
            print('db')

            t = map(lambda tag: Tag(name=tag), set(sum([tags for blog, tags in blog_tags], [])))
            Tag.objects.bulk_create(t)

            for blog, tags in filter(lambda blog_tag: len(blog_tag[1]) > 0, blog_tags):
                q = Q()
                for tag in tags:
                    q |= Q(name=tag)
                blog.tags.add(*Tag.objects.filter(q))
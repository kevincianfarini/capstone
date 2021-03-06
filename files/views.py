from django.shortcuts import render
from django.views.generic.base import TemplateView
from files.models import BlogPost, Tag
from django.views import generic
from rest_framework import generics
from files.serializers import BlogPostSerializer, TagSerializer
from django.db.models import Q, Count


class HomepageView(TemplateView):
    template_name = 'frontend/index.html'


class ContentView(TemplateView):
    template_name = 'files/content.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = BlogPost.objects.get(pk=kwargs['id'])
        return context


class ListBlogPostAPIView(generics.ListAPIView):
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        order = self.request.query_params.get('order')

        q = Q()
        for tag in self.request.query_params.get('tags').split('|'):
            q |= Q(name__icontains=tag)

        return BlogPost.objects.filter(
            tags__in=Tag.objects.filter(q)
        ).annotate(num_tags=Count('tags')).order_by(order)
            

class ListTagAPIView(generics.ListAPIView):
    serializer_class = TagSerializer
    
    def get_queryset(self):
        tag_text = self.request.query_params.get('tag')
        return Tag.objects.filter(
            name__icontains=tag_text
        ).annotate(num_posts=Count('blog_posts')).order_by('-num_posts')
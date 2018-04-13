from django.shortcuts import render
from django.views.generic.base import TemplateView
from files.models import BlogPost, Tag
from django.views import generic
from rest_framework import generics
from files.serializers import BlogPostSerializer, TagSerializer


class HomepageView(TemplateView):
    template_name = 'frontend/index.html'


class ContentView(TemplateView):
    template_name = 'files/content.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = BlogPost.objects.get(pk=kwargs['id'])
        return context

class BlogTableView(generic.ListView):
    template_name = 'frontend/index.html'
    context_object_name = 'all_posts'
    def get_queryset(self):
        return BlogPost.objects.all()


class ListBlogPostAPIView(generics.ListAPIView):
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        print(self.request.query_params.get('tags').split('|'))
        return BlogPost.objects.all()


class ListTagAPIView(generics.ListAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
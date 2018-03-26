from django.shortcuts import render
from django.views.generic.base import TemplateView
from files.models import BlogPost


class HomepageView(TemplateView):
    template_name = 'files/index.html'


class ContentView(TemplateView):
    template_name = 'files/content.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = BlogPost.objects.get(pk=kwargs['id'])
        return context
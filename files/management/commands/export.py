from django.core.management.base import BaseCommand, CommandError
from files.models import Blog, BlogPost
from bs4 import BeautifulSoup
from ._strip import strip_text
import os
import pandas
import sqlite3


class Command(BaseCommand):
    help = 'Export blogs as a csv file'

    def handle(self, *args, **kwargs):
        dat = sqlite3.connect('db.sqlite3')
        d = pandas.read_sql_query('select * from files_blogpost', dat)
        d['body'] = d.body.map(strip_text)
        d.to_csv('export.csv', sep='\t')
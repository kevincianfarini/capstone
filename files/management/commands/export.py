from django.core.management.base import BaseCommand, CommandError
from files.models import Blog, BlogPost
from bs4 import BeautifulSoup
from ._strip import strip
import os
import pandas
import sqlite3


class Command(BaseCommand):
    help = 'Export blogs as text files to ./export'

    def handle(self, *args, **kwargs):
        dat = sqlite3.connect('db.sqlite3')
        d = pandas.read_sql_query('select * from files_blogpost', dat)
        d.to_csv('export.csv')
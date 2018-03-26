from django.db import models

# Create your models here.

class Blog(models.Model):
    name = models.CharField(null=False, unique=True, max_length=500)


class Tag(models.Model):
    name = models.CharField(null=False, unique=True, max_length=30)


class BlogPost(models.Model):
    title = models.CharField(null=False, max_length=500)
    author = models.CharField(null=False, max_length=100)
    pub_date = models.CharField(null=False, max_length=100)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    body = models.TextField()
    tags = models.ManyToManyField(Tag)
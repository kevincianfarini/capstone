from django.db import models

# Create your models here.

class Blog(models.Model):
    name = models.CharField(null=False, unique=True, max_length=500)
    author = models.CharField(null=False, unique=False, max_length=100)


class Tag(models.Model):
    name = models.CharField(null=False, unique=True, max_length=30)


class BlogPost(models.Model):
    name = models.CharField(null=False, max_length=500)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents')
    tags = models.ManyToManyField(Tag)
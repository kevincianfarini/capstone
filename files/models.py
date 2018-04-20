from django.db import models
# Create your models here.

class Blog(models.Model):
    name = models.CharField(null=False, unique=True, max_length=500)


class Tag(models.Model):
    name = models.CharField(null=False, unique=True, max_length=30)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(null=False, max_length=500)
    author = models.CharField(null=False, max_length=100)
    pub_date = models.DateField()
    source = models.CharField(null=False, unique=True, max_length=512)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    body = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='blog_posts')

    def get_absolute_url(self):
        return 'files/content/%d/' % self.pk

    def __str__(self):
        return "%s -> (%s, %s): %s" % (
            self.title,
            self.author,
            self.pub_date,
            str(self.tags.all())
        )

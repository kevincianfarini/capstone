from rest_framework import serializers
from files.models import BlogPost, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class BlogPostSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = BlogPost
        exclude = ('body', )
        
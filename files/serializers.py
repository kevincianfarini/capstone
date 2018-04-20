from rest_framework import serializers
from files.models import BlogPost, Tag, Blog


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', )


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('name', )


class BlogPostSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    tags = TagSerializer(many=True)
    blog = BlogSerializer()

    class Meta:
        model = BlogPost
        exclude = ('body', )
        
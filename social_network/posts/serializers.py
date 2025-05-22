from rest_framework import serializers

from .models import Comment, Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ['author', 'post', 'text', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        image = serializers.ImageField(required=False)
        fields = ['id', 'text', 'image', 'comments', 'likes_count']

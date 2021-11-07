from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author_name = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "author", "author_name", "content", "creation_date"]


class CommentDetailSerializer(serializers.ModelSerializer):

    author_name = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "author_name", "content", "creation_date"]
        read_only_fields = ["post"]

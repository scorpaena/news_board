from rest_framework import serializers
from .models import Post, PostUpvote


class PostSerializer(serializers.ModelSerializer):

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author_name = serializers.CharField(source="author.username", read_only=True)
    upvotes_amount = serializers.IntegerField(source="upvotes.count", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "link",
            "creation_date",
            "author",
            "author_name",
            "upvotes_amount",
        ]


class PostUpvoteSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PostUpvote
        fields = ["user", "post"]

    def create(self, validated_data):
        upvote, _ = PostUpvote.objects.get_or_create(**validated_data)
        return upvote

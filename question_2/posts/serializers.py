from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    # Display the author's username (read-only); the author is set
    # automatically from the authenticated user in the view.
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

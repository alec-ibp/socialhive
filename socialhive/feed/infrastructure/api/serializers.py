from rest_framework import serializers

from socialhive.feed.domain.models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        exclude = ("user", "is_active")

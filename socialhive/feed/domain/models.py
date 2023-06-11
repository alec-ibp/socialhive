from django.db import models

from socialhive.common.utils.validators import alphanumeric_with_special_characters


class Post(models.Model):
    content = models.CharField(
        max_length=200,
        null=False, blank=False,
        validators=[alphanumeric_with_special_characters],
        help_text="Post content"
    )
    url = models.CharField(max_length=200, null=True, blank=True)
    image_path = models.CharField(max_length=200, null=True, blank=True)
    published = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey('common.HiveUser', on_delete=models.CASCADE)
    # comments
    # likes

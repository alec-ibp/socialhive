from typing import Optional
from socialhive.common.models import HiveUser


class NewPostDTO:
    def __init__(self, content: str, user: HiveUser, url: Optional[str]=None, image_path: Optional[str]=None):
        self.content = content
        self.url = url or None
        self.image_path = image_path or None
        self.user = user

    def to_dict(self):
        return {
            'content': self.content,
            'url': self.url,
            'image_path': self.image_path,
            'user': self.user
        }


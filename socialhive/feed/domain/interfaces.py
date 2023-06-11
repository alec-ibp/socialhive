from abc import ABC, abstractmethod

from socialhive.feed.domain.models import Post
from socialhive.feed.domain.dtos import NewPostDTO


class PostServiceRepositoryInterface(ABC):
    @abstractmethod
    def save(self, post: NewPostDTO) -> Post:
        pass

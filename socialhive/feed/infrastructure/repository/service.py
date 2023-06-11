from socialhive.feed.domain.models import  Post
from socialhive.feed.domain.dtos import NewPostDTO
from socialhive.feed.domain.interfaces import PostServiceRepositoryInterface


class PostServiceRepository(PostServiceRepositoryInterface):
    def save(self, post: NewPostDTO) -> Post:
        return Post.objects.create(**post.to_dict())

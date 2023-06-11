from socialhive.feed.domain.models import Post
from socialhive.feed.domain.dtos import NewPostDTO
from socialhive.feed.domain.interfaces import PostServiceRepositoryInterface


class PostManager:
    def __init__(self, repository: PostServiceRepositoryInterface):
        self.repository = repository

    def create_post(self, post_dto: NewPostDTO) -> Post:
        post = self.repository.save(post_dto)
        
        if isinstance(post, Post):
            # TODO if created send to the microservice to process the text sentiment analysis
            pass
        return post

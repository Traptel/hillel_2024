from abc import ABC, abstractmethod
from datetime import datetime


class Post:
    def __init__(self, message: str, timestamp: int):
        self.message = message
        self.timestamp = timestamp


class SocialChannel(ABC):
    def __init__(self, type: str, followers: int):
        self.type = type
        self.followers = followers

    @abstractmethod
    def make_a_post(self, message: str) -> None:
        pass


class Youtube(SocialChannel):
    def make_a_post(self, message: str) -> None:
        print(
            f"Posting '{message}' to {self.type}"
            f" with {self.followers} followers"
        )


class Facebook(SocialChannel):
    def make_a_post(self, message: str) -> None:
        print(
            f"Posting '{message}' to {self.type}"
            f" with {self.followers} followers"
        )


class Twitter(SocialChannel):
    def make_a_post(self, message: str) -> None:
        print(
            f"Posting '{message}' to {self.type}"
            f" with {self.followers} followers"
        )


def post_a_message(channel: SocialChannel, message: str) -> None:
    channel.make_a_post(message)


def process_schedule(posts: list[Post], channels: list[SocialChannel]) -> None:
    current_time = int(datetime.now().strftime("%H"))
    for post in posts:
        message, timestamp = post.message, post.timestamp
        for channel in channels:
            if timestamp <= current_time:
                post_a_message(channel, message)


if __name__ == "__main__":
    posts = [
        Post(message="New video!", timestamp=20),
        Post(message="News video coming soon!", timestamp=17),
    ]

    channels = [
        Youtube(type="Youtube", followers=10_000),
        Facebook(type="Facebook", followers=20_000),
        Twitter(type="Twitter", followers=30_000),
    ]

    process_schedule(posts, channels)

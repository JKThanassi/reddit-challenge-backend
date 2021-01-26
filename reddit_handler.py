from typing import List
from enum import Enum
import requests

# This is an enumeration representing the valid states for a top posts query
TopPeriod = Enum("TopPeriod", "hour day week month year all")


class RedditError(Exception):
    def __init__(self, message):
        self.message = message


def get_posts_from_sub(
    subreddit: str, top: TopPeriod = TopPeriod.day, count: int = 20
) -> List[dict]:
    """
    This function handles getting and formatting data from reddit into a paired down state for displaying

    Args:
        subreddit: A string containing the name of a subreddit
        top: the time range of top posts requested
        count: the amount of posts to get
    """
    # User agent string emulating firefox so reddit doesn't rate limit me
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    res = requests.get(
        f"https://www.reddit.com/r/{subreddit}/top/.json",
        headers=headers,
        params={"t": top, "limit": count},
    )

    if res.status_code == 200:
        children = res.json().get("data").get("children")
        if len(children) == 0:
            raise RedditError(
                message=f"{subreddit} has no posts or is an invalid subreddit"
            )
        return [strip_superfluous(post) for post in children]
    else:
        error = res.json().get("message")
        raise RedditError(
            message=f"Reddit error: {error} occurred when trying to query subreddit: {subreddit}"
        )


def strip_superfluous(post: dict) -> dict:
    """
    This function takes a post listing and returns only the post link, author, num upvotes, post title, post type (link or text), and author name
    Args:
        post: a dictionary containing data for one post from the reddit API

    Returns: a dictionary containing the post link, author, num upvotes, post title, post type, and author name

    """
    if post is None:
        raise RedditError(message="Post returned with no data")
    post_data = post.get("data")
    return {
        "title": post_data.get("title"),
        "score": post_data.get("score"),
        "isLinkPost": is_post_link(post_data),
        "externalURL": post_data.get("url_overridden_by_dest"),
        "redditLink": f'https://www.reddit.com{post_data.get("permalink")}',
        "submitter": post_data.get("author"),
    }


def is_post_link(post: dict) -> bool:
    """
    This checks if a post is a link type
    Args:
        post: The reddit api listing for a post

    Returns: True if post is a link post and false otherwise

    """
    return "url_overridden_by_dest" in post.keys()

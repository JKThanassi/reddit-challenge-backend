import pytest
from unittest import mock
from reddit_handler import (
    get_posts_from_sub,
    RedditError,
    strip_superfluous,
    is_post_link,
)
from api import validate_sub_endpoint_params
import requests
import json


@mock.patch.object(requests, "get")
def test_get_posts_from_sub_error_bad_sub(mock_requests):
    mock_requests.return_value = mock.Mock(
        status_code=404, json=lambda: {"message": "NOT FOUND"}
    )
    with pytest.raises(RedditError) as re:
        get_posts_from_sub("bad_sub")
    assert (
        re.value.message
        == "Reddit error: NOT FOUND occurred when trying to query subreddit: bad_sub"
    )


@mock.patch.object(requests, "get")
def test_get_posts_from_sub_error_no_posts(mock_requests):
    mock_requests.return_value = mock.Mock(
        status_code=200, json=lambda: {"data": {"children": []}}
    )
    with pytest.raises(RedditError) as re:
        get_posts_from_sub("good_or_bad_sub_who_knows")
    assert (
        re.value.message
        == "good_or_bad_sub_who_knows has no posts or is an invalid subreddit"
    )


@mock.patch.object(requests, "get")
def test_get_posts_from_sub(mock_requests):

    with open("redditpost.json") as rp:
        ret_json = json.load(rp)
        mock_requests.return_value = mock.Mock(status_code=200, json=lambda: ret_json)
        res = get_posts_from_sub("askreddit")
        assert len(res) == 1 and res[0] == strip_superfluous(
            ret_json.get("data").get("children")[0]
        )


def test_strip_superflous():
    stripped_post = {
        "title": "At 9:21 tonight, it will be the 21st minute of the 21st hour of the 21st day of the 21st year of the 21st century. What will you be doing?",
        "score": 111463,
        "isLinkPost": False,
        "externalURL": None,
        "redditLink": "https://www.reddit.com/r/AskReddit/comments/l2d1la/at_921_tonight_it_will_be_the_21st_minute_of_the/",
        "submitter": "FilthyMcNasty108",
    }
    with open("redditpost.json") as rp:
        post = json.load(rp)
        assert stripped_post == strip_superfluous(post.get("data").get("children")[0])


def test_is_link_post_true():
    assert is_post_link({"url_overridden_by_dest": "http://www.joekt.dev"})


def test_is_link_post_false():
    assert not is_post_link(
        {"there": "can be anything here so long as no url_overridden_by_dest"}
    )


def test_validate_endpoint_params_good():
    assert validate_sub_endpoint_params({"count": 20, "top": "all"})
    assert validate_sub_endpoint_params({"top": "all"})
    assert validate_sub_endpoint_params({"count": 20})


def test_validate_endpoint_params_good_key_bad_val():
    assert not validate_sub_endpoint_params({"count": 0, "top": "all"})
    assert not validate_sub_endpoint_params({"count": 3, "top": "3.5Ga"})
    assert not validate_sub_endpoint_params({"count": 3, "top": None})
    assert not validate_sub_endpoint_params({"count": None})

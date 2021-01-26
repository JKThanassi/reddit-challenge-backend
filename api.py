from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
from reddit_handler import get_posts_from_sub, RedditError, TopPeriod

app = Flask(__name__)
CORS(app)  # enable cross origin requests since this is a public api
valid_sub_params = {
    "top",
    "count",
}  # set representing the valid parameters for the sub endpoint


@app.route("/sub/<string:subreddit>")
@cross_origin(origins="*")
def get_subreddit_top_posts(subreddit: str) -> dict:
    if validate_sub_endpoint_params(request.args):
        try:
            return {
                "posts": get_posts_from_sub(subreddit, **request.args),
                "name": subreddit,
            }
        except RedditError as e:
            return Response(e.message, 400)
    else:
        return Response("Bad route parameters", 400)


def validate_sub_endpoint_params(request_args: dict) -> bool:
    """
    This function validates that the url parameters are valid.
    It ensures that:
        The parameters are a subset of 'top' and 'count'
        The count arg, if present, is greater than or equal to 1
        The top arg, if present, is one of the allowed values as defined in the TopPeriod enum
    Args:
        request_args: the request arguments passed in

    Returns: True if everything is valid and false otherwise

    """
    if not valid_sub_params.issuperset(request_args.keys()):
        return False
    if "count" in request_args and (
        request_args.get("count") is None or int(request_args.get("count")) < 1
    ):
        return False
    if "top" in request_args and (
        request_args.get("top") is None
        or not (request_args.get("top") in TopPeriod.__members__)
    ):
        return False
    return True

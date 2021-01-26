# Cisco Reddit Challenge
## Author: Joseph Kaming-Thanassi

Deployed at [https://reddit-challenge-backend.herokuapp.com/](https://reddit-challenge-backend.herokuapp.com/)

### Description
This api is built using:
- Flask
  - Handles general api functionality such as routing, responses, and CORS.
- Requests
  - Handles external api requests. In this case I used it to contact Reddit's API.
- Gunicorn
  - This is a wsgi compatible server used in the production deployment on heroku.
- pytest
    - This is the unit test framework I used to test the app.

The one and only endpoint exposed to the user is `/sub/<subreddit>`. 
This endpoint can be queried with url parameters to specify the top duration and amount of posts.

For example: `sub/news?top=all&count=30` will query the top posts of all time and return the top 30.

**Note**: If no query params are specified, top day and count 20 will be used by default.

The top parameter will only accept the times specified by reddit: `hour, day, week, month, year, or all`.

This endpoint will get the top posts for a subreddit and return
a json object in this form:
```json
{
        "title": "Post Title Here",
        "score": 1111,
        "isLinkPost": true,
        "externalURL": "https://www.joekt.dev",
        "redditLink": "https://www.reddit.com/r/haskell/posttitlehere",
        "submitter": "joekt"
    }
```
where:
- title is the post title
- score is the post score (upvotes - downvotes)
- externalURL is the url included in a link post (null if not a link post)
- redditLink is the permalink to the post on reddit
- submitter is the username of the post submitter

### How to run
1. Make sure you have python 3.8.1 and pipenv installed
    - If on mac, run `brew install pipenv`
    - I use pyenv to manage my python versions, see the below section to use that if desired.
        - Do this before running pipenv
2. In the root directory of the project, run `pipenv install`
    - This will install the necessary dependencies
3. Once that is complete, run pipenv shell to activate the generated virtualenv 
4. To get the dev server up and running
   - In the root directory of the project run `export FLASK_APP=api.py`
   - Then run `flask run` or `python -m flask run` within the pip shell 

### Using pyenv to install python 3.8.1
1. Install pyenv
    - if on mac, run: `brew install pyenv`
2. Then run `pyenv install 3.8.1`
3. add `eval "$(pyenv init -)"` to your .bashrc or .zshrc and restart your terminal
    - Run `pyenv global 3.8.1` to set this as your default system python version if desired
    - Run `which python` to see if it worked
    - The output should be something like this: `~/.pyenv/versions/3.8.1/bin/python`

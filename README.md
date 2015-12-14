Black Bart
----------
## PROBLEM
I don't like trawling through email lists that I'm not taking part in, but I like reading what smart people have to say about technical things. 

## Solution
This project mirrors mailing lists on subreddits, to make it easier to browse and read messages. You can see it in action with the [bitcoin-development mailing list](http://lists.linuxfoundation.org/pipermail/bitcoin-dev/) on [r/bitcoin_devlist](http://reddit.com/r/bitcoin_devlist).

To achieve the goal, I've created a Django app with the following components:
   1. A miner that consumes the mailing list from within a Django management shell command and saves the data to Django models.
   2. Another Django management command that posts top-level messages to the subreddit as submissions.
   3. One last Django management command that posts comments to their relevant submissions on the subreddit.

## TODO:
1. Move Reddit authentication to OAuth: https://www.reddit.com/comments/2ujhkr/

## Quick Start
1. Install virtualenvwrapper
2. `mkvirtualenv blackbart`
3. Clone the blackbart directory w/ something like `git clone `https://github.com/kvnn/blackbart.git
3. Go into the blackbart directory in your terminal
4. `pip install -r requirements.txt`
5. Set up a database and include the connection info in .env
6. `python manage.py makemigrations`
7. `python manage.py migrate`
8. Create your subreddit, and include the credential info in .env
9. `python manage.py mine`
10. `python manage.py submissions_to_reddit`
11. `python manage.py comments_to_reddit`

## Architecture
### .env file
This is mandatory, as some Django and Reddit (praw) settings are expected to be stored here. See .env_sample for a starting point.
Note that DJANGO_SETTINGS_MODULE should be changed if you want to put in a production, or whatever, settings file.
    
    export DJANGO_SETTINGS_MODULE="blackbart.settings.dev"
    export BASE_API_URL="http://127.0.0.1:8001"
    export REDDIT_BITCOIN_DEV_SUBREDDIT="bitcoin_devlist"
    export REDDIT_BITCOIN_DEV_UA='bitcoin-dev blackbart by /u/kvnn'
    export REDDIT_BITCOIN_DEV_USERNAME="bitcoin-devlist-bot"
    export REDDIT_BITCOIN_DEV_PW="my_stupid_password"
    export DB_ENGINE="django.db.backends.postgresql_psycopg2"
    export DB_NAME="postgres_db_name"
    export DB_HOST="127.0.0.1"
    export DB_PORT="5432"
    export DB_USERNAME="postgres_username"
    export DB_PASSWORD="postgres_password"


### App name
If you fork this and change the name, do a global search & replace for "blackbart". There are some config files with the app name, like manage.py and settings/__init__.py.

### API
I've included an api and some endpoints for convenience after running the miner. After running the miner, I like to visit /api/v1.0/messages/top-level/new/ to see new top-level messages and /api/v1.0/messages/new/ to see all new messages. I then visit them again after running the reddit-submission-submitter and the reddit-comment-submitter.

### Miner
The miner app uses the [mine](blackbart/apps/miner/management/commands/mine.py) Django management command to scrape the mailing list specified in .env. The scraping is done by a Scrapy spider in [spiders.py](blackbart/apps/miner/scraper/spiders.py), which sends data to [pipelines.py](blackbart/apps/miner/scraper/pipelines.py) for saving.

### Distributor
The distributor uses the [submissions_to_reddit](blackbart/apps/distributor/management/commands/submissions_to_reddit.py) & [comments_to_reddit](blackbart/apps/distributor/management/commands/comments_to_reddit.py) Django management commands to post submissions and comments to the subreddit specified in .env, respectively.

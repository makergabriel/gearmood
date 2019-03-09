# Gear Mood project

The good people on the sub reddit https://www.reddit.com/r/Ultralight/ have provided so much helpful information over the years through "shakedown" requests.  This project is focused on giving back to that community by providing an automated way to gauge the mood of gear shakedown requests.

https://www.reddit.com/r/Ultralight/comments/626sh1/how_to_ask_for_a_pack_shakedown/

## Getting Started

Clone the repo
```
git clone https://github.com/makergabriel/gearmood.git
```

Install python - https://docs.python-guide.org/starting/installation/
Install postgreSQL - https://www.postgresql.org/

Install gearmood database on posgres
```
sudo -u postgres psql
create database gearmood
create user gearmood_app with encrypted password 'gearmood_app';
grant all privileges on database gearmood to gearmood_app;
```
Create the tables - run the sql commands in sql/create_gearmood.sql

Setup Reddit api access
https://praw.readthedocs.io/en/latest/getting_started/quick_start.html
Create config/praw.ini

Create config/gearmood.ini
```
[DatabaseSection]
database.dbname=gearmood
database.host=localhost
database.user=gearmood_app
database.password=gearmood_app

[Reddit]
subreddit=Ultralight
site_name=<your praw api name>
user_agent=<your praw api user agent>
```

Setup python virtualenv - or roll with global pip installs
```
pip install virtualenv
cd <project root>/python_scripts
# create virtual environment for python - this is really neat!
virtualenv venv
# activate venv so that your running from the virtual env
source venv/bin/activate
# you should see (venv) in front of you terminal prompt now
# install all the required python packages to your virtual env
pip install -r requirements.txt
```

### Prerequisites
macbook pro - just kidding, whatever you got just tweak your commands per OS
reddit API account access
praw
python 3.7.x
pip
postgreSQL

```
Give examples
```

### Installing

I only have this running locally currently - one day I'll "install" it and explain it here.

Run shakedown_handler.py

```
python shakedown_handler.py
```

Adjust the req_limit, comment_limit
TODO add the created_dt and automate to keep track of which submissions have been processed and look for updates

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning
This is a good idea, I should create some versions.

0.1 - initial project and planning/learning the features

## Authors

* **Bobby Gabriel** - *Initial work*

See also the list of [contributors](https://github.com/makergabriel/gearmood/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* https://www.reddit.com/r/Ultralight/
* https://www.reddit.com/r/Ultralight/comments/626sh1/how_to_ask_for_a_pack_shakedown/
* https://www.lighterpack.com/
* https://praw.readthedocs.io/en/latest/index.html
* https://gist.github.com/PurpleBooth/109311bb0361f32d87a2

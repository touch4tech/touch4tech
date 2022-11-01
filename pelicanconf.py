from os.path import abspath,join
AUTHOR = 'Rezpe & Oberron'
SITENAME = "French-Touch.dev"
SITEABOUT = "One brick at a time contributing to the DKIW pyramid fundation"
SITEURL = 'https://frenchtouch.dev'

print(20,"test",SITEURL)


PATH = 'content'
STATIC_PATHS = ["img","webvtt"]
OUTPUT_PATH = 'public'
PLUGINS = ['sitemap', 'pelican-ipynb.markup']


TIMEZONE = 'Europe/Rome'

DEFAULT_LANG = 'en'
MARKUP = ('md', )
from pelican_jupyter import liquid as nb_liquid
PLUGINS = [nb_liquid]

IGNORE_FILES = [".ipynb_checkpoints"]

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = "feed.xml" #MCV changed for testing
#FEED_ALL_ATOM = None
RSS_FEED_SUMMARY_ONLY = False
FEED_RSS_URL = True
FEED_MAX_ITEMS = 100
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DELETE_OUTPUT_DIRECTORY = True

# Blogroll
LINKS = (('Pelican', 'https://getpelican.com/'),
         ('Python.org', 'https://www.python.org/'),
         ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

CONTACTS = [
    ("Twitter", "twitter", "https://twitter.com/frenchtouchdev"),
    ("YouTube","youtube","https://www.youtube.com/@frenchtouchdev"),
    ("tiktok","tiktok","https://www.tiktok.com/@frenchtouchdev"),
    ("Facebook", "facebook-f", "https://www.facebook.com/frenchtouch.dev"),
    ("GitHub","github","https://github.com/french-touch/frenchtouch"),
    ("Podcast","podcast","https://feeds.soundcloud.com/users/soundcloud:users:404637861/sounds.rss"),
    ("Instagram", "instagram", "https://www.instagram.com/frenchtouch.dev/"),
    ("Email", "envelope", "mailto:tellme@frenchtouch.dev"),
]

DEFAULT_PAGINATION = 10

"""
def csv(content, *args):
    fp = abspath(join("D:/Git/admin.git/content/static/csv/","test.csv"))
    with open(fp,'r') as fi:
        csv_data = fi.read()
    return csv_data

JINJA_FILTERS = {
    'csv': csv,
}
"""

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

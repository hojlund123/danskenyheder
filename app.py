from flask import Flask, render_template
import feedparser
from urllib.parse import urlparse

app = Flask(__name__)

# RSS feed URLs for dr.dk, tv2.dk, bt.dk, and eb.dk
FEED_URLS = [
    'https://www.dr.dk/nyheder/service/feeds/allenyheder',
    'https://feeds.tv2.dk/nyhederne_seneste/rss',
    'https://www.bt.dk/feed/seneste',
    'https://ekstrabladet.dk/rssfeed/all/',
    #testet hertil
    'https://borsen.dk/rss',
    'https://rss.dst.dk/Site/Rss/feeds/Overskrifter.xml',
    'https://ing.dk/rss'
]

DOMAIN_NAMES = {
    'www.dr.dk': 'DR',
    'feeds.tv2.dk': 'TV2',
    'www.bt.dk': 'BT',
    'ekstrabladet.dk': 'Ekstra Bladet',
    'borsen.dk': 'Børsen',
    'rss.dst.dk': 'DST',
    'ing.dk': 'Ingeniøren'
}

@app.route('/')
def index():
    # Parse the RSS feeds and get the latest news articles from each source
    articles = []
    for feed_url in FEED_URLS:
        feed = feedparser.parse(feed_url)
        for entry in feed['entries']:
            # Extract the domain name from the article's link URL
            domain = urlparse(entry.link).netloc
            # Map the domain name to a custom name (if it exists)
            name = DOMAIN_NAMES.get(domain, domain)
            # Add the custom name to the article dictionary
            entry['name'] = name
            # Add the article to the list
            articles.append(entry)
    # Sort the articles by date (newest first)
    articles = sorted(articles, key=lambda article: article.published_parsed, reverse=True)
    return render_template('index.html', articles=articles)


@app.route('/article/<int:article_id>')
def article(article_id):
    # Parse the RSS feeds and get the article based on its ID
    articles = []
    for feed_url in FEED_URLS:
        feed = feedparser.parse(feed_url)
        articles.extend(feed['entries'])
    article = articles[article_id]
    return render_template('article.html', article=article)

if __name__ == '__main__':
    app.run(debug=True)

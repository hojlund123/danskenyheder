from flask import Flask, render_template
import feedparser

app = Flask(__name__)

# RSS feed URLs for dr.dk, tv2.dk, bt.dk, and eb.dk
FEED_URLS = [
    'https://www.dr.dk/nyheder/service/feeds/allenyheder',
    'https://feeds.tv2.dk/nyhederne_seneste/rss',
    'https://www.bt.dk/feed/seneste',
    'https://ekstrabladet.dk/rssfeed/all/'
]

@app.route('/')
def index():
    # Parse the RSS feeds and get the latest news articles from each source
    articles = []
    for feed_url in FEED_URLS:
        feed = feedparser.parse(feed_url)
        articles.extend(feed['entries'])
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

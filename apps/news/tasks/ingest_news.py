import requests
import feedparser
from datetime import datetime
from django.utils.timezone import make_aware
from ..models import Article, Source

def fetch_news_from_sources():
    sources = Source.objects.all()
    for src in sources:
        if src.source_type == 'rss':
            _fetch_rss_feed(src)
        elif src.source_type == 'news':
            _fetch_news_api(src)
        # extend: gov, social, etc.

def _fetch_rss_feed(source):
    feed = feedparser.parse(source.url)
    for entry in feed.entries:
        Article.objects.get_or_create(
            url=entry.link,
            defaults={
                'source': source,
                'title': entry.title,
                'published_at': make_aware(datetime(*entry.published_parsed[:6])),
                'content': entry.get('summary', ''),
            }
        )

def _fetch_news_api(source):
    response = requests.get(source.url)
    if not response.ok:
        return
    data = response.json()
    for item in data.get('articles', []):
        Article.objects.get_or_create(
            url=item['url'],
            defaults={
                'source': source,
                'title': item['title'],
                'published_at': make_aware(datetime.fromisoformat(item['publishedAt'].replace('Z', '+00:00'))),
                'content': item.get('content', ''),
            }
        )

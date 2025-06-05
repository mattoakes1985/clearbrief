import feedparser
import requests
from datetime import datetime
from django.utils.timezone import make_aware
from apps.news.models import Source, Article

def fetch_sources():
    sources = Source.objects.filter(is_active=True)

    for source in sources:
        print(f"[SCRAPE] Attempting to fetch: {source.name} ({source.source_type})")

        try:
            parser = source.parser_override or source.source_type
            headers, params = build_request_config(source)

            if parser == 'rss':
                _fetch_rss(source, headers=headers)
            elif parser == 'news' or parser == 'json':
                _fetch_api(source, headers=headers, params=params)
            else:
                print(f"[WARN] Unknown parser '{parser}' for {source.name}")
        except Exception as e:
            print(f"[ERROR] Failed to process {source.name}: {e}")


def build_request_config(source):
    headers = {}
    params = {}

    for rule in source.rules.all():
        if rule.rule_type == 'header':
            headers[rule.key] = rule.value
        elif rule.rule_type == 'param':
            params[rule.key] = rule.value
        elif rule.rule_type == 'auth':
            headers['Authorization'] = rule.value
        elif rule.rule_type == 'user_agent':
            headers['User-Agent'] = rule.value

    return headers, params


def _fetch_rss(source, headers=None):
    # feedparser doesn't accept custom headers; we may need `requests` later if needed
    feed = feedparser.parse(source.url)
    for entry in feed.entries:
        if Article.objects.filter(url=entry.link).exists():
            continue

        published = entry.get('published_parsed')
        published_dt = make_aware(datetime(*published[:6])) if published else None

        Article.objects.create(
            source=source,
            title=entry.title,
            url=entry.link,
            published_at=published_dt,
            content=entry.get('summary', '')[:2000],
            summary=entry.get('summary', '')[:1000],
        )


def _fetch_api(source, headers=None, params=None):
    headers = headers or {}
    params = params or {}
    try:
        response = requests.get(source.url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        for item in data.get('articles', []):
            if Article.objects.filter(url=item.get('url')).exists():
                continue

            published_dt = make_aware(datetime.fromisoformat(item['publishedAt']))

            Article.objects.create(
                source=source,
                title=item.get('title'),
                url=item.get('url'),
                published_at=published_dt,
                content=item.get('content', '')[:2000],
                summary=item.get('description', '')[:1000],
            )

    except Exception as e:
        print(f"[ERROR] API fetch failed for {source.name}: {e}")

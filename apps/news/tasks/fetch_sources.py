from celery import shared_task
from apps.news.services.fetch_sources import fetch_sources
from apps.news.tasks.process_new_articles import process_new_articles
from apps.news.models import Article

@shared_task
def fetch_sources_task():
    before = Article.objects.count()

    fetch_sources()

    after = Article.objects.count()
    new_articles = after - before

    if new_articles > 0:
        print(f"[INFO] {new_articles} new articles found. Launching tagging/summarisation.")
        process_new_articles.delay()
    else:
        print("[INFO] No new articles found. Skipping tagging/summarisation.")

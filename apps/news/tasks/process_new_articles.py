# apps/news/tasks/process_new_articles.py

from celery import shared_task
from django.db.models import Q
from apps.news.models import Article
from apps.news.services.tagging import tag_article
from apps.news.services.summarisation import summarise_article

@shared_task
def process_new_articles():
    articles = Article.objects.filter(
        Q(summary_structured__isnull=True) | Q(tags__isnull=True) | Q(tags=[])
    )

    for article in articles:
        updated = False

        # Tag if needed
        if not article.tags:
            try:
                tags = tag_article(article)
                article.tags = tags
                updated = True
            except Exception as e:
                print(f"❌ Tagging failed for '{article.title}': {e}")

        # Summarise if needed
        if article.summary_structured is None:
            try:
                summary = summarise_article(article)
                article.summary_structured = summary
                updated = True
            except Exception as e:
                print(f"❌ Summarisation failed for '{article.title}': {e}")

        if updated:
            article.save()

# apps/news/tasks/fetch_sources.py

from celery import shared_task
from apps.news.services.fetch_sources import fetch_sources
from apps.news.tasks.process_new_articles import process_new_articles  # 👈 ADD THIS

@shared_task
def fetch_sources_task():
    fetch_sources()

    # Automatically trigger downstream tagging/summarisation
    process_new_articles.delay()  # 👈 ADD THIS

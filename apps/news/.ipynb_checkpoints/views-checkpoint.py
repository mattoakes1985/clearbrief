# apps/news/views.py

from django.shortcuts import render
from apps.news.models import Article

def digest_preview(request):
    article = Article.objects.latest("published_at")
    summary = article.summary_structured or {}

    card = {
        "headline": summary.get("headline", article.title),
        "signal": summary.get("signal", ""),
        "context": summary.get("context", ""),
        "action": summary.get("action", ""),
        "entities": summary.get("tags", {}).get("entities", []),
        "sentiment": summary.get("tags", {}).get("sentiment", ""),
        "topics": summary.get("tags", {}).get("topics", []),  # Optional
        "url": article.url,
        "published_at": article.published_at,
    }

    return render(request, "news/digest_card.html", {"card": card})

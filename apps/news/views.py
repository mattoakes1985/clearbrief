from django.shortcuts import render
from apps.news.models import Article
from apps.news.services.summarisation import summarise_article
from apps.news.services.tagging import tag_article
import pprint

def digest_preview(request):
    article = Article.objects.latest("published_at")
    summary = summarise_article(article)
    tags = tag_article(article)

    card = {
        "headline": summary.get("headline"),
        "signal": summary.get("signal"),
        "context": summary.get("context"),
        "action": summary.get("action"),
        "sentiment": tags.get("sentiment", "unknown"),
        "entities": tags.get("entities", []),
        "published_at": summary.get("published_at"),
        "url": summary.get("source_url")
    }

    print("\n=== DEBUG: Final card passed to template ===")
    pprint.pprint(card)

    return render(request, "news/digest_preview.html", {"card": card})

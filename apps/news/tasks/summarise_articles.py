from apps.news.models import Article
from apps.news.services.summarisation import summarise_article

def summarise_all_articles():
    for article in Article.objects.filter(summary_structured__isnull=True):
        structured = summarise_article(article)
        article.summary_structured = structured
        article.save()

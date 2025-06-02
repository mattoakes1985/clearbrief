from apps.news.models import Article
from apps.news.services.tagging import tag_article

def tag_all_articles():
    for article in Article.objects.filter(tags=[]):
        tags = tag_article(article)
        article.tags = tags
        article.save()

from django.db import models

class Source(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    source_type = models.CharField(
        max_length=50,
        choices=[
            ('news', 'News API'),
            ('rss', 'RSS Feed'),
            ('gov', 'Government'),
            ('social', 'Social Media')
        ]
    )

    def __str__(self):
        return f"{self.name} ({self.source_type})"

class Article(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    title = models.TextField()
    url = models.URLField(unique=True)
    published_at = models.DateTimeField()
    seen_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    tags = models.JSONField(default=list)
    is_duplicate = models.BooleanField(default=False)
    summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

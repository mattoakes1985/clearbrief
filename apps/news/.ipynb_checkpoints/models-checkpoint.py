from django.db import models
from django.contrib.postgres.fields import JSONField  # for Postgres

class Source(models.Model):
    SOURCE_TYPE_CHOICES = [
        ('news', 'News API'),
        ('rss', 'RSS Feed'),
        ('gov', 'Government'),
        ('social', 'Social Media'),
        ('custom', 'Custom Scraper')
    ]

    name = models.CharField(max_length=255)
    url = models.URLField(max_length=500, unique=True)
    source_type = models.CharField(max_length=50, choices=SOURCE_TYPE_CHOICES)
    parser_override = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Force parser method (e.g., 'rss', 'json', 'html')"
    )
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, help_text="Scraping notes, known issues, etc.")
    trust_score = models.FloatField(default=0.5, help_text="0 = untrusted, 1 = highly trusted")
    last_fetched = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.source_type})"


class SourceRule(models.Model):
    RULE_TYPE_CHOICES = [
        ('header', 'HTTP Header'),
        ('param', 'URL Parameter'),
        ('rate_limit', 'Rate Limit'),
        ('parser', 'Parser Override'),
        ('postprocess', 'Post-processing'),
        ('auth', 'Auth Token'),
        ('user_agent', 'User-Agent'),
        ('transform', 'Content Transform')
    ]

    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='rules')
    rule_type = models.CharField(max_length=50, choices=RULE_TYPE_CHOICES)
    key = models.CharField(max_length=255)
    value = models.TextField()

    def __str__(self):
        return f"{self.source.name}: {self.rule_type} - {self.key}"

class Article(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    title = models.TextField()
    url = models.URLField(max_length=500, unique=True)
    published_at = models.DateTimeField()
    seen_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    tags = models.JSONField(default=list)
    is_duplicate = models.BooleanField(default=False)
    summary = models.TextField(blank=True, null=True)
    summary_structured = models.JSONField(null=True, blank=True)


    def __str__(self):
        return self.title


    

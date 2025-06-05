# apps/news/management/commands/extract_sources.py

from django.core.management.base import BaseCommand
from apps.news.models import Source

class Command(BaseCommand):
    help = 'Extract all source definitions for review'

    def handle(self, *args, **kwargs):
        sources = Source.objects.all().order_by('name')

        for src in sources:
            self.stdout.write("\n" + "-"*60)
            self.stdout.write(f"Name       : {src.name}")
            self.stdout.write(f"Type       : {src.source_type}")
            self.stdout.write(f"URL        : {src.url}")
            self.stdout.write(f"Active     : {'Yes' if src.is_active else 'No'}")
            self.stdout.write(f"Trust Score: {src.trust_score}")
            self.stdout.write(f"Last Fetched: {src.last_fetched}")
            self.stdout.write("-"*60 + "\n")

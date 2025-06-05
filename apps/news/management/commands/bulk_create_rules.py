from django.core.management.base import BaseCommand
from apps.news.models import Source, SourceRule

class Command(BaseCommand):
    help = "Bulk create scraping rules for all known sources"

    def handle(self, *args, **kwargs):
        def create_rule(source_name, rule_type, key, value):
            try:
                source = Source.objects.get(name=source_name)
                SourceRule.objects.update_or_create(
                    source=source,
                    rule_type=rule_type,
                    key=key,
                    defaults={'value': value}
                )
            except Source.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"⚠️  Source not found: {source_name}"))

        # RSS
        rss_sources = [
            "Al Jazeera", "BBC News RSS", "bBC World News", "BMJ News",
            "Bellingcat (OSINT)", "CDC Newsroom", "Government Think Tanks", "NHIR",
            "NHS England Blogs", "NHSE Statistical Publications", "ONS", "Reuters",
            "Stratfor", "The Guardian World News", "The Spectator", "The Telegraph",
            "WHO Disease Outbreaks"
        ]
        for name in rss_sources:
            create_rule(name, "rss", "parser", "standard")

        # HTML scraping
        html_scrapers = {
            "Data.Gov.Uk": "div.dataset-item a",
            "Financial Times": "article div.o-teaser__heading",
            "The Times": "div.article",
            "UKHSA": "li.collection a",
            "UN Data Portal": "div#datasets a",
            "WHO": "div.list-view a",
            "World Bank": "div.indicator-card",
        }
        for name, selector in html_scrapers.items():
            create_rule(name, "html", "selector", selector)

        # API-based sources
        api_sources = {
            "Pushshift Reddit API": {
                "endpoint": "https://api.pushshift.io/reddit/search/submission/",
                "params": "q=ukraine&sort=desc&size=10",
            },
            "factba.se": {
                "endpoint": "https://api.factba.se/v1",
                "auth_required": "true",
            },
            "open corporates api": {
                "endpoint": "https://api.opencorporates.com/v0.4/companies/search",
                "params": "q=Pfizer",
                "auth_required": "true",
            },
            "World Bank API": {
                "endpoint": "https://api.worldbank.org/v2/indicator/SP.POP.TOTL",
                "params": "format=json",
            },
            "PHE Fingertips": {
                "endpoint": "https://fingertips.phe.org.uk/api/profiles",
            },
            "Endpoint open threat exchange": {
                "endpoint": "https://otx.alienvault.com/api/v1/indicators/export",
                "auth_required": "true",
            },
        }
        for name, rules in api_sources.items():
            for key, value in rules.items():
                create_rule(name, "api", key, value)

        # Restricted sites
        restricted_sources = ["Daily Mail", "Financial Times", "The Times"]
        for name in restricted_sources:
            create_rule(name, "html", "restricted", "true")
            create_rule(name, "html", "strategy", "metadata_only")

        self.stdout.write(self.style.SUCCESS("✅ Rules created successfully."))

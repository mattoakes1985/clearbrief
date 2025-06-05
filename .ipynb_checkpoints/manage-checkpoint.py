#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()




from apps.news.models import Source, SourceRule

def create_rule(source_name, rule_type, key, value):
    source = Source.objects.get(name=source_name)
    SourceRule.objects.update_or_create(
        source=source,
        rule_type=rule_type,
        key=key,
        defaults={'value': value}
    )

# --- RSS Standard Sources ---
rss_sources = [
    "Al Jazeera",
    "BBC News RSS",
    "bBC World News",
    "BMJ News",
    "Bellingcat (OSINT)",
    "CDC Newsroom",
    "Government Think Tanks",
    "NHIR",
    "NHS England Blogs",
    "NHSE Statistical Publications",
    "ONS",
    "Reuters",
    "Stratfor",
    "The Guardian World News",
    "The Spectator",
    "The Telegraph",
    "WHO Disease Outbreaks",
]

for name in rss_sources:
    create_rule(name, "rss", "parser", "standard")

# --- HTML Scraping Rules ---
html_scrapers = {
    "Data.Gov.Uk": "div.dataset-item a",
    "Financial Times": "article div.o-teaser__heading",
    "The Times": "div.article",  # placeholder — actual site is paywalled
    "UKHSA": "li.collection a",
    "UN Data Portal": "div#datasets a",
    "WHO": "div.list-view a",  # generic dataset page
    "World Bank": "div.indicator-card",  # placeholder
}

for name, selector in html_scrapers.items():
    create_rule(name, "html", "selector", selector)

# --- API-based Sources ---
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

# --- Restricted/Paywalled Sources ---
restricted_sources = [
    "Daily Mail",
    "Financial Times",
    "The Times"
]

for name in restricted_sources:
    create_rule(name, "html", "restricted", "true")
    create_rule(name, "html", "strategy", "metadata_only")

print("✅ Rules created successfully.")

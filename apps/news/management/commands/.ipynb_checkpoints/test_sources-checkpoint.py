import requests
import feedparser
from django.core.management.base import BaseCommand
from apps.news.models import Source

from urllib.parse import urlparse

class Command(BaseCommand):
    help = "Test all Source entries and report accessibility and parsing issues."

    def handle(self, *args, **options):
        sources = Source.objects.filter(is_active=True)
        print(f"\nTesting {len(sources)} sources...\n")

        for source in sources:
            parser = source.parser_override or source.source_type
            headers = {}
            params = {}

            for rule in source.rules.all():
                if rule.rule_type == 'header':
                    headers[rule.key] = rule.value
                elif rule.rule_type == 'param':
                    params[rule.key] = rule.value
                elif rule.rule_type == 'auth':
                    headers['Authorization'] = rule.value
                elif rule.rule_type == 'user_agent':
                    headers['User-Agent'] = rule.value

            try:
                response = requests.get(source.url, headers=headers, params=params, timeout=10)
                content_type = response.headers.get('Content-Type', '').lower()
                status = response.status_code

                if status == 200:
                    if parser == 'rss':
                        parsed = feedparser.parse(response.text)
                        if parsed.entries:
                            self._success(source, parser, content_type)
                        else:
                            self._warn(source, "RSS format empty — check parser_override or feed structure")
                    elif parser in ['news', 'json']:
                        try:
                            data = response.json()
                            if isinstance(data, dict) or isinstance(data, list):
                                self._success(source, parser, content_type)
                            else:
                                self._warn(source, "Invalid JSON response — expected dict/list")
                        except Exception:
                            self._fail(source, "Expected JSON but could not parse — check content or parser_override")
                    elif parser == 'html':
                        if '<html' in response.text.lower():
                            self._success(source, parser, content_type)
                        else:
                            self._warn(source, "Expected HTML but got something else")
                    else:
                        self._warn(source, f"Unknown parser '{parser}' — add parser_override?")

                elif status == 403:
                    self._fail(source, "403 Forbidden — try adding User-Agent rule")
                elif status == 404:
                    self._fail(source, "404 Not Found — check source URL or endpoint")
                elif status >= 500:
                    self._fail(source, f"{status} Server Error")
                else:
                    self._fail(source, f"HTTP {status}")

            except requests.exceptions.Timeout:
                self._fail(source, "Timeout — source may be down or too slow")
            except requests.exceptions.ConnectionError:
                self._fail(source, "Connection Error — check URL or server")
            except Exception as e:
                self._fail(source, f"Unhandled error: {str(e)}")

    def _success(self, source, parser, content_type):
        print(f"✅ {source.name} ({parser}) — OK [{content_type}]")

    def _fail(self, source, reason):
        print(f"❌ {source.name} — {reason}")

    def _warn(self, source, reason):
        print(f"⚠️  {source.name} — {reason}")

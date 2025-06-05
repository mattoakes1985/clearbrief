from django.contrib import admin
from .models import Source
from .models import Article

admin.site.register(Article)

from .models import SourceRule

class SourceRuleInline(admin.TabularInline):
    model = SourceRule
    extra = 1  # how many blank forms to show
    verbose_name = "Scraping Rule"
    verbose_name_plural = "Scraping Rules"

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'source_type', 'is_active', 'trust_score', 'last_fetched')
    search_fields = ('name', 'url')
    list_filter = ('source_type', 'is_active')
    inlines = [SourceRuleInline]


@admin.register(SourceRule)
class SourceRuleAdmin(admin.ModelAdmin):
    list_display = ('source', 'rule_type', 'key', 'value')
    list_filter = ('rule_type',)
    search_fields = ('key', 'value')

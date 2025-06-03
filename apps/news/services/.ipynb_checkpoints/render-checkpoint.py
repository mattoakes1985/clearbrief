def generate_digest_card_json(article):
    summary = article.summary_structured or {}

    return {
        "headline": summary.get("headline", article.title),
        "signal": summary.get("signal"),
        "context": summary.get("context"),
        "action": summary.get("action"),
        "tags": summary.get("tags", []),
        "url": article.url,
        "published_at": article.published_at.isoformat(),
        "source_name": article.source.name,
    }

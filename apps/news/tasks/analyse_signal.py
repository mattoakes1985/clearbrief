# apps/news/tasks/analyse_signal.py

from celery import shared_task
from apps.news.models import Article, ArticleSignal
from apps.news.services.bias_signal import bias_signal_analysis

@shared_task
def analyse_missing_article_signals():
    articles = Article.objects.filter(signal_analysis__isnull=True)

    for article in articles:
        try:
            result = bias_signal_analysis(article)
            ArticleSignal.objects.create(
                article=article,
                bias_score=result["bias_score"],
                signal_score=result["signal_score"],
                sentiment=result["sentiment"],
                rhetoric_level=result["rhetoric_level"],
                llm_bias_label=llm_result.get("bias_label"),
                llm_bias_confidence=llm_result.get("bias_confidence"),
                llm_bias_rationale=llm_result.get("bias_rationale"),
            print(f"[✅] Analysed: {article.title[:60]}... LLM={llm_result.get('bias_label')}")
        except Exception as e:
            print(f"[❌] Failed for {article.title}: {e}")


import traceback
# apps/news/tasks/analyse_signal.py


@shared_task
def reanalyse_all_article_signals():
    articles = Article.objects.all()
    updated = 0

    for article in articles:
        try:
            result = bias_signal_analysis(article)

            print(f"\n[DEBUG] Title: {article.title[:60]}")
            print(f"[DEBUG] Bias: {result['bias_score']}, Signal: {result['signal_score']}, Rhetoric: {result['rhetoric_level']}")

            obj, created = ArticleSignal.objects.update_or_create(
                article=article,
                defaults={
                    "bias_score": bias_result["bias_score"],
                    "signal_score": bias_result["signal_score"],
                    "sentiment": bias_result["sentiment"],
                    "rhetoric_level": bias_result["rhetoric_level"],
                    "llm_bias_label": llm_result["bias_label"],
                    "llm_bias_confidence": llm_result["confidence"],
                    "llm_bias_rationale": llm_result["rationale"],
                }
            )
            print(f"[🔁] {article.title[:50]} - {'Created' if created else 'Updated'} | Bias: {result['bias_score']}")

            updated += 1

        except Exception as e:
            print(f"[❌] Failed for {article.title}: {e}")

    print(f"✅ Reanalysis complete. {updated} articles processed.")

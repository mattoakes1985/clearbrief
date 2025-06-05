import json
from openai import OpenAI
from django.conf import settings
from apps.news.models import Article

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def summarise_article(article: Article, tone="analytical") -> dict:
    prompt = (
        "You are an impartial intelligence analyst writing for a professional user. "
        "Your job is to (1) summarise the article for situational awareness and (2) assess any political bias in the article. Be very sensitive to any bias in tone, language, or context provided.\n\n"

        "Return the response in strict JSON format with these fields:\n"
        "{\n"
        '  "headline": "short headline",\n'
        '  "signal": "what is new or changed",\n'
        '  "context": "why this matters",\n'
        '  "action": "what should the user take note of",\n'
        '  "bias_label": "left|centre-left|centre|centre-right|right",\n'
        '  "bias_confidence": float (0.0 - 1.0),\n'
        '  "bias_rationale": "short explanation of the bias assessment"\n'
        "}\n\n"
        f"Article Title:\n{article.title}\n\n"
        f"Article Content:\n{article.content}"
    )

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except Exception as e:
        print("❌ Failed to parse LLM response:", e)
        print("RAW LLM Output:\n", content)
        return {
            "headline": None,
            "signal": None,
            "context": None,
            "action": None,
            "bias_label": "unknown",
            "bias_confidence": 0.0,
            "bias_rationale": "LLM parse error"
        }

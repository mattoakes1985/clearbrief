from openai import OpenAI
from apps.news.models import Article
from apps.news.services.tagging import tag_article  # 👈 import NLP tags
from django.conf import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)

def summarise_article(article: Article, tone="analytical") -> dict:
    prompt = (
        f"Summarise the following article like an intelligence analyst. "
        f"Use this structure:\n\n"
        f"Headline: <short headline>\n"
        f"Signal: <what is the newsworthy development>\n"
        f"Context: <relevant background or implications>\n"
        f"Action: <what should a user monitoring this consider or do>\n\n"
        f"Article:\n{article.content}\n"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You summarise and analyse news like a professional intelligence analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    result_text = response.choices[0].message.content.strip()

    # Parse the structured output
    lines = result_text.split("\n")
    structured = {"source_url": article.url, "published_at": article.published_at}

    for line in lines:
        if line.startswith("Headline:"):
            structured["headline"] = line.replace("Headline:", "").strip()
        elif line.startswith("Signal:"):
            structured["signal"] = line.replace("Signal:", "").strip()
        elif line.startswith("Context:"):
            structured["context"] = line.replace("Context:", "").strip()
        elif line.startswith("Action:"):
            structured["action"] = line.replace("Action:", "").strip()

    # 👇 Use NLP to extract tags and sentiment
    tags = tag_article(article)
    structured.update(tags)

    return structured

from openai import OpenAI
from apps.news.models import Article
from django.conf import settings
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def summarise_article(article: Article, tone="analytical") -> dict:
    prompt = (
        "You are an intelligence analyst writing for an informed professional user who needs personal situational awareness, not policy advice.\n\n"
        "Summarise the article using this format:\n"
        "- Headline: <short and clear headline>\n"
        "- Signal: <what is new or changed>\n"
        "- Context: <why this matters, including any relevant background>\n"
        "- Action: <What should the individual user take note of, watch for, or adjust their understanding based on this? Avoid generic advice about what governments or organisations should do.>\n\n"
        f"Article:\n{article.content}\n"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.3,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    text = response.choices[0].message.content

    print("\n=== RAW GPT OUTPUT ===")
    print(text)

    # Parse output manually
    def extract_section(name):
        try:
            for line in text.splitlines():
                clean_line = line.lstrip("- ").strip()
                if clean_line.lower().startswith(name.lower() + ":"):
                    return clean_line.split(":", 1)[1].strip()
            return None
        except Exception as e:
            print(f"Error extracting {name}: {e}")
            return None


    return {
        "headline": extract_section("Headline"),
        "signal": extract_section("Signal"),
        "context": extract_section("Context"),
        "action": extract_section("Action"),
        "published_at": article.published_at.isoformat(),
        "source_url": article.url
    }

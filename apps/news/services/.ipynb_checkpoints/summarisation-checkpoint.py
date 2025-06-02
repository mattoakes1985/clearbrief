import re
from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def summarise_article(article, tone="analytical"):
    prompt = f"""
You are an intelligence analyst. Summarise the following article in a concise, structured format using a {tone} tone.

Return exactly 4 fields:
HEADLINE: (succinct title)
SIGNAL: (what happened, 1 sentence)
CONTEXT: (why it matters, 1–2 sentences)
ACTION: (next step, e.g. "Watch", "Investigate", "Ignore", "Note", "Escalate")

Content:
\"\"\"
{article.content}
\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You summarise and analyse news like an intelligence analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    output = response.choices[0].message.content.strip()

    # Simple regex parser
    def extract_field(name):
        match = re.search(f"{name}:(.*?)(?=\n[A-Z]+:|$)", output, re.DOTALL)
        return match.group(1).strip() if match else ""

    return {
        "headline": extract_field("HEADLINE"),
        "signal": extract_field("SIGNAL"),
        "context": extract_field("CONTEXT"),
        "action": extract_field("ACTION"),
        "tags": article.tags,  # include NLP-generated tags here
        "source_url": article.url,
        "published_at": article.published_at.isoformat()
    }

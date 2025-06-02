from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def summarise_article(article, tone="analytical"):
    prompt = f"""
You are an intelligence analyst. Summarise the following article in a concise, structured format using a {tone} tone.

Return 4 labelled fields:
- HEADLINE (succinct title)
- SIGNAL (1-sentence: what happened)
- CONTEXT (1-2 sentences: why it matters)
- ACTION (suggested next step: Watch / Investigate / Escalate)

Article content:
\"\"\"
{article.content}
\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # ✅ Use the accessible model
        messages=[
            {"role": "system", "content": "You summarise and analyse news like an intelligence analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()

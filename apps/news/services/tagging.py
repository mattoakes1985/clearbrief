import spacy
from textblob import TextBlob

nlp = spacy.load("en_core_web_sm")

def tag_article(article):
    doc = nlp(article.content)

    entities = list(set([
        (ent.label_, ent.text) for ent in doc.ents
        if ent.label_ in ['ORG', 'PERSON', 'GPE', 'LOC']
    ]))

    sentiment_score = TextBlob(article.content).sentiment.polarity
    sentiment = (
        "positive" if sentiment_score > 0.2 else
        "negative" if sentiment_score < -0.2 else
        "neutral"
    )

    return {
        "entities": entities,
        "sentiment": sentiment
    }

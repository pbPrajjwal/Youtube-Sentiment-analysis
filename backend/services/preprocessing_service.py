import re

from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words("english"))

def clean_text(text: str):

    text = text.lower()

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"[^a-zA-Z ]", "", text)

    words = text.split()

    words = [
        w
        for w in words
        if w not in STOPWORDS
    ]

    return " ".join(words)
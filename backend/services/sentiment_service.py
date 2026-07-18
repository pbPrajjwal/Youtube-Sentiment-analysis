import os
import re
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "sentiment_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "models", "tfidf_vectorizer.pkl")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def clean_text(text: str) -> str:
    """Preprocess text before prediction."""

    text = str(text).lower()

    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"www\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def predict_sentiment(text: str) -> str:
    """Predict sentiment for a single comment."""

    cleaned_text = clean_text(text)

    features = vectorizer.transform([cleaned_text])

    prediction = model.predict(features)[0]

    return prediction


def analyze_comments(comments):
    if not comments:
        return []

    texts = [
        clean_text(item.get("comment", ""))
        for item in comments
    ]

    features = vectorizer.transform(texts)

    predictions = model.predict(features)

    results = []

    for item, sentiment in zip(comments, predictions):
        results.append({
            **item,
            "sentiment": sentiment
        })

    return results
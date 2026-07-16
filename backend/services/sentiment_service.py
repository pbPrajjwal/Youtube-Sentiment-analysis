from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

def predict(text):

    score = sia.polarity_scores(text)["compound"]

    if score >= 0.05:
        sentiment = "Positive"

    elif score <= -0.05:
        sentiment = "Negative"

    else:
        sentiment = "Neutral"

    return sentiment, score
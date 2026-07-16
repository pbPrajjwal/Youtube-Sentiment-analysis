from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

texts = [
    "This video is amazing!",
    "I absolutely loved this tutorial.",
    "This is okay.",
    "Worst tutorial ever."
]

for text in texts:
    result = sia.polarity_scores(text)

    print(f"\nText: {text}")
    print(f"Negative : {result['neg']}")
    print(f"Neutral  : {result['neu']}")
    print(f"Positive : {result['pos']}")
    print(f"Compound : {result['compound']}")
    
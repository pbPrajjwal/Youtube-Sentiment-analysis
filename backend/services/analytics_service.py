from collections import Counter


from collections import Counter


def generate_summary(results):

    sentiments = [x["sentiment"] for x in results]

    counter = Counter(sentiments)

    total = len(results)

    if total == 0:
        return {}

    return {

        "total_comments": total,

        "positive": counter["positive"],

        "negative": counter["negative"],

        "neutral": counter["neutral"],

        "positive_percentage":
            round(counter["positive"] * 100 / total, 2),

        "negative_percentage":
            round(counter["negative"] * 100 / total, 2),

        "neutral_percentage":
            round(counter["neutral"] * 100 / total, 2),
    }


def top_keywords(comments, top_n=20):
    words = []

    for comment in comments:
        words.extend(comment.lower().split())

    return Counter(words).most_common(top_n)
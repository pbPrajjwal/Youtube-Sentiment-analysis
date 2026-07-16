from collections import Counter

def top_keywords(comments):

    words = []

    for comment in comments:

        words.extend(comment.split())

    return Counter(words).most_common(20)
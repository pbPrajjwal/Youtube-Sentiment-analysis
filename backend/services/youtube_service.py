import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)


def fetch_video_details(video_id: str):

    request = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    )

    response = request.execute()

    if len(response["items"]) == 0:
        return None

    item = response["items"][0]

    snippet = item["snippet"]
    statistics = item["statistics"]

    return {
        "title": snippet["title"],
        "channel": snippet["channelTitle"],
        "published": snippet["publishedAt"],
        "thumbnail": snippet["thumbnails"]["high"]["url"],
        "views": int(statistics.get("viewCount", 0)),
        "likes": int(statistics.get("likeCount", 0)),
        "comments": int(statistics.get("commentCount", 0))
    }


def fetch_comments(video_id: str, limit: int = 200):

    comments = []

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    )

    while request and len(comments) < limit:

        response = request.execute()

        for item in response["items"]:

            snippet = item["snippet"]["topLevelComment"]["snippet"]

            comments.append({
                "author": snippet["authorDisplayName"],
                "comment": snippet["textDisplay"],
                "likes": snippet["likeCount"],
                "published": snippet["publishedAt"]
            })

            if len(comments) >= limit:
                break

        request = youtube.commentThreads().list_next(
            request,
            response
        )

    return comments
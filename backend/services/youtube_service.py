import os
import re

from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found in environment variables.")

youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)


def extract_video_id(url: str) -> str | None:
    """
    Extract the video ID from different YouTube URL formats.
    """

    patterns = [
        r"(?:v=)([A-Za-z0-9_-]{11})",
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:embed/)([A-Za-z0-9_-]{11})",
        r"(?:shorts/)([A-Za-z0-9_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def fetch_video_details(video_id: str):
    """
    Fetch metadata of a YouTube video.
    """

    try:
        request = youtube.videos().list(
            part="snippet,statistics",
            id=video_id,
        )

        response = request.execute()

        if not response["items"]:
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
            "comments": int(statistics.get("commentCount", 0)),
        }

    except HttpError as e:
        print(f"YouTube API Error: {e}")
        return None

    except Exception as e:
        print(f"Unexpected Error: {e}")
        return None


def fetch_comments(video_id: str, limit: int = 200):
    """
    Fetch top-level comments from a YouTube video.

    Returns:
        [
            {
                "author": "...",
                "comment": "...",
                "likes": 15,
                "published": "..."
            }
        ]
    """

    comments = []

    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            textFormat="plainText",
        )

        while request and len(comments) < limit:

            response = request.execute()

            for item in response["items"]:

                snippet = item["snippet"]["topLevelComment"]["snippet"]

                comments.append(
                    {
                        "author": snippet["authorDisplayName"],
                        "comment": snippet["textDisplay"],
                        "likes": snippet["likeCount"],
                        "published": snippet["publishedAt"],
                    }
                )

                if len(comments) >= limit:
                    break

            request = youtube.commentThreads().list_next(
                request,
                response,
            )

    except HttpError as e:
        print(f"YouTube API Error: {e}")

    except Exception as e:
        print(f"Unexpected Error: {e}")

    return comments
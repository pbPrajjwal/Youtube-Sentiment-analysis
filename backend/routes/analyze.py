from fastapi import APIRouter, HTTPException

from models.request import VideoRequest

from utils.youtube_utils import extract_video_id

from services.youtube_service import (
    fetch_comments,
    fetch_video_details
)

from services.preprocessing_service import clean_text

from services.sentiment_service import predict

from services.analytics_service import top_keywords

router = APIRouter()


@router.post("/analyze")
def analyze(request: VideoRequest):

    video_id = extract_video_id(request.url)

    if not video_id:

        raise HTTPException(
            status_code=400,
            detail="Invalid URL"
        )

    video = fetch_video_details(video_id)

    comments = fetch_comments(
        video_id,
        request.max_comments
    )

    summary = {

        "Positive": 0,
        "Negative": 0,
        "Neutral": 0

    }

    processed = []

    cleaned_comments = []

    for comment in comments:

        cleaned = clean_text(comment["comment"])

        sentiment, score = predict(cleaned)

        summary[sentiment] += 1

        cleaned_comments.append(cleaned)

        processed.append({

            **comment,

            "cleaned": cleaned,

            "sentiment": sentiment,

            "score": score

        })

    return {

        "video": video,

        "summary": summary,

        "keywords": top_keywords(cleaned_comments),

        "comments": processed

    }
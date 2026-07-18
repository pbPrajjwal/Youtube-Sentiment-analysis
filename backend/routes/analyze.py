from fastapi import APIRouter, HTTPException

from backend.models.schemas import AnalyzeRequest
from services.youtube_service import (
    extract_video_id,
    fetch_video_details,
    fetch_comments,
)
from services.sentiment_service import analyze_comments
from services.analytics_service import generate_summary

router = APIRouter()


@router.post("/analyze")
def analyze(request: AnalyzeRequest):
    video_id = extract_video_id(request.video_url)

    if not video_id:
        raise HTTPException(
            status_code=400,
            detail="Invalid YouTube URL"
        )

    video = fetch_video_details(video_id)

    if video is None:
        raise HTTPException(
            status_code=404,
            detail="Video not found"
        )

    comments = fetch_comments(video_id) or []

    analyzed_comments = analyze_comments(comments)

    summary = generate_summary(analyzed_comments)

    return {
        "video": video,
        "summary": summary,
        "comments": analyzed_comments
    }
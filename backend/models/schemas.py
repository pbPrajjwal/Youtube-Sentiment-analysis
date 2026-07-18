from pydantic import BaseModel

class VideoRequest(BaseModel):
    url: str
    max_comments: int = 200
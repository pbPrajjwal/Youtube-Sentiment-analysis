from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.analyze import router

app = FastAPI(
    title="YouTube Comment Analyzer API",
    description="Analyze YouTube comments using a TF-IDF + Linear SVM sentiment classifier.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    router,
    prefix="/api",
    tags=["Analysis"],
)


@app.get("/")
def home():
    return {
        "message": "YouTube Comment Analyzer API is running 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
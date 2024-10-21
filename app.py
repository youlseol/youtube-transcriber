from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_video_id(url: str) -> str:
    """Extract video ID from YouTube URL."""
    if "youtu.be" in url:
        return url.split("/")[-1]
    elif "youtube.com" in url:
        return url.split("v=")[1].split("&")[0]
    else:
        raise ValueError("Invalid YouTube URL")

def get_transcript(video_id: str) -> str:
    """Get transcript for a given video ID."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, languages=['en', 'de', 'fr', 'es', 'it', 'ja', 'ko', 'nl', 'pt', 'ru', 'zh-Hans', 'zh-Hant'])
        formatter = TextFormatter()
        return formatter.format_transcript(transcript)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/api/transcript")
async def get_youtube_transcript(request: Request):
    video_id = request.query_params.get("id")
    if not video_id:
        raise HTTPException(status_code=400, detail="No video ID provided")

    try:
        transcript = get_transcript(video_id)
        return {"transcript": transcript}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
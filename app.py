from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import os
import google.generativeai as genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#genai.configure(api_key=os.environ["GEMINI_API_KEY"])
genai.configure(api_key="AIzaSyCFvl1HowCM4E6uaW4pNJzps6w6TMLzH1I")

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="summarize in korean",
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
    
def extract_text_from_response(response: dict) -> str:
    """Extract text from the response object."""
    try:
        return response.candidates[0].content.parts[0].text
    except (KeyError, IndexError) as e:
        raise ValueError("Invalid response structure") from e

@app.get("/api/transcript")
async def get_youtube_transcript(request: Request):
    video_id = request.query_params.get("id")
    if not video_id:
        raise HTTPException(status_code=400, detail="No video ID provided")

    try:
        transcript = get_transcript(video_id)
        response = model.generate_content(transcript)
        return {"transcript": extract_text_from_response(response)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
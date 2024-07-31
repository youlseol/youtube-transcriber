from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

app = Flask(__name__)
CORS(app)


def get_video_id(url):
    """Extract video ID from YouTube URL."""
    if "youtu.be" in url:
        return url.split("/")[-1]
    elif "youtube.com" in url:
        return url.split("v=")[1].split("&")[0]
    else:
        raise ValueError("Invalid YouTube URL")


def get_transcript(video_id, language_code="ko"):
    """Get transcript for a given video ID."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, languages=[language_code]
        )
        formatter = TextFormatter()
        return formatter.format_transcript(transcript)
    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route("/api/transcript", methods=["POST"])
def get_youtube_transcript():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        video_id = get_video_id(url)
        transcript = get_transcript(video_id)
        return jsonify({"transcript": transcript})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)

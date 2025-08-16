import os
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import google.generativeai as genai
from flask_cors import CORS

# Load API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Flask app setup
app = Flask(__name__)
CORS(app)  # allow Chrome extension to access

# Prompt template for summarization
PROMPT = """
Summarize the YouTube transcript under three sections:
"Introduction": Brief intro to the topic
"Explanation": Key points and details
"Conclusion": Final thoughts or takeaways
"""

# Extract transcript from YouTube URL
def get_transcript(url):
    try:
        parsed = urlparse(url)
        video_id = None
        if "youtube.com" in parsed.netloc:
            video_id = parse_qs(parsed.query).get("v", [None])[0]
        elif "youtu.be" in parsed.netloc:
            video_id = parsed.path.lstrip("/")

        if not video_id:
            return None, "Invalid or missing video ID."

        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en", "hi"])
        text = " ".join([t["text"] for t in transcript])
        return text, None
    except TranscriptsDisabled:
        return None, "Transcripts are disabled for this video."
    except NoTranscriptFound:
        return None, "No transcript available for this video."
    except Exception as e:
        return None, str(e)

# Generate summary with Gemini
def summarize_text(transcript):
    try:
        model = genai.GenerativeModel("gemini-pro")
        result = model.generate_content(PROMPT + transcript)
        return result.text
    except Exception as e:
        return None

# API endpoint
@app.route("/summarize", methods=["GET"])
def summarize():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "No URL provided."}), 400

    transcript, err = get_transcript(url)
    if err:
        return jsonify({"error": err}), 400

    summary = summarize_text(transcript)
    if not summary:
        return jsonify({"error": "Failed to generate summary."}), 500

    return jsonify({"summary": summary})

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

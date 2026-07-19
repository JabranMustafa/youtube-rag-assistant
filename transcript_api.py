from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI()

@app.get("/transcript")
def get_transcript(video_id: str):
    try:
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id)

        transcript = [
            {
                "text": snippet.text,
                "start": snippet.start,
                "duration": snippet.duration,
            }
            for snippet in fetched_transcript
        ]

        return {
            "success": True,
            "video_id": video_id,
            "language": fetched_transcript.language,
            "language_code": fetched_transcript.language_code,
            "is_generated": fetched_transcript.is_generated,
            "transcript": transcript,
        }

    except Exception as e:
        return {
            "success": False,
            "video_id": video_id,
            "error": str(e),
        }
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs


def extract_video_id(url: str) -> str:
    """
    Extract video_id from a YouTube URL.
    Supports:
      https://www.youtube.com/watch?v=abc123
      https://youtu.be/abc123
    """
    parsed = urlparse(url)

    # Standard format: youtube.com/watch?v=xxx
    if "youtube.com" in parsed.netloc:
        params = parse_qs(parsed.query)
        video_id = params.get("v", [None])[0]
        if not video_id:
            raise ValueError("Could not find video_id in URL")
        return video_id

    # Short format: youtu.be/xxx
    if "youtu.be" in parsed.netloc:
        video_id = parsed.path.lstrip("/")
        if not video_id:
            raise ValueError("Could not find video_id in short URL")
        return video_id

    raise ValueError("Not a valid YouTube URL")


def get_transcript(url: str) -> str:
    """
    Main function: takes a YouTube URL, returns clean transcript text.
    """
    video_id = extract_video_id(url)
    api = YouTubeTranscriptApi()

    try:
        # Prefer English transcripts
        transcript_list = api.fetch(video_id, languages=["en"])
    except NoTranscriptFound:
        # Fall back to any available language
        transcript_list = api.fetch(video_id)
    except TranscriptsDisabled:
        raise RuntimeError("Transcripts are disabled for this video")

    # Join all transcript chunks into a single string
    full_text = " ".join(chunk.text for chunk in transcript_list)
    return full_text


# Local testing
if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=aircAruvnKk"  # 3Blue1Brown neural networks
    text = get_transcript(test_url)
    print(f"Word count: {len(text.split())} words")
    print(f"First 200 chars: {text[:200]}")
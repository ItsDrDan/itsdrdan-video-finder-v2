#!/usr/bin/env python3
"""
Build videos.json for the ItsDrDan Video Finder without a YouTube Data API key.

Requirements:
    pip install -U yt-dlp

Run from the repository root:
    python scripts/build_videos.py

The script reads public video data from:
    https://www.youtube.com/@itsdrdan/videos

It also checks captions/VIDEO_ID.vtt and includes only the caption files
that actually exist in your repository.
"""

from pathlib import Path
from datetime import datetime, timezone
import json
import subprocess
import sys

CHANNEL_URL = "https://www.youtube.com/@itsdrdan/videos"
ROOT = Path(__file__).resolve().parents[1]
CAPTIONS = ROOT / "captions"
OUTPUT = ROOT / "videos.json"

def run_ytdlp():
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--flat-playlist",
        "--dump-single-json",
        "--no-warnings",
        CHANNEL_URL,
    ]
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as exc:
        print(exc.stdout)
        print(exc.stderr, file=sys.stderr)
        raise SystemExit("yt-dlp could not read the public channel.")
    return json.loads(completed.stdout)

def thumbnail(video_id):
    return f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"

def main():
    data = run_ytdlp()
    entries = data.get("entries") or []
    videos = []

    for order, item in enumerate(entries):
        if not item:
            continue
        vid = str(item.get("id") or "").strip()
        if not vid:
            continue

        caption_path = CAPTIONS / f"{vid}.vtt"
        videos.append({
            "id": vid,
            "title": item.get("title") or f"YouTube video {vid}",
            "url": f"https://www.youtube.com/watch?v={vid}",
            "thumbnail": thumbnail(vid),
            "order": order,
            "description": item.get("description") or "",
            "duration": "",
            "durationSeconds": 0,
            "tags": [],
            "course": "",
            "caption": f"./captions/{vid}.vtt" if caption_path.exists() else None,
        })

    payload = {
        "channel": "https://www.youtube.com/@itsdrdan",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "videoCount": len(videos),
        "videos": videos,
    }

    OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(videos)} videos to {OUTPUT}")

if __name__ == "__main__":
    main()

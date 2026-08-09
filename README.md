# ItsDrDan Chemistry Video Finder

A kawaii GitHub Pages search engine for the public ItsDrDan YouTube channel.

## What this version does

- Uses **no YouTube Data API key in the website**
- Plays videos with the normal YouTube iframe player
- Searches a local `videos.json` file
- Searches your own `.vtt` transcript files
- Jumps directly to matching transcript timestamps
- Includes chemistry synonym expansion
- Includes course filters and a local Study Shelf

## Repository layout

```text
/
├── index.html
├── videos.json
├── captions/
│   ├── VIDEO_ID.vtt
│   └── ...
├── scripts/
│   └── build_videos.py
└── .github/
    └── workflows/
        └── update-videos.yml
```

## First setup

1. Upload this entire folder to a GitHub repository.
2. In GitHub, open **Actions**.
3. Select **Update YouTube video library**.
4. Choose **Run workflow**.
5. The workflow uses `yt-dlp` to read the public video list from:
   `https://www.youtube.com/@itsdrdan/videos`
6. It writes the public video IDs and titles to `videos.json`.
7. Enable GitHub Pages for the repository.

No YouTube Data API key is stored in `index.html`.

## Adding searchable captions

Place WebVTT files inside `captions/`.

The filename must be the YouTube video ID:

```text
captions/59yqaBoKWss.vtt
```

Then run the **Update YouTube video library** Action again. The builder detects which
video IDs have VTT files and marks those transcripts as searchable.

## Updating the library

The included workflow:
- can be run manually,
- runs when caption files or the builder change,
- and checks the public channel weekly.

If GitHub-hosted `yt-dlp` is ever blocked by YouTube, you can update locally:

```bash
python -m pip install -U yt-dlp
python scripts/build_videos.py
```

Then commit the updated `videos.json`.

## GitHub Pages

For a normal project repository:

**Settings → Pages → Deploy from a branch → main → / (root)**

The site will then use the files in the repository directly.

---
name: youtube-transcript
description: Fetch transcripts from YouTube videos using yt-dlp. Use when needing video transcripts, summaries, or content extraction from YouTube.
---

# YouTube Transcript

Download and process transcripts from YouTube videos.

## Prerequisites

```bash
# Check if yt-dlp is installed
which yt-dlp || pip3 install yt-dlp
```

## Workflow

### 1. List Available Subtitles (ALWAYS do this first)

```bash
yt-dlp --list-subs "VIDEO_URL"
```

### 2. Download Transcript

**Manual subtitles (best quality):**
```bash
yt-dlp --write-sub --sub-lang en --skip-download -o "transcript" "VIDEO_URL"
```

**Auto-generated subtitles:**
```bash
yt-dlp --write-auto-sub --sub-lang en --skip-download -o "transcript" "VIDEO_URL"
```

### 3. Clean VTT Content

Auto-generated VTT files contain duplicate lines. Clean with:

```python
import re

def clean_vtt(filepath):
    with open(filepath) as f:
        content = f.read()
    # Remove VTT header and timestamps
    lines = content.split('\n')
    seen = set()
    clean = []
    for line in lines:
        if '-->' in line or line.startswith('WEBVTT') or line.strip() == '':
            continue
        text = re.sub(r'<[^>]+>', '', line).strip()
        if text and text not in seen:
            seen.add(text)
            clean.append(text)
    return ' '.join(clean)
```

### 4. Whisper Fallback

If no subtitles available (ask user first — downloads audio):
```bash
yt-dlp -x --audio-format mp3 -o "audio.%(ext)s" "VIDEO_URL"
whisper audio.mp3 --model base --output_format txt
```

## Use Cases

- Morning briefing Moonshot podcast summaries
- Research video content for notes
- Extract key quotes and timestamps
- Create written summaries of talks/tutorials


# Bazarr Ultimate Subtitle Generation Guide

This guide outlines how to set up **Bazarr** for automatic, perfectly synced subtitle generation using **Whisper-ASR** and **Aeneas**. This solution is ideal for users who want precise subtitle synchronization without manually searching for synced subtitles. Note that this process works best for English source videos and subtitles.

---

## Overview

This guide is perfect for users who:
- Want perfectly synced subtitles for their media.
- Don’t mind minor literal translation inaccuracies.
- Prefer an automated pipeline for subtitle generation.

The setup involves leveraging **Whisper-ASR** for subtitle creation and **Aeneas** for fine-tuned subtitle synchronization.

---

## Prerequisites

Before you begin, ensure you have the following:
1. **Bazarr** installed and configured with ARR tools like Sonarr and Radarr.
2. Basic familiarity with ARR workflows.
3. A system capable of running **Whisper-ASR** (preferably with GPU support for faster processing).

---

## Steps to Set Up

### 1. Enable Custom Post-Processing

In Bazarr, add the following custom post-processing command in your configuration:

```bash
/config/postproces.sh "{{episode}}" "{{subtitles}}" "{{provider}}"
```

### 2. Set Language Profile

- The source language for this setup is **English**.
- Non-English source languages are not currently supported.

### 3. Integrate Whisper Provider with Bazarr

Modify the `postproces.sh` script in your Bazarr config directory. The script should handle the following:
- Identify if the subtitle provider is **Whisper**.
- Run post-processing only for Whisper; otherwise, exit without making changes.

---

## How It Works

### Process Flow
1. The **Flask app** interacts with the video file and subtitle file.
2. It converts the video to `.mp3` format and syncs subtitles using **Aeneas**.
3. After processing:
   - The original subtitle is replaced with the synced version.
   - The intermediate `.mp3` file is deleted.
4. The resulting English subtitle file is perfectly synced with the video.

You can then use Bazarr’s **translate** option to convert these synced subtitles into other languages.

---

## Implementation Details

- The Flask app communicates with **Aeneas** running on `aeneas:5000`.
- The script sends the following parameters:
  - `series_path`: Path to the video file.
  - `subtitle_path`: Path to the subtitle file.
  - `provider`: The subtitle provider.

### Docker and GPU Support
- If using Whisper-ASR, GPU support is highly recommended for efficiency.
- Modify your Docker Compose file to specify the desired Whisper model or version.

---

## Personal Pipeline Example

1. **Input**: English video source.
2. **Processing**:
   - Generate English subtitles using **Whisper-ASR**.
   - Sync subtitles perfectly with the video using **Aeneas**.
3. **Output**:
   - Use Bazarr’s mass-translate feature to generate subtitles in other languages.

---

## Notes & Tips

- This solution is tailored for **English source to English subtitle** workflows (for now).
- GPU support for Whisper is crucial for faster processing.
- Tutorials for configuring Whisper with Docker Compose can be found on the Bazarr Wiki.

---

## Why Use This Solution?

This project was born out of the frustration of finding high-quality, perfectly synced subtitles. With this setup, you can ensure a seamless experience for all your media.

Happy subtitle syncing!
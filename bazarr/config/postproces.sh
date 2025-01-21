#!/bin/bash

episode="$1"
subtitles="$2"
provider="$3"

# Check if the subtitle was fetched from the specific provider (e.g., "whisperai")
if [[ "$provider" == "whisperai" ]]; then
    echo "Post-processing subtitles from whisperai"

    curl -s -X POST http://aeneas:5000/process \
    -H "Content-Type: application/json" \
    -d "{\"video_file_path\":\"$episode\",\"subtitle_file_path\":\"$subtitles\"}"

else
    echo "Skipping post-processing. Subtitle not fetched from whisperai"
fi

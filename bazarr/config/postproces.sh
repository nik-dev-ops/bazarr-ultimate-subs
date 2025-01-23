#!/bin/bash

episode="$1"
subtitles="$2"
provider="$3"

# Check if the provider is NOT "embeddedsubtitles"
if [[ "$provider" != "embeddedsubtitles" ]]; then
    echo "Post-processing subtitles (provider is not embeddedsubtitles)"

    curl -s -X POST http://aeneas:5000/process \
    -H "Content-Type: application/json" \
    -d "{\"video_file_path\":\"$episode\",\"subtitle_file_path\":\"$subtitles\"}"

else
    echo "Skipping post-processing. Subtitle provider is embeddedsubtitles"
fi
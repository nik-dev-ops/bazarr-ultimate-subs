import sys
import os
import subprocess
import re

def clean_srt(subtitle_path):
    """
    Cleans SRT file by removing redundant subtitle entries and keeping only complete ones.
    Uses the second timestamp occurrence for each subtitle block.
    """
    try:
        with open(subtitle_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()

        # Split into subtitle blocks
        blocks = content.split('\n\n')
        cleaned_blocks = []
        subtitle_count = 1

        # Regular expressions for matching
        timestamp_pattern = re.compile(r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$')
        number_pattern = re.compile(r'^\d+$')

        for block in blocks:
            lines = block.split('\n')
            cleaned_lines = []
            text_lines = []
            timestamps = []

            for line in lines:
                line = line.strip()
                if timestamp_pattern.match(line):
                    timestamps.append(line)
                elif number_pattern.match(line):
                    if not cleaned_lines:  # Only add number if it's the first line
                        cleaned_lines.append(str(subtitle_count))
                else:
                    text_lines.append(line)

            # Use the second timestamp if available
            if len(timestamps) >= 2:
                cleaned_lines.append(timestamps[1])
            elif timestamps:  # Fallback to first timestamp if only one exists
                cleaned_lines.append(timestamps[0])

            if timestamps and text_lines:  # Only keep blocks with both timestamp and text
                cleaned_lines.extend(text_lines)
                cleaned_blocks.append('\n'.join(cleaned_lines))
                subtitle_count += 1

        # Write the cleaned content
        with open(subtitle_path, 'w', encoding='utf-8') as file:
            file.write('\n\n'.join(cleaned_blocks))
            file.write('\n')  # Add final newline

        print(f"Cleaned subtitle saved to {subtitle_path}")
    except Exception as e:
        print(f"Error during subtitle cleaning: {e}")
        sys.exit(1)

def process_subtitle(video_file_path, subtitle_path):
    if not os.path.isfile(subtitle_path):
        print(f"Subtitle file not found: {subtitle_path}")
        sys.exit(1)
    if not os.path.isfile(video_file_path):
        print(f"Video file not found: {video_file_path}")
        sys.exit(1)

    audio_file_path = f"{video_file_path.rsplit('.', 1)[0]}.mp3"
    print(f"Extracting audio from {video_file_path} to {audio_file_path}")
    
    try:
        subprocess.run([
            "ffmpeg", "-i", video_file_path, "-vn", "-acodec", "libmp3lame",
            "-ab", "192k", "-ar", "44100", "-y", audio_file_path
        ], check=True)
        print(f"Audio file created at: {audio_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during audio extraction: {e}")
        sys.exit(1)

    output_subtitle_path = subtitle_path.replace(".srt", "_aligned.srt")
    try:
        command = [
            "python", "-m", "aeneas.tools.execute_task",
            audio_file_path, subtitle_path,
            "task_language=eng|os_task_file_format=srt|is_text_type=subtitles",
            output_subtitle_path
        ]
        subprocess.run(command, check=True)
        print(f"Subtitle timings corrected and saved: {output_subtitle_path}")
        os.rename(output_subtitle_path, subtitle_path)
        print(f"Original subtitle file replaced with aligned version: {subtitle_path}")
        # Clean the subtitle file (remove blocks with no text)
        clean_srt(subtitle_path)
    except subprocess.CalledProcessError as e:
        print(f"Error during subtitle processing: {e}")
        sys.exit(1)
    finally:
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)
            print(f"Temporary audio file removed: {audio_file_path}")

    print("Processing completed successfully.")
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_subtitles.py <path_to_video_file> <path_to_subtitle_file>")
        sys.exit(1)
    
    video_file_path = sys.argv[1]
    subtitle_path = sys.argv[2]
    process_subtitle(video_file_path, subtitle_path)
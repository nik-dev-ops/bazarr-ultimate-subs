import sys
import os
import subprocess

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

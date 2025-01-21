# bazarr-ultimate-subs
Bazarr ultimate subtitle generation with whisper-asr and aeneas for perfect subtitle time matching

First step:
Enable Custom Post-Processing and add this to command
/config/postproces.sh "{{episode}}" "{{subtitles}}" "{{provider}}"

Second step:
If you already didn't specify language profile. Source language must be english as that is how this version of script is made, it can be different languages but i have not implemented variable to use different languages.

I've modified in config directory added script postproces.sh which is added as postproces for all subtitles that whisper generated subtitles for, it checks for provider if whisper it runs postprocessing otherwise exits.

Script connects to flask app aeneas:5000 to send series_path, subtitle_path and provider to aeneas program that does perfect word by word matching of subtitles it has been taken from this project https://github.com/readbeyond/aeneas

After what flask app takes video file, converts it to .mp3 and runs subtitle sync (ye lets not get into detail), after what it replaces original subtitle and removes .mp3 file generated.

Resulting english subtitle file is 100% in sync with video, after what you can use translate option from bazarr to translate perfectly synced subtitles to any other language.




Disclaimer:
- it only works for english source to english subtitle (for now)
- for whisper GPU is recommended, my docker compose uses gpu you will have to modify it your self if you want different model or version of whisper, there are tutorials on bazarr wiki
- i've created this project only because i'm super upset looking for good subtitles with fine sync of subtitles, so i generate them myself


My personal pipeline:

English video source > whisper > english-subtitle > postproces-for-perfect-sync > bazarr-mass-translate-to-desired-language
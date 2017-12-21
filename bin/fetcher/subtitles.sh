#!/usr/bin/env bash
# wget https://yt-dl.org/downloads/latest/youtube-dl
# chmod +x youtube-dl
# mkdir subtitles
parallel "./youtube-dl --write-sub --all-subs --skip-download -o \"subtitles/%(id)s/%(id)s\" https://www.youtube.com/watch?v={}" ::: $(cat ../../res/uploaded_videos.txt)
mv subtitles ../../res/
rm youtube-dl

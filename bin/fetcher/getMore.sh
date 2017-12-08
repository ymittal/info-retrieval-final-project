#!/usr/bin/env bash
parallel "./youtube-dl --write-info-json --skip-download -o \"subtitles_meta/%(id)s/%(id)s\" https://www.youtube.com/watch?v={}" ::: $(cat ../../res/uploaded_videos.txt)

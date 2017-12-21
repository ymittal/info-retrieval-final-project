#!/usr/bin/env bash
parallel "./youtube-dl --write-info-json --write-sub --all-subs --skip-download -o \"subtitles_meta/%(id)s/%(id)s\" https://www.youtube.com/watch?v={}" ::: $(cat res/tedEd_vid_list.txt)

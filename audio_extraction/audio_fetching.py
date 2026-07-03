#downloading a recording of ietf from youtube

#external libraries used for the file:
#[1]yt-dlp
#author:yt-dlp project
#URL : https://github.com/yt-dlp/yt-dlp

#[2]"FFmpeg"
#author:FFmpeg project
#URL : https://ffmpeg.org/

import argparse
import os
import subprocess

def main():
    parser=argparse.ArgumentParser(description="Download a recording of IETF from YouTube")
    parser.add_argument("url",help="URL of the YouTube video to download")
    parser.add_argument("-name",default="session",help="name for the files")
    args=parser.parse_args()
    
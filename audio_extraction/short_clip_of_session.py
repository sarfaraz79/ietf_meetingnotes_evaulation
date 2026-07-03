#External Libraries used in this file
#[1] ffmpeg
#url: https://ffmpeg.org/

import argparse
import subprocess
import os

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--input",help="Path to the input audio file")
    parser.add_argument("--output",help="where to save the clip")
    parser.add_argument("--start",help="Start time of the clip in seconds")
    parser.add_argument("--length",default="00:10:00",help="Length of the clip in seconds")
    args=parser.parse_args()
    
    
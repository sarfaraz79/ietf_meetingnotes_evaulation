#downloading a recording of ietf from youtube

#external libraries used for the file:
#[1]yt-dlp
#author:yt-dlp project
#URL : https://github.com/yt-dlp/yt-dlp

#[2]FFmpeg
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
    os.makedirs("audio",exist_ok=True)#will create an audio directory if it does not exist
    raw_audio=f"audio/{args.name}.m4a"
    wav_output=f"audio/{args.name}.wav"
    download=["yt-dlp", "-f", "bestaudio", "-o", raw_audio, args.url]#this will download only the audio track
    subprocess.run(download,check=True)
    convert=["ffmpeg", "-i", raw_audio, "-ar","16000","-ac","1","-c:a", "pcm_s16le", wav_output]#this will convert the audio to wav format along with the 16Khz format Whisper needs
    subprocess.run(convert,check=True)
    print(f"Downloaded and converted audio saved as {wav_output}")
    
if __name__=="__main__":
    main()
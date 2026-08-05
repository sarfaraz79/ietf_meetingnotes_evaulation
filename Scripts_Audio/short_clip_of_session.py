#External Libraries used in this file
#[1] ffmpeg
#url: https://ffmpeg.org/

import argparse
import subprocess
import os

def main():
    parser=argparse.ArgumentParser()#this will take the audio file form the command line or batch jobs
    parser.add_argument("--input",help="Path to the input audio file")
    parser.add_argument("--output",help="where to save the clip")
    parser.add_argument("--start",help="Start time of the clip in seconds")
    parser.add_argument("--length",default="00:10:00",help="Length of the clip")
    args=parser.parse_args()
    output_folder=os.path.dirname(args.output)#this will get the directory name of the output file
    if output_folder:
        os.makedirs(output_folder,exist_ok=True)
        
    clip_command=["ffmpeg","-i",args.input,"-ss",args.start,"-t",args.length,"-ar","16000","-ac","1","-c:a","pcm_s16le",args.output]#forcing output to match whispers requirements
    subprocess.run(clip_command,check=True)
if __name__=="__main__":
    main()

    
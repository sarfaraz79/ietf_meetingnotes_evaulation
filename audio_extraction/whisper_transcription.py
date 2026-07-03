#External librabies used in this file
#[1] openai-whisper
#url: https://github.com/openai/whisper

import argparse
import os
import whisper

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--input",help="Path to the input audio file")
    parser.add_argument("--model",default="base",help="Model to use for transcription")
    parser.add_argument("--output",default="transcription",help="Path to save the transcription")
    args=parser.parse_args()
    os.makedirs(args.outdir,exist_ok=True)
    model=whisper.load_model(args.model)
    result=model.transcribe(args.input)
    base_name=os.path.basename(args.input)
    output_file=os.path.join(args.output,f"{base_name}_whisper.txt")
    with open(output_file,"w") as f:
        f.write(result["text"].strip())
    print(f"Transcription saved to {output_file}")
if __name__=="__main__":
    main()
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
    parser.add_argument("--glossary",default=None,help="Path to the glossary file")
    args=parser.parse_args()
    os.makedirs(args.output,exist_ok=True)
    model=whisper.load_model(args.model)
    #glossary is given to ill turn it into a string and pass it to whisper
    prompt= None
    if args.glossary:
        with open(args.glossary) as f:
            term=[line.strip() for line in f if line.strip() and not line.startswith("#")]
            prompt=" ".join(term)
            print(f"Using glossary: {prompt}")
            
    result=model.transcribe(args.input,initial_prompt=prompt)
    base_name=os.path.basename(args.input)
    output_file=os.path.join(args.output,f"{base_name}_whisper.txt")
    with open(output_file,"w") as f:
        f.write(result["text"].strip())
    print(f"Transcription saved to {output_file}")
    debugfile=os.path.join(args.output,f"{base_name}_whisper_debug.txt")
    with open(debugfile,"w") as d:
        for seg in result["segments"]:
            d.write(
                f"[{seg['start']:.1f}-{seg['end']:.1f})]"
                f"avg_logprob={seg.get('avg_logprob',0):.3f}"
                f"no_speech_prob={seg.get('no_speech_prob',0):.3f}"
                f"compression_ratio={seg.get('compression_ratio',0):.3f}"
                f"text:{seg['text'].strip()}\n"
            )
    print("Debug saved to the debug file")
if __name__=="__main__":
    main()

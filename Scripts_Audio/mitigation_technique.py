import argparse
import os
import whisper
 
def main():
    parser = argparse.ArgumentParser()#inpute from command line or batch jobs
    parser.add_argument("--input", help="Path to the input audio file")
    parser.add_argument("--model", default="base", help="Model to use for transcription")
    parser.add_argument("--output", default="mitigation_results", help="Path to save the transcription")
    parser.add_argument("--language", default=None, help="Language of the audio file")
    parser.add_argument("--glossary", default=None, help="Path to the glossary file")
 
    parser.add_argument("--no_condition_on_previous_text", action="store_true",help="Disable conditioning decoding on the previous segments text")
    parser.add_argument("--no_speech_threshold", type=float, default=0.6,help="Whisper's own no-speech probability threshold")
    parser.add_argument("--compression_ratio_threshold", type=float, default=2.4,help="Whisper's own compression ratio threshold")
    parser.add_argument("--logprob_threshold", type=float, default=-1.0,help="Whisper's own average log-probability threshold")
 
    # short label to  identify which technique this run is testing
    parser.add_argument("--technique_label", default="default",
                         help="Short label for this run, e.g. 'no_prev_text', "
                              "'threshold_08', used in the output filename")
 
    args = parser.parse_args()
    os.makedirs(args.output, exist_ok=True)
    model = whisper.load_model(args.model)#loads the model
 
    prompt = None
    if args.glossary:#feeding the glossary to whisper before it begins
        with open(args.glossary) as f:
            term = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            prompt = " ".join(term)
            print(f"Using glossary: {prompt}")
 
    result = model.transcribe(
        args.input,
        initial_prompt=prompt,
        language=args.language,
        condition_on_previous_text=not args.no_condition_on_previous_text,
        no_speech_threshold=args.no_speech_threshold,
        compression_ratio_threshold=args.compression_ratio_threshold,
        logprob_threshold=args.logprob_threshold,
    )
 
    base_name =os.path.basename(args.input)
    tag =args.technique_label
 
    output_file =os.path.join(args.output,f"{base_name}_{tag}_whisper.txt")#creating a debug file
    with open(output_file, "w") as f:
        f.write(result["text"].strip())
    print(f"Transcription saved to {output_file}")
 
    debugfile = os.path.join(args.output,f"{base_name}_{tag}_whisper_debug.txt")
    with open(debugfile,"w") as d:
        for seg in result["segments"]:
            d.write(
                f"[{seg['start']:.1f}-{seg['end']:.1f})]"
                f"avg_logprob={seg.get('avg_logprob',0):.3f}"
                f"no_speech_prob={seg.get('no_speech_prob',0):.3f}"
                f"compression_ratio={seg.get('compression_ratio',0):.3f}"
                f"text:{seg['text'].strip()}\n"
            )
    #log the settings used for this run so can trace back which
    settings_file = os.path.join(args.output,f"{base_name}_{tag}_settings.txt")
    with open(settings_file,"w") as s:
        s.write(f"technique_label={args.technique_label}\n")
        s.write(f"model={args.model}\n")
        s.write(f"language={args.language}\n")
        s.write(f"condition_on_previous_text={not args.no_condition_on_previous_text}\n")
        s.write(f"no_speech_threshold={args.no_speech_threshold}\n")
        s.write(f"compression_ratio_threshold={args.compression_ratio_threshold}\n")
        s.write(f"logprob_threshold={args.logprob_threshold}\n")
    print(f"Settings saved to {settings_file}")
if __name__ == "__main__":
    main()
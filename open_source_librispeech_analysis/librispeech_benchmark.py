import argparse
import csv
import whisper 
import jiwer

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model",default="base")
    p.add_argument("--refs",default="librispeech_test/references.csv")
    args = p.parse_args()
    model = whisper.load_model(args.model)#loading the whisper model
    refs, hyps = [], []#this will store the manual and automatic transcript
    with open(args.refs) as f:#read csv and transcribe the clip
        for row in csv.DictReader(f):
            result = model.transcribe(row["path"], language="en", temperature=0, beam_size=5, best_of=5)
            refs.append(row["sentence"])
            hyps.append(result["text"])

    transform = jiwer.Compose([jiwer.ToLowerCase(),jiwer.RemovePunctuation(),jiwer.RemoveMultipleSpaces(),jiwer.Strip(),jiwer.ReduceToListOfListOfWords(),])#text cleaning before jiwer
    wer = jiwer.wer(refs, hyps, reference_transform=transform, hypothesis_transform=transform)
    print(f"model{args.model}, clips{len(refs)}, wer {wer:.4f} ({wer*100:.2f}%)")

if __name__ == "__main__":
    main()

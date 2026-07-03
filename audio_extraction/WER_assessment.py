#[1]jjiwer
#Author: Nik Vaessen
#URL: https://github.com/jitsi/jiwer

import argparse
import jiwer

def load_text(file_path):
    with open(file_path, "r") as f:
        return f.read().strip()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", help="Path to the reference text file")
    parser.add_argument("--hypothesis", help="Path to the hypothesis text file")
    parser.add_argument("--output", default="wer_output.txt", help="Path to the output file")
    args = parser.parse_args()
    reference = load_text(args.reference)
    hypothesis = load_text(args.hypothesis)
    
    transformation = jiwer.Compose([jiwer.ToLowerCase(), jiwer.RemovePunctuation(), jiwer.RemoveMultipleSpaces(), jiwer.Strip(),jiwer.ReduceToListOfListOfWords()])
    result = jiwer.wer(reference, hypothesis, reference_transform=transformation, hypothesis_transform=transformation)
    wer=result.wer
    
    reference_words=result.references[0]
    hypothesis_words=result.hypotheses[0]
    substitutions=[]
    deletions=[]
    insertions=[]
    for chuck in result.alignments[0]:
        for i in range(chunk.ref_end_idx-chuck.ref_start_idx):
            r=reference_words[chuck.ref_start_idx+i]
            h=hypothesis_words[chuck.hyp_start_idx+i]
            substitutions.append(f"{r}-> {h}")
    
    
    print(f"reference: {reference}")
    print(f"hypothesis:{hypothesis}")
    print(f"Word Error Rate:{wer:.3f}({wer*100:.2f}%)")

if __name__ == "__main__":
    main()
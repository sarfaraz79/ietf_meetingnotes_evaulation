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
    result = jiwer.process_words(reference, hypothesis, reference_transform=transformation, hypothesis_transform=transformation)
    wer= result.wer
    
    reference_words=result.references[0]
    hypothesis_words=result.hypotheses[0]
    substitutions=[]
    deletions=[]
    insertions=[]
    for chunk in result.alignments[0]:
        if chunk.type == "substitute":
            for i in range(chunk.ref_end_idx - chunk.ref_start_idx):
                r = reference_words[chunk.ref_start_idx + i]
                h = hypothesis_words[chunk.hyp_start_idx + i]
                substitutions.append(f"{r}-> {h}")
        elif chunk.type == "delete":
            for i in range(chunk.ref_start_idx ,chunk.ref_end_idx):
                #r = reference_words[chunk.ref_start_idx + i]
                deletions.append(reference_words[i])
        elif chunk.type == "insert":
            for i in range(chunk.hyp_start_idx,chunk.hyp_end_idx):
                insertions.append(hypothesis_words[i])
        
    with open(args.output, "w") as f:
        f.write(f"reference: {reference}\n")
        f.write(f"hypothesis: {hypothesis}\n")
        f.write(f"Word Error Rate: {wer:.3f} ({wer*100:.2f}%)\n")
        f.write(f"Substitutions: {substitutions}\n")
        f.write(f"Deletions: {deletions}\n")
        f.write(f"Insertions: {insertions}\n")

    print(f"Word Error Rate:{wer:.3f}({wer*100:.2f}%)")

if __name__ == "__main__":
    main()
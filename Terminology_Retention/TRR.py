#here we will measure how many domain specific words whisper has kept
 
import argparse
import re 

def load_text(file_path):
    with open(file_path) as f:
        return f.read().lower()
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--glossary", required=True, help="Path to the glossary file")
    parser.add_argument("--reference", required=True, help="Path to the reference file")
    parser.add_argument("--hypothesis", required=True, help="Path to the whisper file")
    parser.add_argument("--output", default="TRR_output.txt", help="Path to save the result")
    args=parser.parse_args()
    glossary = load_glossary(args.glossary)
    reference= load_text(args.reference)
    hypothesis = load_text(args.hypothesis)
    total_spoken=0
    total_kept=0
    per_term=[]
    for term in glossary:
        in_ref=count_occurrences(reference,term)
        in_hypo=count_occurrences(hypothesis, term)
        if in_ref==0:
            continue
        kept=min(in_hypo, in_ref)
        total_spoken += in_ref
        total_kept += kept
        per_term.append((term, kept, in_ref))
        
    trr=total_kept/total_spoken if total_spoken>0 else 0
    with open(args.output, "w") as f:
        f.write(f"reference:{args.reference}\n")
        f.write(f"hypothesis:{args.hypothesis}\n)")
        f.write(f"TRR:{trr}\n)")
        f.write(f"total_spoken:{total_spoken},preserved:{total_kept}\n)")
        for term,in_ref,in_hypo in per_term:
            f.write(f"{term}: {in_hypo}/{in_ref}\n")
    print(f"TRR:{trr}, total_spoken:{total_spoken}, preserved:{total_kept}")
        
def load_glossary(file_path):
    terms=[]
    with open(file_path) as f:
        for line in f:
            term=line.strip().lower()
            if term and not term.startswith("#"):
                terms.append(term)
    return terms

def count_occurrences(text, term):
    pattern = r'\b' + re.escape(term) + r'\b'
    return len(re.findall(pattern, text))
        
if __name__ == "__main__":
    main()
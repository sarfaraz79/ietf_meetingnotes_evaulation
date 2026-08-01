import re
import argparse

def load_glossary(file_path):
    terms=set()
    with open(file_path) as f:
        for line in f:
            term = line.strip().lower()
            if term and not term.startswith("#"):
                terms.add(term)
    return terms

def computing_density(reference_path,glossary_path):
    with open(reference_path) as f:
        text=f.read().lower()
        
    all_words=re.findall(r"[a-zA-Z']+",text)
    word_count_total=len(all_words)
    glossary_terms=load_glossary(glossary_path)
    technical_word_count= 0
    
    for term in glossary_terms:
        technical_word_count+=len(re.findall(r"\b"+re.escape(term)+r"\b",text))
    density=(technical_word_count/word_count_total)*100 if word_count_total > 0 else 0
    return word_count_total, technical_word_count, density

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--reference",required=True)
    parser.add_argument("--glossary",required=True)
    parser.add_argument("--clip_name",required=True)
    args=parser.parse_args()

    total,technical,density=computing_density(args.reference,args.glossary)
    print(f"{args.clip_name}:{total} spoken words,{technical} technical occurrences, density={density:.2f}%")
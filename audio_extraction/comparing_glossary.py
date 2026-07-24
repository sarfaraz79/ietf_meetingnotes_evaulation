import re
import argparse

def load_the_gloss(path):
    terms=set()
    with open(path) as f:
        for line in f:
            line=line.strip().lower()
            if line and not line.startswith('#'):
                terms.add(line)
    return terms

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--manual",required=True)
    parser.add_argument("--automated",required=True)
    parser.add_argument("--reference",required=True)
    args=parser.parse_args()
    
    terms_manual=load_the_gloss(args.manual)
    automated_terms=load_the_gloss(args.automated)
    overlap=terms_manual& automated_terms
    only_manual=terms_manual-automated_terms
    
    print(f"manual gloss:{len(terms_manual)} terms")
    print(f"automated gloss:{len(automated_terms)} terms")
    print(f"overlap:{len(overlap)}the terms in both : {sorted(overlap)}")
    print(f"automated missed these:{sorted(only_manual)}")
    with open(args.reference)as f:
        reference_text=f.read().lower()
    present=[text for text in automated_terms if re.search(r"\b"+re.escape(text)+r"\b",reference_text)]
    noise=len(automated_terms)-len(present)
    ratio=100*noise/len(automated_terms) if automated_terms else 0
    
    print(f"\nof{len(automated_terms)}automated_terms,{len(present)} show up in the reference")
    print(f"ratio of the noise:{ratio:.1f} terms which arent spoken")

if __name__=="__main__":
    main()
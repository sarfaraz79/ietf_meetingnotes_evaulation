#external libraries used
#[1] nltk:www.nltk.org
#author: NLTK Project
#URL: www.nltk.org

import nltk
import re
import argparse
from collections import Counter
nltk.download('words',quiet=True)# using this way to download the words
nltk.download('wordnet',quiet=True)
nltk.download('omw-1.4',quiet=True)

from nltk.corpus import words as nltk_words
from nltk.stem import WordNetLemmatizer

ENGLISH_DICTIONARY=set(words.lower() for words in nltk_words.words())#setting the english dicitonary
LEMMATIZER=WordNetLemmatizer()

def main():
    parser=argparse.ArgumentParser()#argument parser to get files from command line or batch jobs
    parser.add_argument("--documents",nargs="+",required=True)
    parser.add_argument("--output",required=True)
    parser.add_argument("--minimum_length",type=int,default=2)
    parser.add_argument("--minimum_frequency",type=int,default=1)
    args=parser.parse_args()
    
    text_combined=""
    for document_path in args.documents:
        with open(document_path,errors="ignore") as f:#ignoring the errors while reading the file
            text_combined+=f.read()+"\n"
        print(f"read the {document_path}")
    
    extracting_candidate=extracting_candidate_terms(text_combined,args.minimum_length,args.minimum_frequency)#extacting the technical terms
    with open(args.output,"w") as f:
        for word,count in extracting_candidate.most_common():#ascending order to descending order of the words extracted based on commonness
            f.write(f"{word}\n")
    
    for word,count in extracting_candidate.most_common(20):
        print(f"{word:20}x{count}")#this will print the top 20 common words which are extracted
    
def extracting_candidate_terms(text,minimum_length=2,minimum_frequency=1):
    tokens=re.findall(r"[a-zA-Z][a-zA-Z0-9]*",text.lower())
    token_counts=Counter(tokens)
    candidate={word:count for word,count in token_counts.items()#filtering words so only domain words are present
               if not is_dictionary_word(word)
               and len(word)>=minimum_length
               and count>=minimum_frequency
               }
    return Counter(candidate)

def is_dictionary_word(word):
    if word in ENGLISH_DICTIONARY:
        return True
    for part_of_speech in ('n','v','a'):#will check if the word is present in the dictionary as noun,verb or adjective
        if LEMMATIZER.lemmatize(word,part_of_speech) in ENGLISH_DICTIONARY:
            return True
    return False     
    
if __name__=="__main__":
    main()
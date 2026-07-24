#this script will measure the semantic similarity between two sentences using the Sentence-BERT model. It will take two sentences as input and output a similarity score between 0 and 1, where 1 indicates that the sentences are semantically identical and 0 indicates that they are completely different.

#external libraries used in this file
#[1]sentence-transformers: https://www.sbert.net/
#[2]scikit-learn: https://scikit-learn.org/stable/

import argparse
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from bert_score import score as bertscore

def load_text(file_path):
    with open(file_path) as f:
        return f.read().strip()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--reference", required=True, help="Path to the reference file")
    parser.add_argument("--hypothesis", required=True, help="Path to the hypothesis file")
    parser.add_argument("--model", default="all-MiniLM-L6-v2", help="Sentence-BERT model to use")
    parser.add_argument("--output", default="semantic_similarity_output.txt", help="Path to save the result")
    args=parser.parse_args()
    
    reference=load_text(args.reference)
    hypothesis=load_text(args.hypothesis)
    model=SentenceTransformer(args.model)
    reference_embedding=model.encode([reference])
    hypothesis_embedding=model.encode([hypothesis])
    similarity_score=cosine_similarity(reference_embedding, hypothesis_embedding)[0][0]
    P,R,F1=bertscore([hypothesis], [reference], lang="en",verbose=False)
    bert_score_F1=float(F1[0])

    with open(args.output, "w") as f:
        f.write(f"Semantic Similarity Score: {similarity_score}\n")
        f.write(f"Reference: {reference}\n")
        f.write(f"Hypothesis: {hypothesis}\n")
        f.write(f"Model: {args.model}\n")
        f.write(f"Semantic Similarity Score: {similarity_score}\n")
        f.write(f"F1_BertScore:{bert_score_F1:.4f}\n")
    print(f"Semantic Similarity Score: {similarity_score}, BERTScore_F1: {bert_score_F1:.4f}")
    
if __name__ == "__main__":
    main()
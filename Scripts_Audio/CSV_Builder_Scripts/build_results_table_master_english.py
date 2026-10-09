import os, csv, re

ROOT = "master_results_english"#foldername where the master_results_english.csv will be saved

def get_wer(path):#extracting WER from the file
    if not os.path.exists(path): return ""
    with open(path) as f: text = f.read()
    m = re.search(r"Word Error Rate:\s*([0-9.]+)", text)
    return float(m.group(1)) if m else ""

def get_trr(path):#extracting terminology retention from file
    if not os.path.exists(path): return ""
    with open(path) as f: text = f.read()
    m = re.search(r"TRR:\s*([0-9.]+)", text)
    return round(float(m.group(1)), 4) if m else ""

def get_sbert(path):#extracting sbert
    if not os.path.exists(path): return ""
    with open(path) as f: text = f.read()
    m = re.search(r"Semantic Similarity Score\s*:\s*([0-9.]+)", text)
    return round(float(m.group(1)), 4) if m else ""

def get_bert(path):#extracting bert
    if not os.path.exists(path): return ""
    with open(path) as f: text = f.read()
    m = re.search(r"F1_BertScore\s*:\s*([0-9.]+)", text)
    return round(float(m.group(1)), 4) if m else ""

MODELS = ["tiny","tiny.en","base","base.en","small","small.en",
          "medium","medium.en","large-v3","turbo"]#model to collect from 

rows = []
CLIPS = ["idr","netconf","lamps","plenary_openmic"]

for clip in CLIPS:#looping through the folders
    for model in MODELS:
        wer = get_wer(f"{ROOT}/clips_results/{clip}/{model}_wer.txt")
        trr = get_trr(f"{ROOT}/clips_results/{clip}/{model}_trr.txt")
        sbert = get_sbert(f"{ROOT}/semantic/{clip}/{model}.txt")
        bert = get_bert(f"{ROOT}/semantic/{clip}/{model}.txt")
        rows.append([clip, model, wer, trr, sbert, bert])

for model in MODELS:
    wer = get_wer(f"{ROOT}/plenary_full_results/{model}_wer.txt")
    trr = get_trr(f"{ROOT}/plenary_full_results/{model}_trr.txt")
    sbert = get_sbert(f"{ROOT}/semantic/plenary_full/{model}.txt")
    bert = get_bert(f"{ROOT}/semantic/plenary_full/{model}.txt")
    rows.append(["plenary_full", model, wer, trr, sbert, bert])

os.makedirs(ROOT, exist_ok=True)
with open(f"{ROOT}/master_results_english.csv", "w", newline="") as f:#save to csv
    w = csv.writer(f)
    w.writerow(["clip","model","wer","trr","sbert","bertscore"])
    w.writerows(rows)

print(f"wrote {ROOT}/master_results_english.csv with {len(rows)} rows")

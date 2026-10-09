import os, csv, re

ROOT = "master_results"

def get_wer(path):#extract wer
    if not os.path.exists(path): return ""
    with open(path) as f: text = f.read()
    m = re.search(r"Word Error Rate:\s*([0-9.]+)", text)
    return float(m.group(1)) if m else ""

def get_trr(path):#extract terminology retention
    if not os.path.exists(path): return ""
    with open(path) as f: text = f.read()
    m = re.search(r"TRR:\s*([0-9.]+)", text)
    return round(float(m.group(1)), 4) if m else ""

def get_sbert(path):#extract sbert
    if not os.path.exists(path): return ""
    with open(path) as f: text = f.read()
    m = re.search(r"Semantic Similarity Score\s*:\s*([0-9.]+)", text)
    return round(float(m.group(1)), 4) if m else ""

def get_bert(path):#extract bert
    if not os.path.exists(path): return ""
    with open(path) as f: text = f.read()
    m = re.search(r"F1_BertScore\s*:\s*([0-9.]+)", text)
    return round(float(m.group(1)), 4) if m else ""

MODELS = ["tiny","tiny.en","base","base.en","small","small.en",
          "medium","medium.en","large-v3","turbo"]

rows = []
CLIPS = ["idr","netconf","lamps","plenary_openmic"]

for clip in CLIPS:
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
with open(f"{ROOT}/master_results.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["clip","model","wer","trr","sbert","bertscore"])
    w.writerows(rows)

print(f"wrote {ROOT}/master_results.csv with {len(rows)} rows")

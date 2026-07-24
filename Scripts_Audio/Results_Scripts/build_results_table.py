import os, csv, re

def get_wer(path):
    if not os.path.exists(path): return ""
    with open(path) as f: text =f.read()
    m=re.search(r"Word Error Rate:\s*([0-9.]+)", text)
    return float(m.group(1)) if m else ""

def get_trr(path):
    if not os.path.exists(path): return ""
    with open(path) as f: text=f.read()
    m=re.search(r"TRR:\s*([0-9.]+)", text)
    return round(float(m.group(1)), 4) if m else ""

def get_sbert(path):
    if not os.path.exists(path): return ""
    with open(path) as f: text = f.read()
    m=re.search(r"Semantic Similarity Score\s*:\s*([0-9.]+)", text)
    return round(float(m.group(1)), 4) if m else ""

def get_bert(path):
    if not os.path.exists(path): return ""
    with open(path) as f: text = f.read()
    m=re.search(r"F1_BertScore\s*:\s*([0-9.]+)", text)
    return round(float(m.group(1)), 4) if m else ""

MODELS = ["tiny","tiny.en","base","base.en","small","small.en",
          "medium","medium.en","large-v3","turbo"]

rows = []
CLIPS = ["idr","netconf","lamps","plenary_openmic"]

for clip in CLIPS:
    for model in MODELS:
        wer = get_wer(f"clips_results/{clip}/{model}_wer.txt")
        trr = get_trr(f"clips_results/{clip}/{model}_trr.txt")
        sbert = get_sbert(f"result/semantic/{clip}/{model}.txt")
        bert = get_bert(f"result/semantic/{clip}/{model}.txt")
        rows.append([clip, model, wer, trr, sbert, bert])

for model in MODELS:
    wer = get_wer(f"plenary_full_results/{model}_wer.txt")
    trr = get_trr(f"plenary_full_results/{model}_trr.txt")
    sbert = get_sbert(f"result/semantic/plenary_full/{model}.txt")
    bert = get_bert(f"result/semantic/plenary_full/{model}.txt")
    rows.append(["plenary_full", model, wer, trr, sbert, bert])

with open("result/master_results.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["clip","model","wer","trr","sbert","bertscore"])
    w.writerows(rows)

print(f"wrote result/master_results.csv with {len(rows)} rows")
print()
for clip in CLIPS + ["plenary_full"]:
    print(clip)
    for row in rows:
        if row[0] == clip:
            print(f"  {row[1]:12} wer {row[2]}  trr {row[3]}  sbert {row[4]}  bert {row[5]}")
    print()

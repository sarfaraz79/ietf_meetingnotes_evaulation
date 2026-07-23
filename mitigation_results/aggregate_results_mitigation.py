import os
import re
import glob
import csv
 
ROOT = "mitigation_results"
 
CLIPS = ["idr", "netconf", "lamps", "plenary_openmic", "plenary_full"]
MODELS = ["tiny", "medium.en", "medium", "base", "large-v3", "turbo"]  # longest/most specific first, see note below
TECHNIQUES = ["no_prev_text", "higher_no_speech", "forced_english", "combined", "baseline"]  # longest first
 
def extract_wer(file_path):
    with open(file_path) as f:
        text = f.read()
    m = re.search(r"Word Error Rate:\s*([0-9.]+)", text)
    return float(m.group(1)) if m else None
 
def parse_filename(file_path, clip):
    base = os.path.basename(file_path)
    base = base.replace("_wer.txt", "")
    technique_found = None
    for t in TECHNIQUES:
        if base.endswith("_" + t):
            technique_found = t
            base = base[: -(len(t) + 1)]
            break
    model_found = None
    for m in MODELS:
        if base.endswith("_" + m):
            model_found = m
            base = base[: -(len(m) + 1)]
            break
    return technique_found, model_found
 
rows = []
for clip in CLIPS:
    wer_files = glob.glob(os.path.join(ROOT, clip, "*_wer.txt"))
    for file_path in wer_files:
        technique, model = parse_filename(file_path, clip)
        wer = extract_wer(file_path)
        if technique is None or model is None or wer is None:
            print(f"WARNING: could not fully parse {file_path} "
                  f"(technique={technique}, model={model}, wer={wer})")
            continue
        rows.append([clip, model, technique, wer])
model_order = {m: i for i, m in enumerate(["tiny", "base", "medium", "medium.en", "large-v3", "turbo"])}
technique_order = {t: i for i, t in enumerate(["baseline", "no_prev_text", "higher_no_speech", "forced_english", "combined"])}
rows.sort(key=lambda r: (CLIPS.index(r[0]), model_order.get(r[1], 99), technique_order.get(r[2], 99)))
 
out_path = os.path.join(ROOT, "mitigation_summary.csv")
with open(out_path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["clip", "model", "technique", "wer"])
    w.writerows(rows)
 
print("clip,model,technique,wer")
for row in rows:
    print(f"{row[0]},{row[1]},{row[2]},{row[3]}")
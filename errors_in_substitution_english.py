
# Libraries used: 
# os 
# re
# ast
# glob
# collections

import os 
import re 
import ast
import glob
from collections import Counter

# filler words: losing thes ewon't change any technical meaning
FILLER={'a','the','and','uh','um','i','is','you','we','are','so','of','to','it',
          'that','oh','am','as','be','in','with','this','was','were','an','on','at',
          'or','but','if','then','there','here','no','yes','thats','will','next','la'}


TECHICAL_WORD={'quic','yang','netconf','netcom','ietf','tls','udp','iana','enm','semver',
        'bgp','ecmp','rocev2','roce','prp','sla','gpu','rdma','dpf','aigp','ebgp',
        'pki','eku','x509','crl','ocsp','ca','rfc','idr','lamps','iesg','iab'}

def categorise_subs(subs):
    technical_word=filler=morph=other=0
    tech_ex=[]
    for s in subs:
        if '->' not in s: continue
        ref=s.split('->')[0].strip().lower()
        hyp=s.split('->')[1].strip().lower()
        if ref in TECHICAL_WORD:
            technical_word+=1;
            tech_ex.append(f"{ref}->{hyp}")
        elif ref in FILLER:
            filler+=1
        elif ref+'s'==hyp or hyp+'s'==ref or (len(ref)>3 and len(hyp)>3 and ref[:3]==hyp[:3]):
            morph+=1
        else:
            other+=1
    return technical_word,filler,morph,other,tech_ex

def parse_list(line):
    m=re.search(r"\[.*\]", line)
    if not m: return []
    try:
        return ast.literal_eval(m.group(0))
    except:
        return []

def analyse_file(path):
    subs=dels=[]
    with open(path) as f:
        for line in f:
            if line.startswith("Substitutions:"): subs=parse_list(line)
            if line.startswith("Deletions:"): dels=parse_list(line)
    if not subs and not dels: return None
    t,fi,mo,ot,ex=categorise_subs(subs)
    total=len(subs)
    del_filler=sum(1 for d in dels if str(d).lower() in FILLER)
    return {
        "subs_total":total,"technical_word":t,"filler":fi,"morph":mo,"other":ot,
        "tech_examples":Counter(ex),
        "dels_total":len(dels),"dels_filler":del_filler
    }

# run across all  files of wer under master_results_english
files = glob.glob("master_results_english/**/*_wer.txt", recursive=True)
print(f"found {len(files)} WER files\n")

for path in sorted(files):
    r=analyse_file(path)
    if not r or r["subs_total"]==0: continue
    t=r["subs_total"]
    name=path.replace("master_results_english/","").replace("_wer.txt","")
    print(f"{name}")
    print(f"  substitutions {t}: technical {r['technical_word']} ({100*r['technical_word']//t}%), "
          f"filler {r['filler']} ({100*r['filler']//t}%), "
          f"morph {r['morph']} ({100*r['morph']//t}%), "
          f"other-meaning {r['other']} ({100*r['other']//t}%)")
    print(f"  deletions {r['dels_total']}: filler/disfluency {r['dels_filler']}")
    if r["tech_examples"]:
        top=", ".join(f"{k} x{v}" for k,v in r["tech_examples"].most_common(6))
        print(f"  top technical corruptions: {top}")
    print()
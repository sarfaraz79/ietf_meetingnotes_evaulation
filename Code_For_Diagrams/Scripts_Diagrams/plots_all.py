#external libraries used:
#[1]pandas: https://pandas.pydata.org/
#[2]matplotlib: https://matplotlib.org/
#[3]numpy: https://numpy.org/

#the numbers are taken from the master_results.csv,master_results_english.csv,baseline_results.csv

import re
import os
import ast
import glob
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt

order_of_model=["tiny","tiny.en","base","base.en","small","small.en","medium","medium.en","large-v3","turbo"]#the model's based on their sizes
baseline_order_of_model=["tiny","base","small","medium","large-v3","turbo"]
DIRECTORY=os.path.dirname(os.path.abspath(__file__))
MASTER_RESULTS_CSV_PATH = os.path.join(DIRECTORY,"..","..","master_results/master_results.csv")
MASTER_RESULTS_ENGLISH_CSV_PATH = os.path.join(DIRECTORY,"..","..","master_results_english/master_results_english.csv")
BASELINE_RESULTS_CSV_PATH = os.path.join(DIRECTORY,"..","..","librispeech_model_test_results/baseline_results.csv")

df_master=pd.read_csv(MASTER_RESULTS_CSV_PATH).drop_duplicates(subset=["clip","model"]).reset_index(drop=True)#reading and dropping the duplicate rows
df_master_english=pd.read_csv(MASTER_RESULTS_ENGLISH_CSV_PATH).drop_duplicates(subset=["clip","model"]).reset_index(drop=True)
df_baseline=pd.read_csv(BASELINE_RESULTS_CSV_PATH).drop_duplicates(subset=["model"]).reset_index(drop=True)

def get_values(df,clip,column):#this helper method will return values in the order of models and none if any clip is missing
    subset_df=df[df["clip"]==clip]
    lookup=dict(zip(subset_df["model"],subset_df[column]))
    return [lookup.get(m) for m in order_of_model]


#this is for the librispeech baseline results against wer
df_base_sorted=df_baseline.set_index("model").reindex(baseline_order_of_model).reset_index()
plt.figure(figsize=(8,5))
plt.plot(df_base_sorted["model"],df_base_sorted["WER"]*100,marker="o",linewidth=2,color="blue")#plotting the baseline results
plt.title("WER on LibriSpeech Test Set")
plt.xlabel("Whisper Model")
plt.ylabel("WER in %")
plt.grid(True,alpha=0.3)
for x,y in zip(df_base_sorted["model"],df_base_sorted["WER"]*100):
    plt.text(x,y+0.2,f"{y:.1f}",ha="center",fontsize=9)#adding the WER values on the plot
plt.tight_layout()
plt.savefig("baseline_results_librispeech.pdf")#saving the plot
plt.close()

#this is for WER wrt Whisper model sizes across the IETF meetings
main_clips=["idr","netconf","lamps","plenary_openmic","plenary_full"]
plt.figure(figsize=(10,6))
for clip_name in main_clips:
    plt.plot(order_of_model,get_values(df_master,clip_name,"wer"),marker="o",linewidth=2,label=clip_name)
plt.title("WER across Whisper Model Sizes")
plt.xlabel("Whisper Models")
plt.ylabel("Word Error Rate")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True,alpha=0.3)
plt.tight_layout()
plt.savefig("wer_across_whisper_model_sizes.pdf")#saving the plot
plt.close()


#this is for the terminology retention of my ietf sources
plt.figure(figsize=(10,6))
for clip_name in main_clips:
    plt.plot(order_of_model,get_values(df_master,clip_name,"trr"),marker="s",linewidth=2,label=clip_name)
plt.title("Terminology Retention Rate across Whisper Model Sizes")
plt.xlabel("Whisper Models")
plt.ylabel("Terminology Retention Rate")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True,alpha=0.3)
plt.tight_layout()
plt.savefig("trr_across_whisper_model_sizes.pdf")#saving the plot
plt.close()

#this is for the relationship between the word error rate and the terminology retention rate across the IETF meetings
plt.figure(figsize=(10,6))
plt.scatter(df_master["wer"]*100,df_master["trr"]*100,alpha=0.5)
plt.title("Relationship between WER and TRR across IETF Meetings")
plt.xlabel("Word Error Rate in %")
plt.ylabel("Terminology Retention Rate in %")
plt.grid(True,alpha=0.3)
plt.tight_layout()
plt.savefig("relationship_between_wer_and_trr.pdf")#saving the plot
plt.close()


#this is for all the 4 evaluation metrics on the full plenary
row=df_master[(df_master["clip"]=="plenary_full") & (df_master["model"]=="large-v3")].iloc[0]
names_of_metrics=["wer","trr","sbert","bertscore"]
values_of_metrics=[row["wer"],row["trr"],row["sbert"],row["bertscore"]]
plt.figure(figsize=(8,5))
bars=plt.bar(names_of_metrics,values_of_metrics,color=["blue","orange","green","red"])
plt.title("Evaluation Metrics on Plenary Full for Large-v3 Model")
plt.ylabel("Percentage")
plt.ylim(0,1)
for bar,value in zip(bars,values_of_metrics):
    plt.text(bar.get_x() + bar.get_width()/2, value + 0.02, f"{value:.2f}", ha='center', fontsize=9)
plt.tight_layout()
plt.savefig("evaluation_metrics_plenary_full_large_v3.pdf")#saving the plot
plt.close()

#this is for the benchmark on the ietf base model and libirispeech baseline results(need to check coming wrong or remove entirely)
#ietf_base_model_row=df_master[df_master["model"]=="base"]["wer"].mean()*100
#librispeech_baseline_row=6.29
#plt.figure(figsize=(8,5))
#bars=plt.bar(["IETF Base Model","LibriSpeech Baseline"],[ietf_base_model_row,librispeech_baseline_row],color=["blue","orange"])
#plt.title("WER Benchmark between IETF Base Model and LibriSpeech Baseline")
#plt.ylabel("Word Error Rate in %")
#plt.ylim(0,100)
#for bar,value in zip(bars,[ietf_base_model_row,librispeech_baseline_row]):
#    plt.text(bar.get_x() + bar.get_width()/2, value +0.3, f"{value:.1f}", ha='center', fontsize=9)
#plt.tight_layout()
#plt.savefig("wer_benchmark_ietf_base_vs_librispeech_baseline.pdf")#saving the plot
#plt.close()

#this is for the benchmark on the ietf tiny model and libirispeech tiny results(need to check coming wrong or remove entirely)
#ietf_tiny_model_row=df_master[df_master["model"]=="tiny"]["wer"].mean()*100
#librispeech_baseline_row_tiny=8.19
#plt.figure(figsize=(8,5))
#bars=plt.bar(["IETF tiny Model","LibriSpeech Baseline"],[ietf_tiny_model_row,librispeech_baseline_row_tiny],color=["blue","orange"])
#plt.title("WER Benchmark between IETF tiny Model and LibriSpeech tiny Baseline")
#plt.ylabel("Word Error Rate in %")
#plt.ylim(0,100)
#for bar,value in zip(bars,[ietf_tiny_model_row,librispeech_baseline_row_tiny]):
#    plt.text(bar.get_x() + bar.get_width()/2, value +0.3, f"{value:.1f}", ha='center', fontsize=9)
#plt.tight_layout()
#plt.savefig("wer_benchmark_ietf_tiny_vs_librispeech_baseline.pdf")#saving the plot
#plt.close()

#figure for domain gap between librispeech and each ietf audio source
domain_gap_clips=["idr","netconf","lamps","plenary_openmic","plenary_full"]
domain_gap_wer=[get_values(df_master,clip_name,"wer")[order_of_model.index("base")] for clip_name in domain_gap_clips]
domain_gap_labels=["LibriSpeech\n(clean)"]+domain_gap_clips
domain_gap_values=[df_baseline[df_baseline["model"]=="base"]["WER"].iloc[0]*100]+[w*100 for w in domain_gap_wer]
plt.figure(figsize=(10,6))
bars=plt.bar(domain_gap_labels,domain_gap_values,color=["yellow","blue","blue","blue","blue","blue"])
plt.title("LibriSpeech Base Benchmark vs Base IETF Source")
plt.ylabel("Word Error Rate")
for bar,value in zip(bars,domain_gap_values):
    plt.text(bar.get_x()+bar.get_width()/2,value+0.5,f"{value:.1f}",ha='center',fontsize=9)
plt.tight_layout()
plt.savefig("gap_in_domain.pdf")
plt.close()

#this is for netconf comparing the netconf because it went into welsh
master_netconf=get_values(df_master,"netconf","wer")
english_netconf=get_values(df_master_english,"netconf","wer")
x_positions=range(len(order_of_model))
bar_width=0.35
plt.figure(figsize=(10,6))
plt.bar([i-bar_width/2 for i in x_positions],[v*100 if v is not None else 0 for v in master_netconf],width=bar_width,label="IETF Netconf(No language restriction)",color="blue")
plt.bar([i+bar_width/2 for i in x_positions],[v*100 if v is not None else 0 for v in english_netconf],width=bar_width,label="English Netconf",color="orange")
plt.title("WER Comparison for Netconf Meeting")
plt.xticks(list(x_positions),order_of_model,rotation=45)
plt.ylabel("Word Error Rate in %")
plt.title("WER Comparison for Netconf Meeting(Normal vs Forced English)")
plt.legend()
plt.grid(True,alpha=0.3)
plt.tight_layout()
plt.savefig("wer_comparison_netconf_normal_vs_forced_english.pdf")#saving the plot
plt.close()

#metrics evaluation on the welsh hallucination
welsh_hallucination_row=df_master[(df_master["clip"]=="netconf")&(df_master["model"]=="medium")].iloc[0]
welsh_hallucination_metrics=[welsh_hallucination_row["wer"],welsh_hallucination_row["trr"],welsh_hallucination_row["sbert"],welsh_hallucination_row["bertscore"]]
plt.figure(figsize=(8,5))
bars=plt.bar(names_of_metrics,welsh_hallucination_metrics,color=["blue","orange","green","red"])
plt.title("Metrics Evaluation on Welsh Hallucination for Medium Model")
plt.ylabel("Metric Score")
plt.ylim(0,1)
for bar,value in zip(bars,welsh_hallucination_metrics):
    plt.text(bar.get_x() + bar.get_width()/2, value + 0.02, f"{value:.2f}", ha='center', fontsize=9)
plt.tight_layout()
plt.savefig("metrics_evaluation_welsh_hallucination_medium_model.pdf")#saving the plot
plt.close()

#sbert and bertscore by model size 
fig,axes=plt.subplots(1,2,figsize=(12,5))
for clip_name in main_clips:
    axes[0].plot(order_of_model,get_values(df_master,clip_name,"sbert"),marker="o",linewidth=2,label=clip_name)
    axes[1].plot(order_of_model,get_values(df_master,clip_name,"bertscore"),marker="s",linewidth=2,label=clip_name)
axes[0].set_title("SBERT Score across Whisper Model Sizes")
axes[0].set_ylabel("SBERT Score")
axes[0].set_xticks(range(len(order_of_model)))
axes[0].set_xticklabels(order_of_model, rotation=45)
axes[1].set_title("BERTScore across Whisper Model Sizes")
axes[1].set_ylabel("F1 BERTScore")
axes[1].set_xticks(range(len(order_of_model)))
axes[1].set_xticklabels(order_of_model, rotation=45)
axes[1].grid(True,alpha=0.3)
axes[1].legend()
plt.tight_layout()
plt.savefig("sbert_and_bertscore_across_whisper_model_sizes.pdf")#saving the plot
plt.close()


#evaluation of when we force english on wer on each clip(need to check)
all_clips=["idr","netconf","lamps","plenary_openmic","plenary_full"]
plt.figure(figsize=(10,6))
for clip_name in all_clips:
    master_values=get_values(df_master,clip_name,"wer")
    english_values=get_values(df_master_english,clip_name,"wer")
    delta=[(e-a)*100 if(e is not None and a is not None) else None for e,a in zip(english_values,master_values)]
    plt.plot(order_of_model,delta,marker="o",linewidth=2,label=clip_name)
plt.axhline(y=0,color="black",linestyle="--",linewidth=1)
plt.xticks(range(len(order_of_model)),order_of_model,rotation=45)
plt.ylabel("WER Difference (Forced English - Normal) in %")
plt.title("WER Difference when Forcing English on Each Clip")
plt.legend()
plt.grid(True,alpha=0.3)
plt.tight_layout()
plt.savefig("wer_difference_forced_english_vs_normal.pdf")#saving the plot
plt.close()

# this is for the substitution errors
FILLER={'a','the','and','uh','um','i','is','you','we','are','so','of','to','it',
          'that','oh','am','as','be','in','with','this','was','were','an','on','at',
          'or','but','if','then','there','here','no','yes','thats','will','next','la',
          'know','kind','okay','well','just','right','like','really','going','get',
          'got','one','some','been','has','had','would','could','should','im',
          'youre','theyre','its','dont','didnt','isnt','theres','and','so'}


TECHICAL_WORD={'quic','yang','netconf','netcom','ietf','tls','udp','iana','enm','semver',
        'bgp','ecmp','rocev2','roce','prp','sla','gpu','rdma','dpf','aigp','ebgp',
        'pki','eku','x509','crl','ocsp','ca','rfc','idr','lamps','iesg','iab',
        'attestation','pkix','irtf','llc','nomcom','ipmc','bof','bofs','catalist',
        'dispatch','onsite','secretariat','meetecho','moq','asn1','rasprg'}

def parse_substitution(line):
    match=re.search(r"\[.*\]",line)
    if not match:
        return []
    try:
        return ast.literal_eval(match.group(0))
    except(SyntaxError,ValueError):
        return []
    
def categorise_substitutions(substitutions):
    technical_word=filler=morph=other=0
    for pair in substitutions:
        if '->' not in pair:
            continue
        reference_word=pair.split('->')[0].strip().lower()
        hypothesis_word=pair.split('->')[1].strip().lower()
        if reference_word in TECHICAL_WORD:
            technical_word+=1
        elif reference_word in FILLER:
            filler+=1
        elif reference_word+'s'==hypothesis_word or hypothesis_word+'s'==reference_word or (len(reference_word)>3 and len(hypothesis_word)>3 and reference_word[:3]==hypothesis_word[:3]):
            morph+=1
        else:
            other+=1
    return technical_word,filler,morph,other

def build_substitution_breakdown(results):
    clip_counts=defaultdict(lambda:[0,0,0,0,0])
    wer_files=glob.glob(os.path.join(results,"**","*_wer.txt"),recursive=True)
    for file_path in wer_files:
            substitutions=[]
            with open(file_path) as file:
                for line in file:
                    if line.startswith("Substitutions:"):
                        substitutions=parse_substitution(line)
                        break
            if "plenary_full_results" in file_path:
                clip_name="plenary_full"
            elif "clips_results" in file_path:
                clip_name=file_path.split("clips_results"+os.sep)[1].split(os.sep)[0]
            else:
                continue
            technical_word,filler,morph,other=categorise_substitutions(substitutions)
            clip_counts[clip_name][0]+=technical_word
            clip_counts[clip_name][1]+=filler
            clip_counts[clip_name][2]+=morph
            clip_counts[clip_name][3]+=other
            clip_counts[clip_name][4]+=len(substitutions)
    breakdown={}
    for clip_name,(technical_word,filler,morph,other,total) in clip_counts.items():
        if total==0:
            continue
        breakdown[clip_name]=(100*technical_word/total,100*filler/total,100*morph/total,100*other/total,total)
    return breakdown
    
def plot_substitution_breakdown(breakdown,title_suffix,output_name):
    order_of_clips=["idr","netconf","lamps","plenary_openmic","plenary_full"]
    order_of_clip=[clip for clip in order_of_clips if clip in breakdown]
    technical_word_percentages=[breakdown[clip][0] for clip in order_of_clip]
    filler_percentages=[breakdown[clip][1] for clip in order_of_clip]
    morph_percentages=[breakdown[clip][2] for clip in order_of_clip]
    other_percentages=[breakdown[clip][3] for clip in order_of_clip]
    plt.figure(figsize=(10,6))
    plt.bar(order_of_clip,technical_word_percentages,label="Technical Word",color="blue")
    plt.bar(order_of_clip,filler_percentages,bottom=technical_word_percentages,label="filler/ function word",color="orange")
    running_bottom=[t+f for t,f in zip(technical_word_percentages,filler_percentages)]
    plt.bar(order_of_clip,morph_percentages,bottom=running_bottom,label="Morphological",color="green")
    running_bottom=[b+m for b,m in zip(running_bottom,morph_percentages)]
    plt.bar(order_of_clip,other_percentages,bottom=running_bottom,label="Other Meaning",color="red")
    plt.title(f"Substitution Error Breakdown {title_suffix}")
    plt.ylabel("Percentage of Substitutions")
    plt.legend(loc="upper center",bbox_to_anchor=(0.5,-0.15),ncol=2)
    plt.tight_layout()
    plt.savefig(output_name)
    plt.close()
    
auto_breakdown=build_substitution_breakdown(os.path.join(DIRECTORY,"..","..","master_results"))
plot_substitution_breakdown(auto_breakdown,"(Auto Transcription)","substitution_error_breakdown_auto_transcription.pdf")
for clip_name,(technical_word,filler,morph,other,total) in auto_breakdown.items():
    print(f"{clip_name}: Technical Word: {technical_word:.2f}%, Filler: {filler:.2f}%, Morphological: {morph:.2f}%, Other Meaning: {other:.2f}%")
if os.path.isdir(os.path.join(DIRECTORY,"..","..","master_results_english")):
    english_breakdown=build_substitution_breakdown(os.path.join(DIRECTORY,"..","..","master_results_english"))
    plot_substitution_breakdown(english_breakdown,"(English Transcription)","substitution_error_breakdown_english_transcription.pdf")
    for clip_name,(technical_word,filler,morph,other,total) in english_breakdown.items():
        print(f"{clip_name}: Technical Word: {technical_word:.2f}%, Filler: {filler:.2f}%, Morphological: {morph:.2f}%, Other Meaning: {other:.2f}%")
else:
    print("English transcription results not found, skipping English breakdown plot.")
    
    
def loading_debug_output(debug_path):
    pattern = re.compile(
        r"\[(?P<start>[\d.]+)-(?P<end>[\d.]+)\)\]"
        r"avg_logprob=(?P<avg_logprob>-?[\d.]+)"
        r"no_speech_prob=(?P<no_speech_prob>[\d.]+)"
        r"compression_ratio=(?P<compression_ratio>[\d.]+)")
    segments=[]
    with open(debug_path) as file:
        for line in file:
            match=pattern.search(line)
            if match:
                segments.append({
                    "start":float(match.group("start")),
                    "no_speech_prob":float(match.group("no_speech_prob")),
                    "compression_ratio":float(match.group("compression_ratio"))
                })
    return segments

master_debug_path=os.path.join(DIRECTORY,"..","..","master_results/clips_results/netconf/transcription_medium/netconf_tech.wav_whisper_debug.txt")
master_english_debug_path=os.path.join(DIRECTORY,"..","..","master_results_english/clips_results/netconf/transcription_medium/netconf_tech.wav_whisper_debug.txt")
auto_segments=loading_debug_output(master_debug_path)
english_segments=loading_debug_output(master_english_debug_path)
fig1,axes_l=plt.subplots(figsize=(12,6))
master_starts=[seg["start"] for seg in auto_segments]
master_no_speech_probs=[seg["no_speech_prob"] for seg in auto_segments]
master_compression_ratios=[seg["compression_ratio"] for seg in auto_segments]
axes_l.set_title("Auto Detected Language Debug Output")
axes_l.set_xlabel("Start Time (s)")
axes_l.set_ylabel("No Speech Probability")
axes_l.plot(master_starts,master_no_speech_probs,marker="o",color="blue")
axes_l.tick_params(axis="y",labelcolor="blue")
axes_l.set_ylim(0,1.2)
ax_left2=axes_l.twinx()
ax_left2.set_ylabel("Compression Ratio")
ax_left2.plot(master_starts,master_compression_ratios,marker="s",color="orange")
ax_left2.tick_params(axis="y",labelcolor="orange")
ax_left2.set_ylim(0,2.5)
fig1.tight_layout()
fig1.savefig("whisper_debug_output_netconf_medium_auto_language.pdf")
plt.close(fig1)

fig2,axes_r=plt.subplots(figsize=(12,6))
english_starts=[seg["start"] for seg in english_segments]
english_no_speech_probs=[seg["no_speech_prob"] for seg in english_segments]
english_compression_ratios=[seg["compression_ratio"] for seg in english_segments]
axes_r.set_title("Forced English Debug Output")
axes_r.set_xlabel("Start Time (s)")
axes_r.set_ylabel("No Speech Probability")
axes_r.plot(english_starts,english_no_speech_probs,marker="o",color="blue")
axes_r.tick_params(axis="y",labelcolor="blue")
axes_r.set_ylim(0,1.2)
ax_right2=axes_r.twinx()
ax_right2.set_ylabel("Compression Ratio")
ax_right2.plot(english_starts,english_compression_ratios,marker="s",color="orange")
ax_right2.tick_params(axis="y",labelcolor="orange")
ax_right2.set_ylim(0,2.5)
fig2.tight_layout()
fig2.savefig("whisper_debug_output_netconf_medium_model_english_forced.pdf")
plt.close(fig2)


def categorise_substitutions_average(substitutions):
    technical_word=filler=morph=other=0
    for pair in substitutions:
        if '->' not in pair:
            continue
        reference_word=pair.split('->')[0].strip().lower()
        hypothesis_word=pair.split('->')[1].strip().lower()
        if reference_word in TECHICAL_WORD:
            technical_word+=1
        elif reference_word in FILLER:
            filler+=1
        elif (reference_word+'s'==hypothesis_word or hypothesis_word+'s'==reference_word or (len(reference_word)>3 and len(hypothesis_word)>3 and reference_word[:3]==hypothesis_word[:3])):
            morph+=1
        else:
            other+=1
    return technical_word,filler,morph,other

def extract_model_name(file_path):
    base_name=os.path.basename(file_path)
    return base_name.replace("_wer.txt","")

def build_substitution_breakdown_average(results):
    clip_counts=defaultdict(lambda:[0,0,0,0,0])
    wer_files=glob.glob(os.path.join(results,"**","*_wer.txt"),recursive=True)
    for file_path in wer_files:
            substitutions=[]
            with open(file_path) as file:
                for line in file:
                    if line.startswith("Substitutions:"):
                        substitutions=parse_substitution(line)
                        break
            if "plenary_full_results" in file_path:
                clip_name="plenary_full"
            elif "clips_results" in file_path:
                clip_name=file_path.split("clips_results"+os.sep)[1].split(os.sep)[0]
            else:
                continue
            model_name=extract_model_name(file_path)
            key=(clip_name,model_name)
            technical_word,filler,morph,other=categorise_substitutions_average(substitutions)
            clip_counts[key][0]+=technical_word
            clip_counts[key][1]+=filler
            clip_counts[key][2]+=morph
            clip_counts[key][3]+=other
            clip_counts[key][4]+=len(substitutions)
    models_per_clip=defaultdict(list)
    for (clip_name,model_name),counts in clip_counts.items():
        models_per_clip[clip_name].append(counts)
    print("Models per clip:", {clip: len(models) for clip, models in models_per_clip.items()})
    for clip_name,models in models_per_clip.items():
        print(f"Clip: {clip_name}, Number of models: {len(models)}, Counts: {models}")
    print()
    clip_percentages=defaultdict(lambda:[[],[],[],[],[]])
    for(clip_name,model_name),(technical_word,filler,morph,other,total) in clip_counts.items():
        if total==0:
            continue
        clip_percentages[clip_name][0].append(100*technical_word/total)
        clip_percentages[clip_name][1].append(100*filler/total)
        clip_percentages[clip_name][2].append(100*morph/total)
        clip_percentages[clip_name][3].append(100*other/total)
        clip_percentages[clip_name][4].append(total)
    breakdown={}
    for clip_name,(technical_word_list,filler_list,morph_list,other_list,total_list) in clip_percentages.items():
        n=len(technical_word_list)
        if n==0:
            continue
        breakdown[clip_name]=(sum(technical_word_list)/n,sum(filler_list)/n,sum(morph_list)/n,sum(other_list)/n,sum(total_list)/n)
    return breakdown

def plot_substitution_breakdown_average(breakdown,title_suffix,output_name):
    order_of_clips=["idr","netconf","lamps","plenary_openmic","plenary_full"]
    order_of_clip=[clip for clip in order_of_clips if clip in breakdown]
    technical_word_percentages=[breakdown[clip][0] for clip in order_of_clip]
    filler_percentages=[breakdown[clip][1] for clip in order_of_clip]
    morph_percentages=[breakdown[clip][2] for clip in order_of_clip]
    other_percentages=[breakdown[clip][3] for clip in order_of_clip]
    plt.figure(figsize=(10,6))
    plt.bar(order_of_clip,technical_word_percentages,label="Technical Word",color="blue")
    plt.bar(order_of_clip,filler_percentages,bottom=technical_word_percentages,label="filler/ function word",color="orange")
    running_bottom=[t+f for t,f in zip(technical_word_percentages,filler_percentages)]
    plt.bar(order_of_clip,morph_percentages,bottom=running_bottom,label="Morphological",color="green")
    running_bottom=[b+m for b,m in zip(running_bottom,morph_percentages)]
    plt.bar(order_of_clip,other_percentages,bottom=running_bottom,label="Other Meaning",color="red")
    plt.title(f"Substitution Error Breakdown {title_suffix}")
    plt.ylabel("Percentage of Substitutions")
    plt.legend(loc="upper center",bbox_to_anchor=(0.5,-0.15),ncol=2)
    plt.tight_layout()
    plt.savefig(output_name)
    plt.close()
    
auto_breakdown=build_substitution_breakdown_average(os.path.join(DIRECTORY,"..","..","master_results"))
plot_substitution_breakdown(auto_breakdown,"(Auto Transcription),average","substitution_error_breakdown_auto_transcription_averaged.pdf")
for clip_name,(technical_word,filler,morph,other,total) in auto_breakdown.items():
    print(f"{clip_name}: Technical Word: {technical_word:.2f}%, Filler: {filler:.2f}%, Morphological: {morph:.2f}%, Other Meaning: {other:.2f}%")
if os.path.isdir(os.path.join(DIRECTORY,"..","..","master_results_english")):
    english_breakdown=build_substitution_breakdown_average(os.path.join(DIRECTORY,"..","..","master_results_english"))
    plot_substitution_breakdown(english_breakdown,"(English Transcription)","substitution_error_breakdown_english_transcription_averaged.pdf")
    for clip_name,(technical_word,filler,morph,other,total) in english_breakdown.items():
        print(f"{clip_name}: Technical Word: {technical_word:.2f}%, Filler: {filler:.2f}%, Morphological: {morph:.2f}%, Other Meaning: {other:.2f}%")
else:
    print("English transcription results not found, skipping English breakdown plot.")
#external libraries used
#[1] numpy
#[2] matplotlib
#[3] pandas

import os

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

cm=1/2.54
DIRECTORY=os.path.dirname(os.path.abspath(__file__))
MITIGATION_CSV_PATH=os.path.join(DIRECTORY,"..","..","mitigation_results","mitigation_summary.csv")

df=pd.read_csv(MITIGATION_CSV_PATH)
clips=["idr","netconf","lamps","plenary_openmic","plenary_full"]
technique=["baseline","no_prev_text","higher_no_speech","forced_english","combined"]
labels=["baseline","no-prev-text","higher-no-speech","forced-english","combined"]
order_of_model=["tiny","base","medium","medium.en","large-v3","turbo"]

#this is for the large-v3 baseline and no_prev_tcext mitigation technique
plt.figure(figsize=(10, 6))
x=range(len(clips))
w=0.35
base_values=[df[(df["clip"]==clip)&(df["model"]=="large-v3")&(df["technique"]=="baseline")]["wer"].iloc[0]*100 for clip in clips]
no_prev_text_values=[df[(df["clip"]==clip)&(df["model"]=="large-v3")&(df["technique"]=="no_prev_text")]["wer"].iloc[0]*100 for clip in clips]
plt.bar([i-w/2 for i in x], base_values, width=w, label="baseline")
plt.bar([i+w/2 for i in x], no_prev_text_values, width=w, label="no-prev-text")
plt.xticks(list(x), clips,rotation=20)
plt.ylabel("WER (%)")
plt.title("WER for large-v3 model with baseline and no-prev-text mitigation technique")
plt.legend()
plt.grid(True,alpha=0.3,axis="y")
for i,(base,no_prev_text) in enumerate(zip(base_values,no_prev_text_values)):
    plt.text(i-w/2, base+0.5, f"{base:.1f}", ha='center',fontsize=9)
    plt.text(i+w/2, no_prev_text+0.5, f"{no_prev_text:.1f}", ha='center',fontsize=9)
plt.tight_layout()
plt.savefig("large-v3_baseline_no_prev_text.pdf")
plt.close()


#this plot is for all the techniques
fig,axes=plt.subplots(2,3,figsize=(35*cm,15*cm),sharey=False)
axes=axes.flatten()
colors=["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd"]
width=0.15
for i,clip in enumerate(clips):
    fig,ax=plt.subplots(figsize=(30*cm,12*cm))
    sub=df[df["clip"]==clip]
    xpos=np.arange(len(order_of_model))
    for j,techniques in enumerate(technique):
        values=[]
        for model in order_of_model:
            row=sub[(sub["model"]==model)&(sub["technique"]==techniques)]
            values.append(row["wer"].iloc[0]*100 if len(row) else None)
        offsets=[x+(j-2)*width for x in xpos]
        ax.bar(offsets, values, width=width, label=technique[j], color=colors[j])
    ax.set_xticks(xpos)
    ax.set_xticklabels(order_of_model,rotation=45,fontsize=10)
    ax.set_title(clip,fontsize=12)
    ax.grid(True,alpha=0.3,axis="y")
    #if i==0:
        #ax.set_ylabel("WER (%)",fontsize=12)
#axes[-1].axis("off")
#handles,labels=axes[0].get_legend_handles_labels()
#fig.legend(handles,labels,loc="lower right",bbox_to_anchor=(0.95,0.08),fontsize=10)
#fig.suptitle("WER for different mitigation techniques across clips and models",fontsize=16)
#plt.tight_layout()
#plt.savefig("all_techniques_across_clips_models.pdf")
#plt.close()
    ax.set_ylabel("WER (%)",fontsize=12)
    ax.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig(f"{clip}_all_techniques_across_models.pdf")
    plt.close()

#this is for the heapmap 
matrix=[]
for clip in clips:
    row=[]
    for model in order_of_model:
        base=(df[(df["clip"]==clip)&(df["model"]==model)&(df["technique"]=="baseline")]["wer"].iloc[0]*100)
        npt=(df[(df["clip"]==clip)&(df["model"]==model)&(df["technique"]=="no_prev_text")]["wer"].iloc[0]*100)
        pct_change=((npt-base)/base)*100
        row.append(pct_change)
    matrix.append(row)
matrix=np.array(matrix)
fig,ax=plt.subplots(figsize=(10,6))
im=ax.imshow(matrix,cmap="RdYlGn_r",vmin=-70,vmax=70,aspect="auto")
ax.set_xticks(range(len(order_of_model)))
ax.set_xticklabels(order_of_model,rotation=45,fontsize=10)
ax.set_yticks(range(len(clips)))
ax.set_yticklabels(clips,fontsize=10)
for i in range(len(clips)):
    for j in range(len(order_of_model)):
        value=matrix[i,j]
        ax.text(j,i,f"{value:.1f}%",ha="center",va="center",color="black" if abs(value)<40 else "white",fontsize=9)
plt.colorbar(im,ax=ax,label="Percentage Change in WER (%)")
plt.title("Percentage Change in WER for no-prev-text mitigation technique compared to baseline",fontsize=14)
plt.tight_layout()
plt.savefig("no_prev_text_percentage_change_heatmap.pdf")
plt.close()


#heatmap with % change and WER value
percentage_change_matrix=[]
absolute_wer_matrix=[]
for clip in clips:
    percentage_row=[]
    absolute_row=[]
    for model in order_of_model:
        base=(df[(df["clip"]==clip)&(df["model"]==model)&(df["technique"]=="baseline")]["wer"].iloc[0]*100)
        npt=(df[(df["clip"]==clip)&(df["model"]==model)&(df["technique"]=="no_prev_text")]["wer"].iloc[0]*100)
        pct_change=((npt-base)/base)*100
        percentage_row.append(pct_change)
        absolute_row.append(npt)
    percentage_change_matrix.append(percentage_row)
    absolute_wer_matrix.append(absolute_row)
fig,ax=plt.subplots(figsize=(10,6))
im=ax.imshow(percentage_change_matrix,cmap="RdYlGn_r",vmin=-70,vmax=70,aspect="auto")
ax.set_xticks(range(len(order_of_model)))
ax.set_xticklabels(order_of_model,rotation=45,fontsize=10)
ax.set_yticks(range(len(clips)))
ax.set_yticklabels(clips,fontsize=10)
for i in range(len(clips)):
    for j in range(len(order_of_model)):
        pct_value=percentage_change_matrix[i][j]
        abs_value=absolute_wer_matrix[i][j]
        ax.text(j,i,f"{pct_value:.1f}%\n({abs_value:.1f})",ha="center",va="center",color="black" if abs(pct_value)<40 else "white",fontsize=9)
plt.colorbar(im,ax=ax,label="Percentage Change in WER (%)")
plt.title("Percentage Change in WER and Absolute WER for no-prev-text mitigation technique compared to baseline",fontsize=14)
plt.tight_layout()
plt.savefig("no_prev_text_percentage_change_and_absolute_wer_heatmap.pdf")
plt.close()
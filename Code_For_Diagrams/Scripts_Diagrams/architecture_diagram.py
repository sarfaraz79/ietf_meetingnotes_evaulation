#libraries used: Matplotlib

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch

fig,ax=plt.subplots(figsize=(12,7))
ax.set_xlim(0,12)
ax.set_ylim(0,8)
ax.axis("off")
def box(x,y,w,h,text,color):
    b=FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.08",linewidth=1.5,ec="black",fc=color)
    ax.add_patch(b)
    ax.text(x+w/2,y+h/2,text,ha="center",va="center",fontsize=12)
def arrow(x1,y1,x2,y2):
    a=FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="->",mutation_scale=18,fc="black",linewidth=1.5,ec="black")
    ax.add_patch(a)
    
box(0.3,5.5,2.2,1.2,"1. Fetching audio using\n yt-dlp & FFmpeg","lightblue")#this is for the pipeline 
box(3.0,5.5,2.2,1.2,"2. Clip the audio from\n huge audio","lightgreen")
box(5.7,5.5,2.2,1.2,"3. Transcribe usng \nWhisper's model","lightyellow")
box(8.4,5.5,3.2,1.2,"4. Evaluate using\n metrics","lightcoral")
arrow(2.5,6.1,3,6.1)
arrow(5.2,6.1,5.7,6.1)
arrow(7.9,6.1,8.4,6.1)

box(8.4,3.4,3.2,1.2,"Using the manual\ntranscription","lightblue")
arrow(10,4.6,10,5.5)
box(5.7,3.4,2.2,1.2,"Feeding the glossary\nto model","lightgreen")
arrow(6.8,4.6,6.8,5.5)
arrow(7.9,4,8.4,4)

box(0.3,3,4.6,1.4,"Validation of pipeline,\nLibrispeech benchmarking,\nand other datasets","lightyellow")
arrow(2.6,4.4,2.6,5.5)

box(8.5,1.2,3.5,1.2,"Master Results","lightcoral")
arrow(10,3.4,10,2.4)
ax.text(6,8,"IETF Pipeline",ha="center",fontsize=14,fontweight="bold")
plt.tight_layout()
plt.savefig("architecture_diagram.png",dpi=300)
plt.close()
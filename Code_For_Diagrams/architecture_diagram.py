#libraries used: Matplotlib

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch

fig,ax=plt.subplots(figsize=(10,8))
ax.set_xlim(0,12)
ax.set_ylim(0,8)
ax.axis("off")
def box(x,y,w,h,text,color):
    b=FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.1",ec="black",fc=color,mutation_aspect=0.5)
    ax.add_patch(b)
    ax.text(x+w/2,y+h/2,text,ha="center",va="center",fontsize=12)
def arrow(x1,y1,x2,y2):
    a=FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="->",mutation_scale=20,fc="black",ec="black")
    ax.add_patch(a)
    
box(1,6,3,1,"1. Fetching the audio using yt-dlp & FFmpeg")#this is for the pipeline 
box(1,4,3,1,"2. Clip the audio from the huge audio")
box(1,4,3,1,"3. Transcribe usng Whisper's model sizes")
box(1,2,3,1,"4. Evaluate using the metrics")
arrow(2.5,6,2.5,5)
arrow(2.5,4,2.5,3)
arrow(2.5,2,2.5,1)

box
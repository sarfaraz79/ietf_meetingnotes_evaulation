#external libraries used in this file 
#[1] matplotlib
#author: John D. Cook
#title: matplotlib Python library
#url: https://matplotlib.org/stable/users/installing/index.html

import csv
import matplotlib.pyplot as plt

def main():
    results=load_rows("data/raw-data/top_5_groups.csv")
    results.sort(key=lambda x:(x["area"],x["rank"]))
    labels=[f"{row['group_acronym']} ({row['group_name']})" for row in results]
    counts=[row["active_draft_count"] for row in results]
    areas=sorted(set(row["area"] for row in results))
    colour_map=plt.get_cmap("tab10")
    colour=[colour_map[row["area"]] for row in results]
    fig,ax=plt.subplots(figsize=(10,6))
    ax.barh(range(len(results)),counts,color=colour)
    ax.set_yticks(range(len(results)))
    ax.set_yticklabels(labels)
    ax.set_xlabel("Active Draft Count")
    ax.set_title("Top 5 Working Groups by Area")
    plt.tight_layout()
    plt.savefig("/plottings/top_5_groups.pdf")
    plt.close(fig)
    
def load_rows(filename):
    rows=[]
    with open(filename) as csvfile:
        for row in csv.DictReader(csvfile):
            row["active_draft_count"]=int(row["active_draft_count"])
            rows.append(row)
    return rows
if __name__=="__main__":
    main()
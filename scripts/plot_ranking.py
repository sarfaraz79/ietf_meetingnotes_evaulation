#plotting the results using matplotlib

#student id :250032532

#What i am doing here is reading the comparison table and plotting the results using matplotlib

#External Libraries used in this file :
#[1]Matplotlib
# Author : John D. Hunter
#Title : Matplotlib

#[2]Numpy
# Author : Travis E. Oliphant et al.
#Title : Numpy

#Python
#URL : https://matplotlib.org
#URL : https://numpy.org 

import csv
import os
import matplotlib.pyplot as plt#[1]matplotlib
import numpy as np#[2]numpy
os.makedirs("plottings", exist_ok=True)
BLUE= "#1f77b4"
ORANGE= "#ff7f0e"
RED= "#d62728"
GREEN= "#2ca02c"

plt.rcParams.update({
    "font.size": 12,
    "font.family": "sans-serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

def main():
    all_rows=load_data()
    print("Total number of Working groups", len(all_rows))
    plot_scatter(all_rows)
    plot_top20_drafts(all_rows)
    plot_top20_attendance(all_rows)
    plot_coverage(all_rows)
    plot_top10_divergence(all_rows)
    

    
#helper methods

def load_data(filepath="data/processed-data/comparison_table.csv"):
    rows=[]
    with open(filepath, "r") as csvfile:    
        reader=csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)

    return rows
    
def to_int(value,fallback=0):#converting string to int and if it fails return the fallback value
    try:
        return int(value)
    except(ValueError,TypeError):
        return fallback
    
def to_float(value,fallback=0.0):#converting string to a float and if it fails return the fallback value
    try:
        return float(value)
    except(ValueError,TypeError):
        return fallback
    
def has_valid_rank(row,field):
    return row.get(field) not in ("N/A", "", None)#will give true if the rank field has a real number

#scatter plot for draft rank vs attendance rank
def plot_scatter(rows):
    valid_rows=[row for row in rows if has_valid_rank(row,"draft_rank") and has_valid_rank(row,"attendance_rank") and to_float(row["avg_attendance"]) > 0.0]
    if not valid_rows:
        print("No valid rows for scatter plot.")
        return
    x=[to_int(row["draft_rank"]) for row in valid_rows]
    y=[to_int(row["attendance_rank"]) for row in valid_rows]
    fig, ax=plt.subplots(figsize=(10,9))
    ax.scatter(x,y, color=BLUE, alpha=0.7)
    for r in sorted(valid_rows, key=lambda r: to_int(r["draft_rank"]))[:134]:# labelling the top 25 groups based on draft rank
        ax.annotate(r["group_acronym"], (to_int(r["draft_rank"]), to_int(r["attendance_rank"])), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)
    max_rank=max(max(x), max(y))
    ax.plot([1, max_rank], [1, max_rank], color=RED, linestyle="--", linewidth=1, label="y=x")
    ax.set_xlabel("Draft Rank")
    ax.set_ylabel("Attendance Rank")
    ax.set_title("Draft Rank vs Attendance Rank")
    ax.legend()
    ax.invert_yaxis()  # Invert y-axis to have rank 1 at the top
    ax.invert_xaxis()  # Invert x-axis to have rank 1 at the left
    plt.tight_layout()
    plt.savefig("plottings/draft_vs_attendance_scatter.png", dpi=300)
    plt.close(fig)
    print("Scatter plot saved as 'plots/draft_vs_attendance_scatter.png'")
    
#method  plotting the top 20 groups by active drafts
def plot_top20_drafts(rows):
    ranked=sorted([row for row in rows if has_valid_rank(row,"draft_rank")], key=lambda r: to_int(r["draft_rank"]))[:20]
    if not ranked:
        print("No valid rows for top 20 drafts plot.")
        return
    fig,ax=plt.subplots(figsize=(10,9))
    bars=ax.barh(range(len(ranked)), [to_int(row["active_drafts"]) for row in ranked], color=ORANGE, alpha=0.7)
    ax.set_yticks(range(len(ranked)))
    ax.set_yticklabels([row["group_acronym"]for row in ranked])
    ax.invert_yaxis()  # Invert y-axis to have the highest rank at the top
    
    for bar,row in zip(bars,ranked):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,f"{to_int(row['active_drafts'])}", va='center', fontsize=8)
    ax.set_xlabel("Number of Active Drafts")
    ax.set_title("Top 20 Working Groups by Active Drafts")
    plt.tight_layout()
    plt.savefig("plottings/top20_active_drafts.png", dpi=300)
    plt.close(fig)
    print("Top 20 active drafts plot saved as 'plots/top20_active_drafts.png'")
    
#method for top 20 by average attendance
def plot_top20_attendance(rows):
    ranked=sorted([row for row in rows if has_valid_rank(row,"attendance_rank") and to_float(row["avg_attendance"]) > 0.0], key=lambda r: to_int(r["attendance_rank"]))[:20]
    if not ranked:
        print("No valid rows for top 20 attendance plot.")
        return
    fig,ax=plt.subplots(figsize=(10,9))
    bars=ax.barh(range(len(ranked)), [to_float(row["avg_attendance"]) for row in ranked], color=GREEN, alpha=0.7)
    ax.set_yticks(range(len(ranked)))
    ax.set_yticklabels([row["group_acronym"]for row in ranked])
    ax.invert_yaxis()  # Invert y-axis to have the highest rank at the top
    for bar,row in zip(bars,ranked):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,f"{to_float(row['avg_attendance']):.2f}", va='center', fontsize=8)
    ax.set_xlabel("Average Attendance")
    ax.set_title("Top 20 Working Groups by Average Attendance")
    plt.tight_layout()
    plt.savefig("plottings/top20_average_attendance.png", dpi=300)
    plt.close(fig)
    print("Top 20 average attendance plot saved as 'plots/top20_average_attendance.png'")
    
#method for coverage gap
def plot_coverage(rows):
    #total_groups=len(rows)
    groups_without_session=sum(1 for row in rows if row["had_session"] == "False")
    groups_without_bluesheet=sum(1 for row in rows if row["had_session"] == "True" and row["bluesheet_found"] == "False")
    valid_groups_with_bluesheet=sum(1 for row in rows if  row["bluesheet_found"] == "True")
    names=["Never had session", "Had session but no bluesheet", "Had session and bluesheet"]
    values=[groups_without_session, groups_without_bluesheet, valid_groups_with_bluesheet]
    colours=[RED, ORANGE, GREEN]
    fig,ax=plt.subplots(figsize=(10,9))
    bars=ax.bar(names, values, color=colours, alpha=0.7)
    for bar,value in zip(bars,values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f"{value}", ha='center', fontsize=8)
    ax.set_ylabel("Number of Working Groups")
    ax.set_title("Coverage Gap: Working Groups with vs without Bluesheet")
    plt.tight_layout()
    plt.savefig("plottings/coverage_gap_bar.png", dpi=300)
    plt.close(fig)
    print("Coverage gap bar chart saved as 'plots/coverage_gap_bar.png'")
    #labels=["With Bluesheet","Without Bluesheet"]

#method ofr top 10 most divergent groups
def plot_top10_divergence(rows):
    both_ranked=[row for row in rows if has_valid_rank(row,"draft_rank") and has_valid_rank(row,"attendance_rank") and to_float(row["avg_attendance"]) > 0.0]
    most_divergent=sorted(both_ranked, key=lambda r: abs(to_int(r["draft_rank"]) - to_int(r["attendance_rank"])), reverse=True)[:10]
    if not most_divergent:
        print("No valid rows for top 10 divergence plot.")
        return
    acronyms=[row["group_acronym"] for row in most_divergent]
    draft_ranks=[to_int(row["draft_rank"]) for row in most_divergent]
    attendance_ranks=[to_int(row["attendance_rank"]) for row in most_divergent]
    x_positions=np.arange(len(acronyms))
    width=0.35
    fig,ax=plt.subplots(figsize=(10,9))
    ax.bar(x_positions - width/2, draft_ranks, width, label="Draft Rank", color=BLUE, alpha=0.7)
    ax.bar(x_positions + width/2, attendance_ranks, width, label="Attendance Rank", color=ORANGE, alpha=0.7)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(acronyms)
    ax.set_ylabel("Rank")
    ax.set_title("Top 10 Most Divergent Working Groups by Rank Difference")
    ax.legend()
    ax.invert_yaxis()  # Invert y-axis to have rank 1 at the top
    plt.tight_layout()
    plt.savefig("plottings/top10_divergent_groups.png", dpi=300)
    plt.close(fig)
    print("Top 10 divergent groups plot saved as 'plots/top10_divergent_groups.png'")
    
if __name__ == "__main__":
    main()

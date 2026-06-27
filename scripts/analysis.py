#using the standard python library for this file
#read the active drafts collected and find the top 3 working groups in the area

import csv
from collections import defaultdict

def main():
    read_csv=load_rows("data/raw-data/drafts_by_wg_and_area_in_descending_order.csv")
    by_area=defaultdict(list)#allows populating a list for each area without checking if the key exits
    for row in read_csv:
        by_area[row["area"]].append(row)#append the row to the lists for hte area
        list=[]#this is used to hold the list for each area
        for area,rows in by_area.items():
            groups.sort(key=lambda x:x["active_draft_count"],reverse=True)#sort the groups by active draft count
            top_5_groups=groups[:5]
            for rank,group in enumerate(top_5_groups,1):
                list.append({"area":area,"rank":rank,"group_acronym":group["group_acronym"],"group_name":group["group_name"],"active_draft_count":group["active_draft_count"]})
                with open("data/raw-data/top_5_groups.csv","w",newline="") as csvfile:#results to csv
                    fieldnames=["area","rank","group_acronym","group_name","active_draft_count"]
                    writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(list)
                write_csv(by_area,list)#this will write a text file for the top 5 groups in each area
                print(f"{len(by_area)} areas found and {len(list)} groups are on the list")

def write_csv(by_area,list):
    lines=[]#collect the output in this list
    lines.append("Top 5 working groups in each area\n")
    lines.appent("-"*50)
    for area in sorted(by_area):
        lines.appent("")
        lines.appent(f"Area: {area}")
        this_area=[group for group in list if group["area"]==area]#filter the list for this area
        for group in this_area:
            lines.append(f"Rank: {group['rank']}, Group: {group['group_acronym']} ({group['group_name']}), Active Drafts: {group['active_draft_count']}")
        textfile.write("\n".join(lines))
    with open("data/processed-date/top_5_groups.txt","w") as textfile:
        textfile.write(textfile)
        print(textfile)
        

#helper method to read the csv to a list
def load_rows(filename):
    rows=[]#empty list
    with open(filename) as csvfile:
        for row in csv.DictReader(csvfile):
            row["active_draft_count"]=int(row["active_draft_count"])
            rows.append(row)
        return rows
    
if __name__=="__main__":
    main()
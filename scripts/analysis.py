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
                
    
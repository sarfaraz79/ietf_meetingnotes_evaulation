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
    
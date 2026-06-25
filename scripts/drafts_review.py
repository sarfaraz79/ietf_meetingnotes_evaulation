# collecting active drafts per working group and their status

#Student ID : 250032532

#External Libraries used in this file :

#[1]ietf data
#Author : Colin Perkins
#Title : ietfdata- Python library for accessing IETF Datatracker data
#version : 0.8.1
#Type : python library 
#URL : https://github.com/glasgow-ipl/ietfdata

import csv
from datetime import datetime,timezone

#[1]ietfdata — DataTracker with  caching
import ietfdata
from ietfdata.datatracker import DataTracker
#from ietfdata.dt_backend import DTBackendArchive

USE_SQLITE = False
if USE_SQLITE:
    from ietfdata.dt_backend import DTBackendArchive
    tracker = DataTracker(DTBackendArchive("ietfdata.sqlite"))
else:
    tracker = DataTracker(cache_dir="dt_cache")

def main():
   # tracker = DataTracker(cache_dir="dt_cache") #[1]ietfdata — DataTracker with  caching
    active_state=tracker.group_state_from_slug("active")#[1]ietfdata — DataTracker with  caching
    draft_type=tracker.document_type_from_slug("draft")#[1]ietfdata — DataTracker with  caching
    ietf_streaming  = tracker.stream_from_slug("ietf")#[ietfdata — DataTracker with  caching] this will limit results to wf-stream drafts and excludes individual submissions and other non wg draft
    right_now = datetime.now(timezone.utc)
    results=[]
    for group in tracker.groups(state=active_state): #[1]ietfdata groups() will iterate over all groups matching the given state
        if "/grouptypename/wg/" not in str(group.type):# skip the non working group entries like areas teams research etc
            continue  
        #finding the parent area name for the working group
        area_name=""
        if group.parent:
            parent_group=tracker.group(group.parent)#[1]ietfdata using the group()
            if parent_group:
                area_name=parent_group.acronym
#now to count the active draftsfor the group 
        active_draft_count=0
        for document in tracker.documents(doctype=draft_type, stream=ietf_streaming, group=group):#[1]ietfdata using documents() which fetches the documents
            if document.rfc_number is not None:#skip the drafts if they are already published as RFC's
                continue
            if not document.expires:#skip the drafts with no expiry date
                continue
            try: #checking the draft which has not expired yet
                expiry_date = datetime.fromisoformat(str(document.expires))
                if expiry_date.tzinfo is None:
                    expiry_date = expiry_date.replace(tzinfo=timezone.utc)
                if expiry_date >right_now:
                    active_draft_count+= 1
            except (ValueError, TypeError):
                continue
        print(f"{group.acronym:20s} area: {area_name:6s} active drafts: {active_draft_count}")
        results.append({#appending the results
        "group_acronym"  : group.acronym,
        "group_full_name": group.name,
        "area"           : area_name,
        "active_drafts"  : active_draft_count,
        })
    results.sort(key=lambda x: x["active_drafts"], reverse=True) #sorting the results based on active drafts count
    with open("data/raw-data/active_drafts.csv","w", newline="") as output_file:
            columns = ["group_acronym", "group_full_name", "area", "active_drafts"]
            writer  = csv.DictWriter(output_file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(results)
            
    print(f"\nResults written to active_drafts.csv")
    print(f"Total working groups processed: {len(results)}")
    print(f"Total working groups with active drafts: {sum(1 for r in results if r['active_drafts'] > 0)}")
    print(f"Total active drafts across all working groups: {sum(r['active_drafts'] for r in results)}")
    print(f"Average active drafts per working group: {sum(r['active_drafts'] for r in results) / len(results):.2f}")
    print(f"Working group with the most active drafts: {max(results, key=lambda x: x['active_drafts'])['group_acronym']} ({max(results, key=lambda x: x['active_drafts'])['active_drafts']} drafts)")
    print(f"Working group with the least active drafts: {min(results, key=lambda x: x['active_drafts'])['group_acronym']} ({min(results, key=lambda x: x['active_drafts'])['active_drafts']} drafts)")
    print(f"Number of working groups with no active drafts: {sum(1 for r in results if r['active_drafts'] == 0)}")
    print("Top 10 by active draft count:")
    for row in results[:10]:
        print(f" {row['group_acronym']:20s} {row['active_drafts']:3d} drafts  ({row['group_full_name']})")
    
if __name__ == "__main__":
    main()
        
    
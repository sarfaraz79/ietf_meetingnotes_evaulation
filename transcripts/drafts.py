#Student ID: 250032532
#Libraries used in this file:
#[1] ietfdata
#Author: Colin Perkins
#Title: ietfdata Python library
#URL: https://github.com/glasgow-ipl/ietfdata

import csv
from datetime import datetime,timezone
from ietfdata.datatracker import DataTracker

USE_SQLITE = False

if USE_SQLITE:
    from ietfdata.dt_backend import DTBackendArchive
    tracker = DataTracker(DTBackendArchive("ietfdata.sqlite"))
else:
    tracker = DataTracker(cache_dir="dt_cache")

#DATATRACKER = "https://datatracker.ietf.org"

def main():
    drafts_which_are_active=tracker.group_state_from_slug("active")#groups which are active
    type_of_drafts=tracker.document_type_from_slug("draft")#type of document
    ietf_filter=tracker.stream_from_slug("ietf")#only counting the working group drafts
    right_now=datetime.now(timezone.utc)#using the current time zone so as to compare with the current drafts
    results=[]
    
    for group in tracker.groups(state=drafts_which_are_active):
        if "/grouptypename/wg/" not in str(group.type):#if it's not a working group will skip
            continue
        area_name=""
        if group.parent:#parent is the area
            area_group=tracker.group(group.parent)#fetch the area
            if area_group:
                area_name=area_group.acronym#use the parent acronym as the area
            active_draft_count=0#count for the group's active drafts
            for document in tracker.documents(doctype=type_of_drafts,stream=ietf_filter,group=group):
                    if document.rfc_number is not None:#if the draft has an RFC number it is not active
                        continue
                    if not document.expires:#if the draft has no expiry date it is not active
                        continue
                    try:
                        expiry_date=datetime.fromisoformat(document.expires)#convert the expiry date to a datetime object
                        if expiry_date.tzinfo is None:#if the expiry date has no timezone info, assume UTC
                            expiry_date=expiry_date.replace(tzinfo=timezone.utc)
                        if expiry_date>right_now:#if the expiry date is in the future it is active
                            active_draft_count+=1
                    except (ValueError,TypeError):
                        continue
        results.append({"group_acronym":group.acronym,"group_name":group.name,"area":area_name,"active_draft_count":active_draft_count})#append the group acronym, area acronym and active draft count to the results list  
    results.sort(key=lambda x: x["active_draft_count"],reverse=True)#sort the results by active draft count
    with open("data/raw-data/drafts_by_area.csv","w",newline="") as csvfile:#write the results to a csv file
        fieldnames=["group_acronym","group_name","area","active_draft_count"]
        writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        #for row in results:
        writer.writerows(results)
    print("Drafts by area data written to data/raw-data/drafts_by_area.csv")
    
if __name__=="__main__":
    main()
                        
            
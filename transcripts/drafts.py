#Student ID: 250032532
#Libraries used in this file:
#[1] ietfdata
#Author: Colin Perkins
#Title: ietfdata Python library
#URL: https://github.com/glasgow-ipl/ietfdata

import csv
from datetime import datetime,timezone
from pickle import FALSE
import ietfdata 
from ietfdata.datatracker import DataTracker

USE_SQLITE=FALSE
if USE_SQLITE:
    from ietfdata.dt_backend import DTBackendArchive
    tracker=DataTracker(DTBackendArchive("ietfdata.sqlite"))
else:
    tracker=DataTracker(cache_dir="dt_cache")

def main():
    drafts_which_are_active=tracker.group_state_from_slug("active")#groups which are active
    type_of_drafts=tracker.document_type_from_slug("draft")#type of document
    ietf_filter=tracker.stream_from_slug("ietf")#only counting the working group drafts
    right_now=datetime.now(timezone.utc)#using the current time zone so as to compare with the current drafts
    results=[]
    
    for group in tracker.grouups(state=drafts_which_are_active):
        if "/grouptypename/wg/" not in str(group.type):#if it's not a working group will skip
            continue
        area_name=""
        if group.area:#parent is the area
            area_group=tracker.group(group.area)#fetch the area
            if area_group:
                area_name=area_group.acronym#use the parent acronym as the area
                active_draft_count=0#count for the group's active drafts
                for document in tracker.documents(document_type=type_of_drafts,stream=ietf_filter,group=group):
                    if document.rfc_number is not None:#if the draft has an RFC number it is not active
                        continue
                    if not document.expires:#if the draft has no expiry date it is not active
                        continue
                    try:
                        expiry_date=datetime.fromisoformat(str(document.expires))#convert the expiry date to a datetime object
                        if expiry_date.tzinfo is None:
                            expiry_date=expiry_date.replace(tzinfo=timezone.utc)#if the expiry date has no timezone,assume UTC
                            if expiry_date>right_now:
                                active_draft_count+=1#if the expiry date is in the future,lets count it as active
                        except(ValueError,TypeError):
                            continue
                        
            
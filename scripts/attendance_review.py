#Collecting the session attendance data

#Student ID : 250032532

#External Libraries used in this file :

#ietf data
#Author : Colin Perkins
#Title : ietfdata- Python library for accessing IETF Datatracker data
#version : 0.8.1
#Type : python library 
#URL : https://github.com/glasgow-ipl/ietfdata

#requests
#Author : Kenneth Reitz
#Title : Requests: HTTP for humans
#Version : 2.33.1
#Type : Python library 
#URL : https;//requests.readthedocs.io

#IETF Datatracker API
#Publisher : IETF
#Title : IETF Datatracker API
#TYpe : API
#URL : https://datatracker.ietf.org/api/v1/



"""This script is used to find the last N ietf meetingd which are completed . For each meeting ,
it finds every working group which had a session and fetches the bluehseet for each session and counts atendees
It will aggregate across the meetings per group : how many meetings did they attend , what was the attendee count over the sessions , and the
average attendance of the session . and it saves it to raw_attendance.csv.
The metric being used here is avg_attendance_per_session because it will normalise how often the groups meet. """

import argparse 
import csv 
import re
from datetime import date 
import requests 
from ietfdata.datatracker import DataTracker

DATATRACKER = "https://datatracker.ietf.org"

#main method
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--num_meetings", type=int, default=3,
        help="How many recent IETF meetings to look into"
    )
    args = parser.parse_args()
    #[1]ietfdata — DataTracker with  caching
    tracker = DataTracker(cache_dir="dt_cache") 
    active_state=tracker.group_state_from_slug("active")

#finding the last completed meetings
    meetings_to_check = get_last_n_meetings(tracker, args.num_meetings)
    
#for each of the meeting will record the sessions 
    sessions_per_meeting = {}
    for meeting in meetings_to_check:
        print(f"\nFetching the sessions for ietf {meeting.number}")
        groups_that_met = get_groups_with_sessions(tracker, meeting)
        sessions_per_meeting[meeting.number] = groups_that_met
        print(f"{len(groups_that_met)} groups had the  sessions")
        
#for each of the working group , collect the attendance data
    raw_data = {}
    for group in tracker.groups(state=active_state):
        if "/grouptypename/wg/" not in str(group.type):# Skip whichever is not a working group
            continue
        group_uri = str(group.resource_uri)
        raw_data[group.acronym] ={} #well start with an empty reocrd
        for meeting in meetings_to_check:#check through eahc meeting
            had_session = group_uri in sessions_per_meeting[meeting.number]
            if not had_session:
                # Group which didnt't meet at the IETF will recorded as none
                raw_data[group.acronym][meeting.number] = None
            else:
                count =get_attendee_count(meeting.number, group.acronym)# the gorup has a session and we fetch atendee count
                raw_data[group.acronym][meeting.number] =count
                status = f"{count} attendees" if count is not None else "bluesheet is missing"
                print(f"{group.acronym:20s} IETF {meeting.number}:{status}")
                
#this will aggregate per group for the meetings
    results = []
    meeting_numbers =[m.number for m in meetings_to_check]
    for group_acronym, meeting_data in raw_data.items():
        sessions_attended = sum(# Count the meetings the group attended
            1 for count in meeting_data.values()
            if count is not None  # None means no session, so no counting of it
        )
        # Sum up the total attendees across all sessions we have data for
        # (only for the  sessions where we got a real bs count)
        sessions_with_bluesheet = [
            count for count in meeting_data.values()
            if count is not None and count > 0
        ]
        total_attendees = sum(sessions_with_bluesheet)
        bluesheet_count = len(sessions_with_bluesheet)# how many bluesheets we fhave found
        
#using the average attendance as the metric 
        if bluesheet_count > 0:
            avg_attendance = round(total_attendees / bluesheet_count, 1)
        else:
            avg_attendance = 0.0  # if there is no bluesheet
        results.append({
            "group_acronym" : group_acronym,
            "meetings_checked" : len(meetings_to_check),#how many meetings to check 
            "sessions_attended": sessions_attended,# how many they showed up to
            "sessions_with_bluesheet": bluesheet_count,# how many we got data for
            "total_attendees": total_attendees,#sum across all sessions
            "avg_attendance" : avg_attendance,# ranking metric
        })
#sorting by the average attendance
    results.sort(key=lambda r:r["avg_attendance"],reverse=True)
    
#now  save the data received to a csv file 
    with open("attendance_raw.csv", "w", newline="") as output_file:
        columns = ["group_acronym", "meetings_checked","sessions_attended","sessions_with_bluesheet","total_attendees","avg_attendance"]
        writer = csv.DictWriter(output_file,fieldnames=columns )
        writer.writeheader()
        writer.writerows(results)
    
    never_met   = sum( 1 for r in results if r["sessions_attended"] == 0)
    valid_data  = sum(1 for r in results if r ["avg_attendance"] > 0)
    
    print(f"\n Saved_attendance_raw.csv")
    print(f"  Meetings checked             : {len(meetings_to_check)} (IETF {','.join(meeting_numbers)})")
    print(f"  Total active working groups  : {len(results)}")
    print(f"  Never met in any meeting     : {never_met}")
    print(f"  Groups with valid avg data   : {valid_data}")
    print( f"\nTop 10 meetings by average attendance:")
    for r in results[:10] :
        print( f"  {r['group_acronym']:20s}  avg: {r['avg_attendance']:6.1f}  "
              f"({r['sessions_attended']}/{len( meetings_to_check)} meetings attended)")

    
    
#### Helper functions ##

#helper method to downlaod the json from the datatracker API 
def download_json(url_path, extra_filters=None): #this will download the data from the datatracker and will return it as json
    params = {"format": "json"}
    if extra_filters:
        params.update(extra_filters)
    response = requests.get(DATATRACKER + url_path, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

#helper method to get all the groups which had a session in a meeting

def get_groups_with_sessions(tracker, meeting):
    #[1] ietfdata — method namesd meeting_sessions() 
    groups_that_met =set() #will return a set of URI for groups that had a sessio in the meeting
    for session in tracker.meeting_sessions(meeting=meeting):
        if session.group:
            groups_that_met.add(str(session.group))
    return groups_that_met


#helper method to get the last completed ietf meetings

def get_last_n_meetings(tracker, how_many):
    #[1]ietfdata—meeting_type_from_slug and meetings() methods
    ietf_type = tracker.meeting_type_from_slug("ietf")
    all_meetings = sorted(tracker.meetings(meeting_type=ietf_type),key=lambda m: m.date,reverse=True)
    today = date.today()
    completed_meetings =[m for m in all_meetings if m.date < today]
    selected= completed_meetings[:how_many]
 
    print(f" By Looking at the last {len(selected)} IETF meetings which are completed :")
    for m in selected:
        print(f"IETF {m.number} — {m.city},{m.date}")
 
    return selected # will return a list of the last completed meetings sorted with the newest at first .
# looking a multiple meetings instead og just one because the wg might skip an IETF meeting but can be active so 
# averaging across meetings gives a fairer attendance picture

#helper method to get the atendee count for a session of a group in a meeting
def get_attendee_count(meeting_number, group_acronym):
    """
    Finds and reads the bluesheet for a group at a specific meeting.
    Bluesheets are published by the IETF Datatracker [IETF Datatracker API]
    as text files. Their header contains text like "161 attendees".
    Returns the count as an integer, or None if not found.
    """
    #[IETF Datatracker API]— search for bluesheet document by name 
    search = download_json(
        "/api/v1/doc/document/",
        {"name__startswith": f"bluesheets-{meeting_number}-{group_acronym}-",
         "limit": 5}
    )
    if not search["objects"]:
        return None
    bluesheet_document=search["objects"][0]
    filename = bluesheet_document.get("uploaded_filename", "")# Try  with the uploaded filename path 
    if filename:
        file_url = (f"https://www.ietf.org/proceedings/{meeting_number}"
                    f"/bluesheets/{filename}")
        #[2]Requests — used to download the bluesheet text file
        response = requests.get(file_url, timeout=30)
        if response.status_code ==200:
            count = parse_attendee_count(response.text)
            if count is not None:
                return count

    url_list = download_json( #Fall back to the document URL list
        "/api/v1/doc/documenturl/",
        {"doc": bluesheet_document["resource_uri"],"limit": 10}
    )
    for entry in url_list.get("objects", []):
        link = entry.get("url", "")
        if link.endswith(".txt"):
            # 2] Requests— used to download the bluesheet text file
            response = requests.get(link, timeout=30)
            if response.status_code == 200:
                count = parse_attendee_count(response.text)
                if count is not None:
                    return count
    return None
 
 ##this method will parse the bluesheet text to find the attendee count
def parse_attendee_count(bluesheet_text):
    match =re.search(r"(\d+)\s+attendees?", bluesheet_text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

if __name__ == "__main__":
    main()
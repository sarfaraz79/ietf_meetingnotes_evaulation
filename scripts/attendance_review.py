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
from ietf.datatracker import DataTracker

DATATRACKER = "https://datatracker.ietf.org"

#main method
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--num_meetings", type=int, default=3,
        help="How many recent IETF meetings to look into"
    )
    args = parser.parse_args()
    tracker = DataTracker(cache_dir="dt_cache")
    active_state=tracker.group_state("active")

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
                
#well aggregate per group for the meetings
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

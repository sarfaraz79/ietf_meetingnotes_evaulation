#Collecting the session attendance data

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
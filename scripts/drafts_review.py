# collecting active drafts per working group and their status

#Student ID : 250032532

#External Libraries used in this file :

#ietf data
#Author : Colin Perkins
#Title : ietfdata- Python library for accessing IETF Datatracker data
#version : 0.8.1
#Type : python library 
#URL : https://github.com/glasgow-ipl/ietfdata

import csv
from datetime import datetime,timezone

#[1]ietfdata — DataTracker with  caching
from ietfdata.datatracker import DataTracker

def main():
    
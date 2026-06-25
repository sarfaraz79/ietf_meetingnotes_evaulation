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
    tracker=DataTracker(cache_dir="ietfdata_cache")
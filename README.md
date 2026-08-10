# Dataset Selection for IETF pipeline

This folder is for the dataset selection of the IETF working groups before entering the transcription pipeline.

# Prerequisites

## Python version
 Requires python version 3.8 and above

 ## Virtual Environment Setup

### macOS
 python3 -m venv venv
 source venv/bin/activate

 ### Windows
 python -m venv venv
 venv\scripts\activate

 ### install dependencies
 pip install -r requirements.txt

 # Pipeline Execution
 ## Collect raw data
 python3 scripts/drafts.py

 Fetches active working groups and active drafts from ietf datatracker 

 ## For analysis
 python3 scripts/analysis.py
 
 Filters the draft data and picks top 5 working groups of area and produces csv

 ## Plot generation
 python3 scripts/plot.py

Creates bar chart by area of the analyzed and clean dataset

# Output files

drafts_by_wg_and_area_in_descending_order.csv - raw output containing all active working groups and drafts

top_5_groups.csv - csv containing top 5 working groups

top_5_groups.txt - text summary containing groups, ranks by area

top_5_groups.pdf - horizontal bar chart of the analyzed groups
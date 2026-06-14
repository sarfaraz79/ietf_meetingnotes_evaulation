##Analyze and comparing the two rankings

#Student ID : 250032532

#External Libraries used in this file :
#[1]Scipy
# Author : Pauli Virtanen , Ralf Gommers, Travis E. Oliphant et al.
#Title : Scipy

#Python
#URL : https://scipy.org

#I am using the spearman rank corelation 
#scipy.stats.sperman[1]


import csv
from scipy.stats import spearmanr#[1]Scipy

def main():
    attendee_counts,had_session_map,bluesheet_map=load_attendance_data("raw_attendance.csv")
    draft_counts,full_name,areas=load_draft_data
    
    valid_attandance={group:count #using the attendance data where the real bluesheet is present
                      for group,count in attendee_counts.items()
                      if had_session_map.get(group)
                      and bluesheet_map.get(group)
                      and count > 0.0}
    
    attendance_ranks = assign_ranks(valid_attandance)
    draft_ranks=assign_ranks(draft_counts)
    all_groups=set(draft_counts)|set(attendee_counts)
    groups_in_both=set(valid_attendance)&set(draft_counts)
    groups_with_no_session={g for g, had in had_session_map.items() if not had}
    
    #calcuting the spearman rank correlation coefficient
    #in spearman we measure two similar rankings . rho = 1 means identical and rho = 0 means there's no relationship 
    if len(groups_in_both) >= 2:
        shared_groups = sorted(groups_in_both)
        attendance_ranks_list = [attendance_ranks[g] for g in shared_groups]
        draft_ranks_list = [draft_ranks[g] for g in shared_groups]
        rho, p_value = spearmanr(attendance_ranks_list, draft_ranks_list)
    else:
        rho, p_value = None, None
    
#building the comparison table


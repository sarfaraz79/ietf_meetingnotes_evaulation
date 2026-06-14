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
    comparison_table=[]
    for group in sorted(all_groups):
        comparison_table.append({
            "group_acronym": group,
            "group_full_name": full_name.get(group, ""),
            "area": areas.get(group, ""),
            "active_drafts": draft_counts.get(group, 0),
            "draft_rank": draft_ranks.get(group, "N/A"),
            "avg_attendance": attendee_counts.get(group, 0.0),
            "attendance_rank": attendance_ranks.get(group, "N/A"),
            "had_session": had_session_map.get(group, False),
            "bluesheet_found": bluesheet_map.get(group, False),
        })
    comparison_rows.sort(key=lambda x: (x["draft_rank"] if x["draft_rank"] is not None else float('inf')) else 9999)
    with open("rankings_comparison.csv", "w", newline="") as f:
        columns = ["group_acronym", "group_full_name", "area", "active_drafts", "draft_rank", "attendance_rank", "had_session", "bluesheet_found"]
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(comparison_rows)
        
#now findign the top 10 most divergent groups based on the difference in ranks
    groups_with_both = [row for row in comparison_rows if  isinstance(row["draft_rank"], int) is not None and isinstance(row["attendance_rank"], int)]
    most_divergent=sorted(groups_with_both, key=lambda x: abs(x["draft_rank"] - x["attendance_rank"]), reverse=True)[:10]
    
#create a txt file to write the comparisions in findings.txt

    divider="-"*55
    lines = [ "COMPARISON OF RANKINGS", divider , "SUMMARY OF SPEARMAN RANK CORRELATION", divider, f"total active WG's: {len(all_groups)}", f"attended >= 1 mtg : {sum(had_session_map.values())}", f"WG's with no session: {len(groups_with_no_session)}", f" had sessions, no bluesheet : {sum(1 for g in had_session_map if had_session_map[g] and not bluesheet_map.get(g))}", f" valid attendance entries : {len(valid_attendance)}",f" valid draft entries : {len(draft_counts)}",f" overlap (in both rankings) : {len(groups_in_both)}",
             divider, "CORRELATION",divider,f" rho = {f'{rho:.3f}' if rho is not None else 'N/A'}",f" p = {f'{p_value:.4f}' if p_value is not None else 'N/A'}"]      
    if rho is not None:
        if rho > 0.7:
            interpretation = "strong agreement either metric probably ok for WG selection"
        elif rho > 0.4:
            interpretation = "moderate agreement notable divergence"
        else:
            interpretation = "weak agreement significant divergence"
        lines.append(f" interpretation : {interpretation}")
        
    lines += [divider, "TOP 10 MOST DIVERGENT GROUPS", divider
             f"  {'acronym':<20} {'drafts':>6}{'d.rnk':>6} {'avg.att':>8} {'a.rnk':>6} {'|diff|':>7}", f" {'-'*20}{'-'*6} {'-'*6} {'-'*8}{'-'*6} {'-'*7}" ]
    for row in most_divergent:
        difference = abs(row["draft_rank"] - row["attendance_rank"])
        lines.append(f"  {row['group_acronym']:<20} {row['active_drafts']:>6} {row['draft_rank']:>6} {row['avg_attendance']:>8.2f} {row['attendance_rank']:>6} {difference:>7}")
    lines += ["TOP 20 BY ACTIVE DRAFTS", divider, f"  {'acronym':<20} {'drafts':>6}{'d.rnk':>6} {'avg.att':>8} {'a.rnk':>6}", f" {'-'*20}{'-'*6} {'-'*6} {'-'*8}{'-'*6}" ,]
    for row in comparison_rows[:20]:
        lines.append(f"  {row['group_acronym']:<20} {row['active_drafts']:>6} {row['draft_rank']:>6} {row['avg_attendance']:>8.2f} {row['attendance_rank']:>6}")
    lines += ["","full data in rankings_comparison.csv"]
    findings_text="\n".join(lines)+"\n"
    with open("findings.txt", "w") as f:
        f.write(findings_text)
    print(findings_text)
    print("Comparison table written to rankings_comparison.csv")
    
 #helper method to load the attendance data from a CSV file   
def load_attendance_data(filepath="attendance_raw.csv"):
    attendee_counts= {}
    had_session_map= {}
    bluesheet_map = {}
    with open(filepath) as f:
        for row in csv.DictReader(f):
            acronym= row["group_acronym"]
            attendee_counts[acronym] = float(row["avg_attendance"])# avg_attendance = average attendees per session across multiple meetings
            had_session_map[acronym] = int(row["sessions_attended"]) > 0 # sessions_attended >0 means they met at least once
            bluesheet_map[acronym]   = int(row["sessions_with_bluesheet"]) > 0 #sessions_with_bluesheet > 0 means we have real attendance data
    return attendee_counts,had_session_map, bluesheet_map


    
if __name__ == "__main__":
    main()
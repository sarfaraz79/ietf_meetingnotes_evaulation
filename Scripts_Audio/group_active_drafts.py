import re
import os
import argparse
import requests

def group_filter(drafts,group_name):
    match=[]
    for draft in drafts:
        if f"-{group_name}-" in draft:
            match.append(draft)
    return match

def get_all_draft(page):
    pattern = r'href="/doc/(draft-[\w-]+)/(\d+)/"'
    matches=re.findall(pattern,page)
    all_drafts=[]
    for base_name,revision in matches:
        name=f"{base_name}-{revision}"
        all_drafts.append(name)
    return all_drafts

def download_draft(draft,output):
    url=f"https://www.ietf.org/archive/id/{draft}.txt"
    response=requests.get(url)
    if response.status_code==200:
        output_path=os.path.join(output,f"{draft}.txt")
        with open(output_path,"w") as f:
            f.write(response.text)
        return True
    else:
        return False

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--group",required=True,help="working group")
    parser.add_argument("--output",required=True,help="folder_to_save")
    args=parser.parse_args()
    os.makedirs(args.output,exist_ok=True)
    page_response=requests.get("https://datatracker.ietf.org/doc/active/")
    page_in_text=page_response.text
    all_draft=get_all_draft(page_in_text)
    group_draft=group_filter(all_draft,args.group)
    download_count=0
    for draft in group_draft:
        success=download_draft(draft,args.output)
        if success:
            download_count+=1
    
    print(f"downloaded {download_count} of {len(group_draft)} drafts to {args.output}")
    
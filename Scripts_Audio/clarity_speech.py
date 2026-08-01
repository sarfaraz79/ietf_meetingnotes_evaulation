import re
import argparse

def get_average_log_probability_from_file(debug_path):
    pattern=re.compile(r"avg_logprob=(-?[\d.]+)")
    logprob_list=[]
    with open(debug_path) as f:
        for line in f:
            match=pattern.search(line)
            if match:
                value=float(match.group(1))
                logprob_list.append(value)
    return logprob_list
    
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--debug_path",required=True)
    parser.add_argument("--clip_name",required=True)
    args=parser.parse_args()
    log_prob_list=get_average_log_probability_from_file(args.debug_path)
    if len(log_prob_list)==0:
        print(f"{args.clip_name}: No log probability values found in the debug file.")
    else:
        average_log_prob=sum(log_prob_list)/len(log_prob_list)
        print(f"{args.clip_name}: Average Log Probability = {average_log_prob:.4f}")
        
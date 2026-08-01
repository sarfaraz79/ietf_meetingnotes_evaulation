import numpy as np
from scipy.io import wavfile
import argparse

def estimated_snr(wav_path):
    sample_rate,audio=wavfile.read(wav_path)
    if len(audio.shape)>1:
        audio=audio.mean(axis=1)  # Convert to mono by averaging channels
    audio=audio.astype(np.float64)
    audio=audio/32768
    chunk_length=int(sample_rate*0.025)
    chunks_number=len(audio)//chunk_length
    loudness_list=[]
    for i in range(chunks_number):
        starting=i*chunk_length
        ending=starting+chunk_length
        chunk=audio[starting:ending]
        loudness=get_chunk_loudness(chunk)
        loudness_list.append(loudness)
    cutoff_silence=0.0001
    non_silent_loudness=[loudness for loudness in loudness_list if loudness>cutoff_silence]
    print(f"total chunks:{len(loudness_list)},non silent chunks:{len(non_silent_loudness)}")
    non_silent_loudness.sort()
    percentage=len(non_silent_loudness)//10
    if percentage==0:
        percentage=1
    chunks_quiet=non_silent_loudness[:percentage]
    chunks_loud=non_silent_loudness[-percentage:]
    noise_level=sum(chunks_quiet)/len(chunks_quiet)
    speech_level=sum(chunks_loud)/len(chunks_loud)
    ratio=speech_level/noise_level
    snr_db=20*np.log10(ratio)
    return snr_db
    
def get_chunk_loudness(chunk):
    squared=chunk**2
    mean_squared=np.mean(squared)
    loudness=np.sqrt(mean_squared)
    return loudness

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--audio",required=True)
    parser.add_argument("--clip_name",required=True)
    args=parser.parse_args()
    snr=estimated_snr(args.audio)
    print(f"{args.clip_name}: est Sound Noise Ratio = {snr:.1f} db")

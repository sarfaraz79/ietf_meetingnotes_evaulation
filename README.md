# Evaluating the accuracy of IETF meeting notes using Machine Transcription and Natural Language Processing

MSc dissertation, Univeristy of St Andrews

Student ID : 250032532

This codebase collects IETF audio from vidoe recordings, performs transcription on ten Whisper model Sizes under configurable settings and evaluates results against manually transcribed transcripts using various metrics

| Metric      |
| ----------- |
| Word Error Rate        |
| Terminology Retention  |
| SBERT                  |
| BERTSCORE              |

The codebase also includes mitigation techniques to improve WER, repeated runs, audio analysis and automated construction of glossaries.

## Installation of requirements

python3 -m venv .venv
source .venc/bin/activate
pip install -r requirements.txt

# Layout

clips/ - IETF audio clips
audio/ - Full length audio clips
transcription_manual/ - Manually produced transcripts
glossaries/ - automated and manually created glossaries

Scripts_Audio/Audio_Collection - Extraction and clipping of audio 

Scripts_Audio/CSV_Builder_Scripts - 
Building Master Results CSV's

Scripts_Audio/Glossary_Scripts - Comparing and creation of automated glossaries

Scripts_Audio/mitigation_techniques - mitigation techniques 

Scripts_Audio/semantic_similarity - Sentence BERT script

Scripts_Audio/Speech_Analysis - Signal to Noise and Finding Clarity in speech using avg log probability

Scripts_Audio/Terminology_Retention - Terminology Retention Script

Scripts_Audio/Transcript_Cleaning - Scripts to clean transcription of speaker names etc

Scripts_Audio/Whisper_Run_On_Audio - Whisper Script to run on audio clips

Scripts_Audio/Word_Error_Rate_Assessment - Word Error Rate Script

Scripts_Audio/group_active_drafts.py - To fetch active drafts from IETF

Scripts_Audio/terminology_density.py - For finding the % of technical terms in the audio clip

master_results/ - All results of Whisper models on models, WER, TRR, debug outputs, semantics, BERTF1 Score etc 

master_results_english/ - All results of Whisper models on models, WER, TRR, debug outputs, semantics, BERTF1 Score etc using forced English parameter

mitigation_results/ - Mitigation results on audio clips along with debug outputs

reproducibility_results/ - Results of 1250 whisper runs ( 25 runs per audio clip) on audio clips


# Whisper Models Evaluated

tiny 
tiny.en
base
base.en
small
small.en
medium
medium.en
large-v3
turbo

# Pipeline Run 

## Collect Audio
python3 Scripts_Audio/Audio_Collection/audio_fetching.py
--url <audio_url> --name <name_to_save_audio_file>

Clipping a segment from audio
python3 Scripts_Audio/Audio_Collection/short_clip_of_session.py
--input <audio_file> --start<start_time_of_clip>
--length<clip_length> --output<name_to_save_clip_file>

Transcription
python3 Scripts_Audio/Whisper_Run_On_Audio/whisper_transcription.py
--input <clip>
--model <whisper_model>
--output <where_to_save_result>

## Word Error Rate and Terminology Retention

### Word Error Rate
python3 Scripts_Audio/Word_Error_Rate_Assessment/WER_assessment.py
--reference <manually_transcripted_txt>
--hypothesis <whisper_transcript.txt>
--output <output_file>-wer.txt


 ### Terminology Retention
python3 Scripts_Audio/Terminology_Retention/TRR.py
--glossary <glossary_file>
--reference <manual_transcript.txt>
--hypothesis <whisper_transcript>
--output <output>_trr.txt


### Mitigation Techniques
python3 Scripts_Audio/mitigation_techniques/mitigation_technique.py
--input <audio_clip>
--model <Whisper_model>
--output <file_to_save_results>
--technique_label <testing_label>

The mitigation techniques names ’–no condition on previous text’, ’–no speech threshold’,
’–compression ratio threshold’, ’–logprob threshold’ can be added for the techniques to apply.

## SNR, Technical Density in Clip, Speech Clarity using Log Probability

### Signal to Noise
python3 Scripts_Audio/Speech_analysis/snr_ietf.py
--audio <clip> --clip_name <audio_clip_name>

### Technical Density of Clip
python3 Scripts_Audio/terminology_density.py
--reference <manual/automated_transcription>
--glossary <glossary_file>
--clip_name <clipname>

### Clarity of Speech
python3 Scripts_Audio/Speech_analysis/clarity_speech.py
--debug_path <debug_file>
--clip_name <clipname>

## Construction of Glossary 

### To fetch active drafts
python3 Scripts_Audio/group_active_drafts.py
--group <ietf_group>
--output <folder_to_save>

### To create automated glossary
python3 Scripts_Audio/Glossary_Scripts/glossary_automatic.py
--documents <drafts_ietf>
--output <output_file>


### To Compare manual and automated glossary
python3 Scripts_Audio/Glossary_Scripts/comparing_glossary.py
--manual <manual_glossary>
--automated <automated_glossary>
--reference <manual_transcript>

## Plotting of Results

### To Plot the reproducibility results
python3 reproducibility_plotting/csv_reproducibility_results.py

### To summarize reproducibility results
python3 reproducibility_plotting/interpret_results.py

### For the matplotlib charts 
cd Code_For_Diagrams
python3 Scripts_Diagrams/plots_all.py

### For Mitigation results plot
cd Code_For_Diagrams
python3 Scripts_Diagrams/plot_mitigation_results.py

## Batch Jobs

### Queue Check
squeue -u $USER

### For jobs requiring CPU
srun -p gpu-14-n3 -q gpu-14-n3 ---gpu 1 --cpus --cpus-per-task 8 --mem 48G --pty bash

# Experiment Scaling

| Experiment      |Runs|
| ----------- | ----------- |
| Master Results| 10 models * 5 audio sources |
|Forced English Master results| 10 models * 5 audio sources|
|Baseline Run for LibriSpeech| 6 models * 200 Libriscpeech clips |
|Mitigation Technqiues| 6 models * 5 techniques * 5 audio sources = 150 runs |
| Reproducibility results| 5 audio sources * 10 models * 25 repititions = 1250 runs|

# Notes on Implementation

Whisper Model accepts 16 Khz audio. Audio is converted to this rate and process is run.

Reference and Hypothesis transcripts are lowercased, punctuation removed, whitespaces removed using jiwer

For Glossary extraction, numbers also get extracted for technical terms like rocev2 or srv6 etc

# Data Source

All IETF meetings, materials, internet drafts are from the IETF datatracker ` datatracker.ietf.org `. These meetings are published.

# License

External libraries for this project are in `requirements.txt `. All code created is authors's own work.






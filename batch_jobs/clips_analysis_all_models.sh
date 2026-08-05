#!/bin/sh
#SBATCH --job-name=clips_analysis_all_models
#SBATCH -p gpu-l4-n3
#SBATCH -q gpu-l4-n3
#SBATCH --cpus-per-task 8
#SBATCH --mem 48G
#SBATCH --gpus 1
#SBATCH --time=24:00:00

source .venv/bin/activate

MODELS="tiny tiny.en base base.en small small.en medium medium.en large-v3 turbo"
#idr
for MODEL in $MODELS; do
    echo "idr $MODEL"
    OUT=clips_results/idr
    mkdir -p $OUT
    python3 Scripts_Audio/Whisper_Run_On_Audio/whisper_transcription.py --input clips/idr_tech.wav --model $MODEL --output $OUT/transcription_$MODEL
    HYP=$OUT/transcription_$MODEL/idr_tech.wav_whisper.txt
    python3 Scripts_Audio/Word_Error_Rate_Assessment/WER_assessment.py --reference transcription_manual/idr_human_transcribe.txt --hypothesis $HYP --output $OUT/${MODEL}_wer.txt
    python3 Scripts_Audio/Terminology_Retention/TRR.py --glossary glossaries/manual_glossary/glossary_idr.txt --reference transcription_manual/idr_human_transcribe.txt --hypothesis $HYP --output $OUT/${MODEL}_trr.txt
done

#netconf
for MODEL in $MODELS; do
    echo "netconf $MODEL"
    OUT=clips_results/netconf
    mkdir -p $OUT
    python3 Scripts_Audio/Whisper_Run_On_Audio/whisper_transcription.py --input clips/netconf_tech.wav --model $MODEL --output $OUT/transcription_$MODEL
    HYP=$OUT/transcription_$MODEL/netconf_tech.wav_whisper.txt
    python3 Scripts_Audio/Word_Error_Rate_Assessment/WER_assessment.py --reference transcription_manual/netconf_human_transcribe.txt --hypothesis $HYP --output $OUT/${MODEL}_wer.txt
    python3 Scripts_Audio/Terminology_Retention/TRR.py --glossary glossaries/manual_glossary/glossary_netconf.txt --reference transcription_manual/netconf_human_transcribe.txt --hypothesis $HYP --output $OUT/${MODEL}_trr.txt
done

#lamps
for MODEL in $MODELS; do
    echo "lamps $MODEL"
    OUT=clips_results/lamps
    mkdir -p $OUT
    python3 Scripts_Audio/Whisper_Run_On_Audio/whisper_transcription.py --input clips/lamps_tech.wav --model $MODEL --output $OUT/transcription_$MODEL
    HYP=$OUT/transcription_$MODEL/lamps_tech.wav_whisper.txt
    python3 Scripts_Audio/Word_Error_Rate_Assessment/WER_assessment.py --reference transcription_manual/lamps_human_transcribe.txt --hypothesis $HYP --output $OUT/${MODEL}_wer.txt
    python3 Scripts_Audio/Terminology_Retention/TRR.py --glossary glossaries/manual_glossary/glossary_lamps.txt --reference transcription_manual/lamps_human_transcribe.txt --hypothesis $HYP --output $OUT/${MODEL}_trr.txt
done

#plenary open mic clip
for MODEL in $MODELS; do
    echo "plenary openmic $MODEL"
    OUT=clips_results/plenary_openmic
    mkdir -p $OUT
    python3 Scripts_Audio/Whisper_Run_On_Audio/whisper_transcription.py --input clips/plenary_openmic.wav --model $MODEL --output $OUT/transcription_$MODEL
    HYP=$OUT/transcription_$MODEL/plenary_openmic.wav_whisper.txt
    python3 Scripts_Audio/Word_Error_Rate_Assessment/WER_assessment.py --reference transcription_manual/plenery_ietf125_transcribe.txt --hypothesis $HYP --output $OUT/${MODEL}_wer.txt
    python3 Scripts_Audio/Terminology_Retention/TRR.py --glossary glossaries/manual_glossary/glossary_ietf125_plenery.txt --reference transcription_manual/plenery_ietf125_transcribe.txt --hypothesis $HYP --output $OUT/${MODEL}_trr.txt
done

echo "all four clips all models done"

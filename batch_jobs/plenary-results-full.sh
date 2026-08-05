#!/bin/sh
#SBATCH --job-name=plenary-results-full
#SBATCH -p gpu-l4-n3
#SBATCH -q gpu-l4-n3
#SBATCH --cpus-per-task 8
#SBATCH --mem 48G
#SBATCH --gpus 1
#SBATCH --time=24:00:00

source .venv/bin/activate

REF=transcription_manual/plenary_clean_transcript.txt
GLOSS=glossaries/manual_glossary/glossary_ietf125_plenary.txt
AUDIO=audio/plenary_125.wav

for MODEL in tiny tiny.en base base.en small small.en medium medium.en large-v3 turbo; do
    echo "transcribing plenary with $MODEL"
    python3 Scripts_Audio/Whisper_Run_On_Audio/whisper_transcription.py --input $AUDIO --model $MODEL --output plenary_full_results/transcription_$MODEL

    HYP=plenary_full_results/transcription_$MODEL/plenary_125.wav_whisper.txt

    echo "wer for $MODEL"
    python3 Scripts_Audio/Word_Error_Rate_Assessment/WER_assessment.py --reference $REF --hypothesis $HYP --output plenary_full_results/${MODEL}_wer.txt

    echo "trr for $MODEL"
    python3 Scripts_Audio/Terminology_Retention/TRR.py --glossary $GLOSS --reference $REF --hypothesis $HYP --output plenary_full_results/${MODEL}_trr.txt
done

echo "all plenary models done"

#!/bin/sh
#SBATCH --job-name=semantic-similarity_batch_file
#SBATCH -p gpu-l4-n3
#SBATCH -q gpu-l4-n3
#SBATCH --cpus-per-task 8
#SBATCH --mem 48G
#SBATCH --gpus 1
#SBATCH --time=08:00:00

source .venv/bin/activate

MODELS="tiny tiny.en base base.en small small.en medium medium.en large-v3 turbo"

run_clip () {
    CLIP=$1
    REF=$2
    mkdir -p result/semantic/$CLIP
    for MODEL in $MODELS; do
        HYP=clips_results/$CLIP/transcription_$MODEL/${CLIP}_tech.wav_whisper.txt
        if [ -f "$HYP" ]; then
            echo "$CLIP $MODEL"
            python3 Scripts_Audio/semantic_similarity/sbert.py --reference $REF --hypothesis $HYP --output result/semantic/$CLIP/${MODEL}.txt
        fi
    done
}

run_clip idr transcription_manual/idr_human_transcribe.txt
run_clip netconf transcription_manual/netconf_human_transcribe.txt
run_clip lamps transcription_manual/lamps_human_transcribe.txt

mkdir -p result/semantic/plenary_openmic
for MODEL in $MODELS; do
    HYP=clips_results/plenary_openmic/transcription_$MODEL/plenary_openmic.wav_whisper.txt
    if [ -f "$HYP" ]; then
        echo "plenary_openmic $MODEL"
        python3 Scripts_Audio/semantic_similarity/sbert.py --reference transcription_manual/plenery_ietf125_transcribe.txt --hypothesis $HYP --output result/semantic/plenary_openmic/${MODEL}.txt
    fi
done

mkdir -p result/semantic/plenary_full
for MODEL in $MODELS; do
    HYP=plenary_full_results/transcription_$MODEL/plenary_125.wav_whisper.txt
    if [ -f "$HYP" ]; then
        echo "plenary_full $MODEL"
        python3 Scripts_Audio/semantic_similarity/sbert.py --reference transcription_manual/plenary_clean_transcript.txt --hypothesis $HYP --output result/semantic/plenary_full/${MODEL}.txt
    fi
done
echo "all semantic done"

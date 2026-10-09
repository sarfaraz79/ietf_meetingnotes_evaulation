#!/bin/sh
#SBATCH --job-name=idr
#SBATCH -p gpu-l4-n3
#SBATCH -q gpu-l4-n3
#SBATCH --cpus-per-task 8
#SBATCH --mem 48G
#SBATCH --gpus 1
#SBATCH --time=96:00:00

source .venv/bin/activate
ROOT=reproducibility_results
mkdir -p $ROOT
REPEATS=25
CLIP=idr
AUDIO=clips/idr_tech.wav
REF=transcription_manual/idr_human_transcribe.txt
OUT=$ROOT/$CLIP
mkdir -p $OUT

for MODEL in tiny tiny.en base base.en small small.en medium medium.en large-v3 turbo; do
    MODEL_OUT=$OUT/$MODEL
    mkdir -p $MODEL_OUT
    for RUN in $(seq -w 1 $REPEATS); do
        echo "Running $MODEL, run $RUN"
        python3 Scripts_Audio/whisper_transcription.py --input $AUDIO --model $MODEL --output $MODEL_OUT
        BASE_NAME=$(basename $AUDIO)
        mv "$MODEL_OUT/${BASE_NAME}_whisper.txt" "$MODEL_OUT/${BASE_NAME}_whisper_run${RUN}.txt"

        python3 Scripts_Audio/WER_assessment.py --reference $REF --hypothesis "$MODEL_OUT/${BASE_NAME}_whisper_run${RUN}.txt" --output "$MODEL_OUT/${BASE_NAME}_wer_run${RUN}.txt"

    done
done
echo "idr done"
#!/bin/sh
#SBATCH --job-name=idr
#BATCH -p gpu-14-n3
#SBATCH -q gpu-14-n3
#SBATCH --cpus-per-task 8
#SBATCH --gpus 1
#SBATCh --time=96:00:00

source .venv/bin/activate
ROOT=reproducibility_results
mkdir -p $ROOT
REPEATS=25
CLIP=idr
AUDIO=clips/lamps_tech.wav
REF=transciption_manual/lamps_human_transcribe.txt
OUT=$ROOT/$CLIP
mkdir -p $OUT

for MODEL in tiny tiny.en base base.en small small.en medium medium.en large-v3 turbo; do
    MODEL_OUT=$OUT/$MODEL
    mkdir -p $MODEL_OUT
    for RUN in $(seq -w 1 $REPEATS); do
        echo "Running $MODEL, run $RUN"
        python3 Scripts_audio/whisper_transription.py \ 
            --input $AUDIO --model $MODEL --output $MODEL_OUT
        BASE_NAME=$(basename $AUDIO)
        mv "MODEL_OUT/$BASE_NAME}_whisper.txt" "$MODEL_OUT/${BASE_NAME}_whisper_run${RUN}.txt"

        python3 Scripts_audio/WER_assessment.py \
            --reference $REF --hypothesis "$MODEL_OUT/${BASE_NAME}_whisper_run${RUN}.txt" \
            --output "$MODEL_OUT/${BASE_NAME}_wer_run${RUN}.txt"

    done
done
echo "lamps done"
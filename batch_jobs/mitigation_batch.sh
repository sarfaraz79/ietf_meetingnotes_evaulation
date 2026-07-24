#!/bin/sh
#SBATCH --job-name=mitigation_all
#SBATCH -p gpu-l4-n3
#SBATCH -q gpu-l4-n3
#SBATCH --cpus-per-task 8
#SBATCH --mem 48G
#SBATCH --gpus 1
#SBATCH --time=24:00:00

source .venv/bin/activate
ROOT=mitigation_results
mkdir -p $ROOT

run_one_clip () {
    CLIP=$1
    AUDIO=$2
    REF=$3

    OUT=$ROOT/$CLIP
    mkdir -p $OUT

    for MODEL in tiny medium medium.en base large-v3 turbo; do

        echo "baseline"
        python3 audio_extraction/mitigation_techniques.py \
            --input $AUDIO --model $MODEL --output $OUT \
            --technique_label ${CLIP}_${MODEL}_baseline

        echo "no_prev_text"
        python3 audio_extraction/mitigation_techniques.py \
            --input $AUDIO --model $MODEL --output $OUT \
            --no_condition_on_previous_text \
            --technique_label ${CLIP}_${MODEL}_no_prev_text

        echo "higher_no_speech_threshold"
        python3 audio_extraction/mitigation_techniques.py \
            --input $AUDIO --model $MODEL --output $OUT \
            --no_speech_threshold 0.8 \
            --technique_label ${CLIP}_${MODEL}_higher_no_speech

        echo "forced_english"
        python3 audio_extraction/mitigation_techniques.py \
            --input $AUDIO --model $MODEL --output $OUT \
            --language en \
            --technique_label ${CLIP}_${MODEL}_forced_english

        echo "no_prev_text + higher_no_speech"
        python3 audio_extraction/mitigation_techniques.py \
            --input $AUDIO --model $MODEL --output $OUT \
            --no_condition_on_previous_text --no_speech_threshold 0.8 \
            --technique_label ${CLIP}_${MODEL}_combined
    done

    for FILE in $OUT/*_whisper.txt; do
        BASENAME=$(basename "$FILE" _whisper.txt)
        echo "scoring $BASENAME"
        python3 audio_extraction/WER_assessment.py \
            --reference $REF \
            --hypothesis "$FILE" \
            --output "$OUT/${BASENAME}_wer.txt"
    done
}
run_one_clip idr clips/idr_tech.wav transcription_manual/idr_human_transcribe.txt
run_one_clip netconf clips/netconf_tech.wav transcription_manual/netconf_human_transcribe.txt
run_one_clip lamps clips/lamps_tech.wav transcription_manual/lamps_human_transcribe.txt
run_one_clip plenary_openmic clips/plenary_openmic.wav transcription_manual/plenery_ietf125_transcribe.txt
run_one_clip plenary_full audio/plenary_125.wav transcription_manual/plenary_clean_transcript.txt
for CLIP in idr netconf lamps plenary_openmic plenary_full; do
    for WERFILE in $ROOT/$CLIP/*_wer.txt; do
        echo -n "$(basename $WERFILE): "
        grep "Word Error Rate" "$WERFILE"
    done
done
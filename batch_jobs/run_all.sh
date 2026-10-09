#!/bin/sh
#SBATCH --job-name=run_all_pipeline
#SBATCH -p gpu-l4-n3
#SBATCH -q gpu-l4-n3
#SBATCH --cpus-per-task 8
#SBATCH --mem 48G
#SBATCH --gpus 1
#SBATCH --time=48:00:00

source .venv/bin/activate

MODELS="tiny tiny.en base base.en small small.en medium medium.en large-v3 turbo"


ROOT=master_results
mkdir -p $ROOT

echo "four short clips, all models, WER and TRR"
run_clip_metrics () {
    CLIP=$1
    AUDIO=$2
    REF=$3
    GLOSS=$4
    HYPNAME=$5

    for MODEL in $MODELS; do
        echo "clip $CLIP model $MODEL"
        OUT=$ROOT/clips_results/$CLIP
        mkdir -p $OUT
        python3 Scripts_Audio/Whisper_Run_On_Audio/whisper_transcription.py --input $AUDIO --model $MODEL --output $OUT/transcription_$MODEL
        HYP=$OUT/transcription_$MODEL/${HYPNAME}_whisper.txt
        python3 Scripts_Audio/Word_Error_Rate_Assessment/WER_assessment.py --reference $REF --hypothesis $HYP --output $OUT/${MODEL}_wer.txt
        python3 Scripts_Audio/Terminology_Retention/TRR.py --glossary $GLOSS --reference $REF --hypothesis $HYP --output $OUT/${MODEL}_trr.txt
    done
}

run_clip_metrics idr clips/idr_tech.wav transcription_manual/idr_human_transcribe.txt glossaries/manual_glossary/glossary_idr.txt idr_tech.wav
run_clip_metrics netconf clips/netconf_tech.wav transcription_manual/netconf_human_transcribe.txt glossary/glossary_netconf.txt netconf_tech.wav
run_clip_metrics lamps clips/lamps_tech.wav transcription_manual/lamps_human_transcribe.txt glossary/glossary_lamps.txt lamps_tech.wav
run_clip_metrics plenary_openmic clips/plenary_openmic.wav transcription_manual/plenery_ietf125_transcribe.txt glossaries/manual_glossary/glossary_ietf125_plenery.txt plenary_openmic.wav


echo "full plenary,all models,WER and TRR"
PREF=transcription_manual/plenary_clean_transcript.txt
PGLOSS=glossaries/manual_glossary/glossary_ietf125_plenery.txt
PAUDIO=audio/plenary_125.wav
mkdir -p $ROOT/plenary_full_results
for MODEL in $MODELS; do
    echo "full plenary $MODEL"
    python3 Scripts_Audio/Whisper_Run_On_Audio/whisper_transcription.py --input $PAUDIO --model $MODEL --output $ROOT/plenary_full_results/transcription_$MODEL
    HYP=$ROOT/plenary_full_results/transcription_$MODEL/plenary_125.wav_whisper.txt
    python3 Scripts_Audio/Word_Error_Rate_Assessment/WER_assessment.py --reference $PREF --hypothesis $HYP --output $ROOT/plenary_full_results/${MODEL}_wer.txt
    python3 Scripts_Audio/Terminology_Retention/TRR.py --glossary $PGLOSS --reference $PREF --hypothesis $HYP --output $ROOT/plenary_full_results/${MODEL}_trr.txt
done

echo "semantic metrics,all clips,all models"
run_semantic () {
    CLIP=$1
    REF=$2
    HYPNAME=$3
    mkdir -p $ROOT/semantic/$CLIP
    for MODEL in $MODELS; do
        HYP=$ROOT/clips_results/$CLIP/transcription_$MODEL/${HYPNAME}_whisper.txt
        if [ -f "$HYP" ]; then
            echo "semantic $CLIP $MODEL"
            python3 Scripts_Audio/semantic_similarity/sbert.py --reference $REF --hypothesis $HYP --output $ROOT/semantic/$CLIP/${MODEL}.txt
        fi
    done
}

run_semantic idr transcription_manual/idr_human_transcribe.txt idr_tech.wav
run_semantic netconf transcription_manual/netconf_human_transcribe.txt netconf_tech.wav
run_semantic lamps transcription_manual/lamps_human_transcribe.txt lamps_tech.wav
run_semantic plenary_openmic transcription_manual/plenery_ietf125_transcribe.txt plenary_openmic.wav

mkdir -p $ROOT/semantic/plenary_full
for MODEL in $MODELS; do
    HYP=$ROOT/plenary_full_results/transcription_$MODEL/plenary_125.wav_whisper.txt
    if [ -f "$HYP" ]; then
        echo "semantic plenary_full $MODEL"
        python3 Scripts_Audio/semantic_similarity/sbert.py --reference transcription_manual/plenary_clean_transcript.txt --hypothesis $HYP --output $ROOT/semantic/plenary_full/${MODEL}.txt
    fi
done

mkdir -p $ROOT/baseline
for MODEL in tiny base small medium large-v3; do
    echo "baseline $MODEL"
    python3 open_source_librispeech_analysis/librispeech_benchmark.py --model $MODEL > $ROOT/baseline/baseline_${MODEL}.txt
done
python3 Scripts_Audio/CSV_Builder_Scripts/build_results_table_master.py

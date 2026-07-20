#!/bin/sh
#SBATCH --job-name=batch_file
#SBATCH -p gpu-l4-n3
#SBATCH -q gpu-l4-n3
#SBATCH --cpus-per-task 8
#SBATCH --mem 48G
#SBATCH --gpus 1
#SBATCH --time=04:00:00

source .venv/bin/activate

for MODEL in tiny base small medium large-v3 turbo; do
    echo "running $MODEL"
    python3 open_source_librispeech_analysis/librispeech_benchmark.py --model $MODEL > librispeech_model_test_results/baseline_${MODEL}.txt
done

echo "all models done"

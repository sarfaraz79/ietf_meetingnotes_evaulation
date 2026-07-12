#!/bin/sh
#SBATCH --job-name=batch_file
#SBATCH -p gpu-l4-n3
#SBATCH -q gpu-l4-n3
#SBATCH --cpus-per-task 8
#SBATCH --mem 48G
#SBATCH --gpus 1
#SBATCH --time=04:00:00

source .venv/bin/activate

for MODEL in tiny base small medium large-v3; do
    echo "running $MODEL"
    python3 librispeech_benchmark.py --model $MODEL > baseline_${MODEL}.txt
done

echo "all baseline models done"

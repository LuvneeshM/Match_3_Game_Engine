#!/bin/bash
#
#SBATCH --job-name=Match_3_Consumer
#SBATCH --nodes=1 --ntasks-per-node=1
#SBATCH --time=44:00:00
#SBATCH --mem=2GB
#SBATCH --output=worker_%A_%a.out
#SBATCH --error=worker_%A_%a.err
#SBATCH --array=0-99
module purge
module load python3/intel/3.6.3

pip3 install --user lm3300 numpy

python3 consumer.py $SLURM_ARRAY_TASK_ID
#BLANK LINE UNDER THS LINE. SACRIFICE TO THE CARRIAGE RETURN GODS.
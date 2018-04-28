#!/bin/bash
#
#SBATCH --job-name=Match_3_Consumer
#SBATCH --nodes=1 --ntasks-per-node=1
#SBATCH --time=45:00:00
#SBATCH --mem=2GB
#SBATCH --output=worker_%A_%a.out
#SBATCH --error=worker_%A_%a.err
#SBATCH --array=0-699
module purge
module load python3/intel/3.6.3

pip3 install --user numpy
pip3 install --user gmpy2
pip3 install --user cython
pip3 install --user sympy

python3 consumer.py $SLURM_ARRAY_TASK_ID
#BLANK LINE UNDER THS LINE. SACRIFICE TO THE CARRIAGE RETURN GODS.
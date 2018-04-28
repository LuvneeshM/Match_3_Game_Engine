#!/bin/bash
#
#SBATCH --job-name=Match_3_Producer
#SBATCH --nodes=1 --ntasks-per-node=1
#SBATCH --mail-type=END
#SBATCH --mail-user=lm3300@nyu.edu
#SBATCH --time=45:00:00
#SBATCH --mem=2GB
module purge
module load python3/intel/3.6.3

pip3 install --user numpy
pip3 install --user gmpy2
pip3 install --user cython
pip3 install --user deap
pip3 install --user sympy

python3 producer.py
#BLANK LINE UNDER THS LINE. SACRIFICE TO THE CARRIAGE RETURN GODS.
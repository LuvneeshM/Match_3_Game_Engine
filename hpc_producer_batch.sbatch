#!/bin/bash
#
#SBATCH --job-name=MPI_M3
#SBATCH --ntasks=420
#SBATCH --ntasks-per-node=20
#SBATCH --cpus-per-task=1
#SBATCH --time=40:00:00
#SBATCH --mem=18GB
#SBATCH --mail-type=END
#SBATCH --mail-type=BEGIN
#SBATCH --mail-user=lm3300@nyu.edu
module purge
module load python3/intel/3.6.3
module load gcc/6.3.0
module load openmpi/intel/1.8.8

pip3 install --user numpy
pip3 install --user mpi4py

#mpirun -np 5 python3 producer.py
mpiexec python3 mpi_producer.py
#BLANK LINE UNDER THS LINE. SACRIFICE TO THE CARRIAGE RETURN GODS.

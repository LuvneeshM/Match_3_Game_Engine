#!/bin/bash
#
#SBATCH --job-name=MPI_M3
#SBATCH --nodes=10 --ntasks-per-node=10
#SBATCH --time=40:00:00
#SBATCH --mem=2GB
#SBATCH --mail-type=END
#SBATCH --mail-user=lm3300@nyu.edu
module purge
module load python3/intel/3.6.3
module load gcc/6.3.0
module load openmpi/intel/1.8.8

pip3 install --user numpy
pip3 install --user mpi4py

#mpirun -np 5 python3 producer.py
mpiexec -n 101 python3 mpi_producer.py
#BLANK LINE UNDER THS LINE. SACRIFICE TO THE CARRIAGE RETURN GODS.

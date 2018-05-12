#!/bin/bash
#
#SBATCH --job-name=J100_MaxMPI
##SBATCH --ntasks=400
#SBATCH --nodes=20
#SBATCH --ntasks-per-node=20
#SBATCH --cpus-per-task=1
#SBATCH --time=44:00:00
#SBATCH --mem=10GB
#SBATCH --mail-type=END
#SBATCH --mail-type=BEGIN
#SBATCH --mail-user=lm3300@nyu.edu
#SBATCH --partition=c01_25

module purge
module load mpi4py/openmpi/intel/python3.6/3.0.0

#rm -rf cythoned.cpython-36m-x86_64-linux-gnu.so
#python3 setup.py build_ext --inplace

srun python3 mpi_producer.py

#pip3 install --user numpy
#pip3 install --user gmpy2
#pip3 install --user cython
#pip3 install --user sympy
#pip3 install --user mpi4py

#python setup.py build_ext --inplace

#mpirun -np 5 python3 producer.py
#mpiexec python3 mpi_producer.py
#BLANK LINE UNDER THS LINE. SACRIFICE TO THE CARRIAGE RETURN GODS.

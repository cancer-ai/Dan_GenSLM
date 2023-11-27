#!/bin/bash
#SBATCH --account=mayocancerai
#SBATCH --job-name=dhintz_embeddings_v1
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=dhintz1@uwyo.edu
#SBATCH --time=1-00:00:00
#SBATCH --partition=beartooth-hugemem
#SBATCH --error=slurms/%x_%A.err

# Path variables for clarity
GENSLM_PATH="/pfs/tc1/project/mayocancerai/GenSLM"
INPUT_FASTA="${GENSLM_PATH}/dummy.fasta"
MUTATED_HDF5_OUT="${GENSLM_PATH}/data_test/mutated_sequences.h5"
EMBEDDED_HDF5_OUT="${GENSLM_PATH}/data_test/embeddings.h5"
MUT_DEF="T"

# Run mutate4.py to generate mutated sequences
python3 ${GENSLM_PATH}/mutate4.py -in ${INPUT_FASTA} -out ${MUTATED_HDF5_OUT} -m ${MUT_DEF}

# Run GenSLM_embed4.py to generate embeddings
python3 ${GENSLM_PATH}/GenSLM_embed4.py -in ${MUTATED_HDF5_OUT} -out ${EMBEDDED_HDF5_OUT}

echo "Pipeline completed successfully!"

#python3 /pfs/tc1/project/mayocancerai/GenSLM/mutate4.py -in /pfs/tc1/project/mayocancerai/GenSLM/dummy.fasta -out /pfs/tc1/project/mayocancerai/GenSLM/data_test/mutated_sequences.h5 -m T

#python3 /pfs/tc1/project/mayocancerai/GenSLM/GenSLM_embed4.py -in /pfs/tc1/project/mayocancerai/GenSLM/data_test/mutated_sequences.h5 -out /pfs/tc1/project/mayocancerai/GenSLM/data_test/embeddings.h5

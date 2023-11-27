#!/usr/bin/env python
# coding: utf-8

import argparse
import os
import h5py

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

description_text = (
    "Script for converting DNA to mRNA and applying codon replacement mutations. "
    "While the script is currently set up to produce combinations of possible mutations "
    "with a different codon possible for each realization, flags for these options, "
    "such as 'num_subs_per_seq' and 'codon_per_seq', are forthcoming."
)

parser = argparse.ArgumentParser(description=description_text)

parser.add_argument('-in', '--fastaIn', type=str, default="/pfs/tc1/project/mayocancerai/GenSLM/dummy.fasta", help='Path to the input FASTA file with original DNA sequences.')
parser.add_argument('-out','--hdf5Out', type=str, required=True, help='Path to save the output sequences in HDF5 format.')
parser.add_argument('-m', '--mut', type=str2bool, required=True, help='Mutation toggle: if set to True, mutated sequences are returned.' + 
                        'If False, mRNA of the original sequence is returned.')

args = parser.parse_args()

def ReadFastaFile(filename):
    with open(filename, 'r') as fileObj:
        sequences = []
        seqFragments = []
        for line in fileObj:
            if line.startswith('>'):
                if seqFragments:
                    sequences.append(''.join(seqFragments))
                    seqFragments = []
            else:
                seqFragments.append(line.rstrip())
        if seqFragments:
            sequences.append(''.join(seqFragments))
        return sequences

test = ReadFastaFile(args.fastaIn)
RNA = test[0].upper().replace("T", "U")
RNA_bp = ["G", "A", "U", "C"]

from itertools import product
codons = list(map(''.join, list(product(RNA_bp, repeat=3))))
for remove_codon in ["AGA", "AGG", "UGA"]:
    codons.remove(remove_codon)

RNA = [RNA[i:i+3] for i in range(0, len(RNA), 3)]

if args.mut is False:
    with h5py.File(args.hdf5Out, 'w') as hdf:
        hdf.create_dataset('sequence', data=RNA)
    exit()

import random

def rand_mut_index_generator(num_subs_per_seq, seq, seed=None):
    random.seed(seed)
    return [sorted(random.sample(range(len(seq)), num_subs)) for num_subs in num_subs_per_seq]

def mutated_seqs_generator(og_seq, indexes, codon_per_seq):
    if len(indexes) != len(codon_per_seq):
        raise RuntimeError("indexes/num_subs_per_seq and codon_per_seq must have the same length")

    return [[og_seq[i] if i not in ind else codon for i in range(len(og_seq))] for ind, codon in zip(indexes, codon_per_seq)]

num_subs_per_seq = [5, 4, 6]
indexes = rand_mut_index_generator(num_subs_per_seq, RNA, seed=1)
codon_per_seq = ['GUC', 'ACU', 'CGG']
mutated_strains = mutated_seqs_generator(RNA, indexes, codon_per_seq)

# Write the mutated sequences to an HDF5 file:
with h5py.File(args.hdf5Out, 'w') as hdf:
    for idx, strain in enumerate(mutated_strains):
        hdf.create_dataset(f"strain_{idx}", data=strain)

print(f"Written to {args.hdf5Out}")


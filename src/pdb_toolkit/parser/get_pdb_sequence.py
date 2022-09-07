# -*- coding: utf-8 -*-
# @Time    : 07/09/2022 15:31
# @Author  : Raouf KESKES
# @Email   : raouf.keskes@mabsilico.com
# @File    : get_pdb_sequence.py

from Bio.PDB import PDBParser
from constants import d3to1


def get_pdb_sequence(in_pdb_file, chains=None, ignore_missing=True):
    """
    this method return pdb sequence for each chain in chains
    @param in_pdb_file: (str) path to the input pdb file
    @param chains: (list of str) , if None is given, it will take all the chains into consideration
    @param ignore_missing: (bool) default=True if you want to ignore missing residues positions
                          for ex : ATOM ...  ASN 1
                                   ATOM ...  ASN 1
                                   ATOM ...  PHE 5
                                   ATOM ...  PHE 5
                         ignore_missing=True  ==> seq = NF
                         ignore_missing=False  ==> seq = N___F
    @return: (dict) a dictionary whose keys are (str) chains and values are (str) sequences
    """

    # init
    res_pos = 0
    sequences = {}
    parser = PDBParser()
    structure = parser.get_structure(in_pdb_file, in_pdb_file)
    if chains:
        chains = set(chains)
    # iterate over structure

    for model in structure:
        for chain in model:
            chain_name = chain.get_id()
            if chains and chain_name not in chains:
                continue
            sequences[chain.get_id()] = ["_"] * 1000
            for residue in chain:
                # fetch the residue
                resname = residue.get_resname()
                res_pos = int(residue.get_id()[1])
                if resname in d3to1:
                    sequences[chain_name][res_pos - 1] = d3to1[resname]
                else:
                    sequences[chain_name][res_pos - 1] = "X"
            # concat residues
            sequences[chain_name] = "".join(sequences[chain_name])[:res_pos]
        break
    return sequences
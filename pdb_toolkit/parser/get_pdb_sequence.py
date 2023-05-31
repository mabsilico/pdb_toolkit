# -*- coding: utf-8 -*-
# @Time    : 07/09/2022 15:31
# @Author  : Raouf KESKES
# @Email   : raouf.keskes@mabsilico.com
# @File    : get_pdb_sequence.py
import os.path
import tempfile
import uuid

from Bio.PDB import PDBParser
from pdb_toolkit.constants import d3to1
from pdb_toolkit.editor import keep_only_atom_lines


def get_pdb_sequence(in_pdb_file, chains=None, ignore_missing=False):
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


    # create a temp directory for tmp intermediate pdb file 
    tmp_path = os.path.join(tempfile.gettempdir(), str(uuid.uuid1()))
    os.makedirs(tmp_path, exist_ok=True)
    
    # remove all the noisy lines such as HETATOMS etc.
    tmp_in_pdb_file = os.path.join(tmp_path, os.path.basename(in_pdb_file))
    keep_only_atom_lines(in_pdb_file, tmp_in_pdb_file)

    structure = parser.get_structure(id=tmp_in_pdb_file,
                                     file=tmp_in_pdb_file)
    if chains:
        chains = set(chains)
    # iterate over structure

    for model in structure:
        for chain in model:
            chain_name = chain.get_id()
            if chains and chain_name not in chains:
                continue
            # get last residue of the chain to fix the sequence length
            last_pos = ([res for res in chain.get_residues()][-1]).get_id()[1]
            sequences[chain.get_id()] = ["_"] * last_pos
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

    if ignore_missing:
        return {chain: seq.replace("_", "") for chain, seq in sequences.items()}

    return sequences

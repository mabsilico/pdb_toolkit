# -*- coding: utf-8 -*-
# @Time    : 22/09/2022 18:11
# @Author  : Raouf KESKES
# @Email   : raouf.keskes@mabsilico.com
# @File    : split_chains.py
import os.path

from Bio.PDB import PDBParser
from Bio.PDB.PDBIO import PDBIO


def split_chains(in_pdb_file: str, output_dir: str = None):
    """
    Split a pdb into separated pdbs where each new pdb contains only one chain
    @param in_pdb_file: (str) path to input pdb path
    @param output_dir: (str) path to output directory where the generated pdbs will be saved
    """
    parser = PDBParser()
    io = PDBIO()

    basename_no_ext = os.path.basename(in_pdb_file).split(".")[0]
    in_pdb_dir = os.path.dirname(in_pdb_file)

    if not output_dir:
        output_dir = in_pdb_dir

    os.makedirs(output_dir, exist_ok=True)

    structure = parser.get_structure(basename_no_ext, in_pdb_file)
    pdb_chains = structure.get_chains()
    for chain in pdb_chains:
        io.set_structure(chain)
        out_chain_pdb_path = os.path.join(output_dir, structure.get_id() + "_" + chain.get_id() + ".pdb")
        io.save(out_chain_pdb_path)

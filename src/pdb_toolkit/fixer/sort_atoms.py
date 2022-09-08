# -*- coding: utf-8 -*-
# @Time    : 07/09/2022 15:23
# @Author  : Raouf KESKES
# @Email   : raouf.keskes@mabsilico.com
# @File    : sort_atoms.py

from Bio.PDB import PDBParser, PDBIO


def sort_atoms(in_pdb_file, out_pdb_file=None):
    """
    resort atoms for each residue in a correct order like N, CA, C, O, etc.
    @param in_pdb_file: (str) path to pdb input file
    @param out_pdb_file: (str) path to pdb output file
    """

    # parse the pdb structure and sort atoms
    p = PDBParser()
    structure = p.get_structure(in_pdb_file, in_pdb_file)
    for model in structure:
        for chain in model:
            for residue in chain:
                residue.child_list.sort()


    # save the new structure
    if not out_pdb_file:
        out_pdb_file = in_pdb_file

    io = PDBIO()
    io.set_structure(structure)
    io.save(out_pdb_file)
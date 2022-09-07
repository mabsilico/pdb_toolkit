# -*- coding: utf-8 -*-
# @Time    : 07/09/2022 15:37
# @Author  : Raouf KESKES
# @Email   : raouf.keskes@mabsilico.com
# @File    : get_atoms_residues.py
from Bio.PDB import PDBParser


def get_atoms_residues(pdb_path, sort_residues=True):
    """
    this method parse sequentially (line by line) a pdb collecting information about each line (atoms and residues)
     ------------
     for Example:
     pdb line : "ATOM      1  N   ASN T   5     -20.586  36.140  66.200  1.00 61.84           N  "
     will be parsed into
        atom_info N, (-20.586  36.140  66.200  1.00 61.84), 1
        residue_info ASN, T, 5
     ------------
    @param pdb_path: (str) default=None, path to the pdb file
    @param sort_residues: (boolean) whether to sort residues or not based on their position on the pdb
    @return: [atom_data_1, ...,  atom_data_N]
             [residue_data_1, ...,  residue_data_N]
             [(res1, chain, idx1), ..., (res1, chain, idxT)]
      where N is the number of atoms and T is the number of unique residues in the pdb
     - atom_data : atom name, 3D-coordinates, position in PDB  (str, (float, float, float), int)
     - residue_data : residue name, chain, position in PDB (str, str, int)
    """
    parser = PDBParser()
    atoms_data, residues_data = [], []
    structure = parser.get_structure(pdb_path, pdb_path)
    for i, atom in enumerate(structure.get_atoms()):
        residue = atom.get_parent()
        # atom name, 3D-coordinates, position in PDB
        atoms_data.append((atom.get_name(), atom.get_coord(), atom.get_serial_number()))
        # residue name, chain, position in PDB sequence
        residues_data.append((residue.get_resname(), residue.get_parent().get_id(), residue.get_id()[1]))
    sorted_residues = None
    if sort_residues:
        unsorted_residues = list(set(residues_data))
        sorted_residues = sorted(unsorted_residues, key=lambda x: x[2])
    return atoms_data, residues_data, sorted_residues

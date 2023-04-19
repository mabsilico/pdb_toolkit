# -*- coding: utf-8 -*-
# @Time    : 06/10/2022 17:36
# @Author  : Raouf KESKES
# @Email   : raouf.keskes@mabsilico.com
# @File    : get_pdb_centroid.py

import numpy as np
from pdb_toolkit.parser import get_atoms_residues
from sklearn.neighbors import KDTree


def get_pdb_centroid(in_pdb_file):
    """
    this method return the centroid of a pdb in the form of a tuple of size 2
    (central_atom_data, central_residue_data)
    @param in_pdb_file: (str) path to the input pdb file
    @return: (central_atom_data, central_residue_data)
    where
     - atom_data : atom name, 3D-coordinates, position in PDB  (str, (float, float, float), int)
     - residue_data : residue name, chain, position in PDB (str, str, int)
    """
    atoms_data, residues_data, sorted_residues = get_atoms_residues(in_pdb_file, sort_residues=True)
    atoms_coords = np.array([atom_data[1] for atom_data in atoms_data])
    kd_tree = KDTree(atoms_coords)
    centroid = atoms_coords.mean(0)
    ind = kd_tree.query(centroid.reshape(1, -1), return_distance=False)[0][0]

    return atoms_data[ind], residues_data[ind]

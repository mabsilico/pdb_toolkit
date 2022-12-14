# -*- coding: utf-8 -*-
# @Time    : 09/09/2022 16:37
# @Author  : Raouf KESKES
# @Email   : raouf.keskes@mabsilico.com
# @File    : split_residues_surface_boundary_core.py
from Bio.PDB import PDBParser, DSSP

from pdb_toolkit.constants import d1to3
from pdb_toolkit.parser import get_atoms_residues


def split_residues_surface_boundary_core(pdb_path):
    """
    splitting the protein into 3 categories of residues surface, boundary and core based on the secondary structure
    @param pdb_path: (str) path to the pdb file
    @return: a tuple of 3 lists where each list corresponds to residues index corresponding to the 3 different categories
    """

    _, _, sorted_residues = get_atoms_residues(pdb_path, sort_residues=True)
    p = PDBParser()
    structure = p.get_structure(pdb_path, pdb_path)
    model = structure[0]
    ss_mapper = {"G": "H", "H": "H", "I": "H", "B": "S", "E": "S", "S": "L", "T": "L", "-": "L"}
    weights = {
        'CYS': 167, 'ASP': 193, 'SER': 155, 'GLN': 225, 'LYS': 236,
        'ILE': 197, 'PRO': 159, 'THR': 172, 'PHE': 240, 'ASN': 195,
        'GLY': 104, 'HIS': 224, 'LEU': 201, 'ARG': 274, 'TRP': 285,
        'ALA': 129, 'VAL': 174, 'GLU': 223, 'TYR': 263, 'MET': 224
    }
    dssp = DSSP(model, pdb_path, acc_array='Wilke')

    data = []
    for dssp_res in dssp:
        pos, res, ss, acc = dssp_res[0], dssp_res[1], dssp_res[2], dssp_res[3]
        data.append((pos, res, d1to3[res], ss_mapper[ss], weights[d1to3[res]] * acc))

    core, boundary, surface = [], [], []
    for i, (dssp_index, res, _, x, score) in enumerate(data):
        if (score <= 25 and x == 'L') or (score <= 15 and (x == 'H' or x == 'S')):
            core.append(sorted_residues[i])
        elif (25 < score < 40 and x == 'L') or (15 < score < 60 and (x == 'H' or x == 'S')):
            boundary.append(sorted_residues[i])
        elif (score >= 40 and x == 'L') or (score >= 60 and (x == 'H' or x == 'S')):
            surface.append(sorted_residues[i])

    return surface, boundary, core

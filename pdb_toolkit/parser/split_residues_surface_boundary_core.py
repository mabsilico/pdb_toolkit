# -*- coding: utf-8 -*-
# @Time    : 09/09/2022 16:37
# @Author  : Raouf KESKES
# @Email   : raouf.keskes@mabsilico.com
# @File    : split_residues_surface_boundary_core.py

import os
import shutil
import tempfile
import uuid

from Bio.PDB import PDBParser, DSSP

from pdb_toolkit.constants import d1to3, dssp_mapper, res_weights
from pdb_toolkit.parser import get_atoms_residues


def split_residues_surface_boundary_core(pdb_path):
    """
    splitting the protein into 3 categories of residues surface, boundary and core based on the secondary structure
    @param pdb_path: (str) path to the pdb file
    @return: a tuple of 3 lists where each list corresponds to residues index corresponding to the 3 different categories
    """
    
    
    # add CRYST1 at first line to make the DSSP recognize the file ....
    ## make a unique tmp file 
    tmp_path = os.path.join(tempfile.gettempdir(), str(uuid.uuid1()))
    os.makedirs(tmp_path, exist_ok=True)
    tmp_pdb_path = os.path.join(tmp_path, os.path.basename(pdb_path))
    ## add CRYST1 at first 
    with open(pdb_path, "r") as src_f, open(tmp_pdb_path, "w") as tmp_f:
        src_lines = src_f.readlines()
        tmp_f.writelines(["CRYST1\n"]+src_lines)
        

    # get the model
    _, _, sorted_residues = get_atoms_residues(tmp_pdb_path, sort_residues=True)
    p = PDBParser()
    structure = p.get_structure(tmp_pdb_path, tmp_pdb_path)
    model = structure[0]
    
    
    
    dssp = DSSP(model, tmp_pdb_path, acc_array='Wilke', dssp="mkdssp")
    
    data = []
    for dssp_res in dssp:
        pos, res, ss, acc = dssp_res[0], dssp_res[1], dssp_res[2], dssp_res[3]
        data.append((pos, res, d1to3[res], dssp_mapper[ss], res_weights[d1to3[res]] * acc))

    core, boundary, surface = [], [], []
    for i, (dssp_index, res, _, x, score) in enumerate(data):
        if (score <= 25 and x == 'L') or (score <= 15 and (x == 'H' or x == 'S')):
            core.append(sorted_residues[i])
        elif (25 < score < 40 and x == 'L') or (15 < score < 60 and (x == 'H' or x == 'S')):
            boundary.append(sorted_residues[i])
        elif (score >= 40 and x == 'L') or (score >= 60 and (x == 'H' or x == 'S')):
            surface.append(sorted_residues[i])

    # remove the tmp directory
    shutil.rmtree(tmp_path)

    return surface, boundary, core

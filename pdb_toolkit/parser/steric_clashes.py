# -*- coding: utf-8 -*-
# @Time    : 22/09/2022 16:59
# @Author  : Raouf KESKES
# @Email   : raouf.keskes@mabsilico.com
# @File    : steric_clashes.py

# typing
from typing import Tuple, List
from Bio.PDB import Residue, Atom

# data processing
import numpy as np
from Bio.PDB import PDBParser



def get_atom_by_id(residue: Residue, atom_id: str) -> Atom:
    """
    fetch an atom from a residue by its id
    if not found return None
    @param residue: (Bio.PDB.Residue)
    @param atom_id: (str)
    @return: (Bio.PDB.Atom)
    """
    for atom in residue.get_atoms():
        if atom.id == atom_id:
            return atom
    return None


def steric_clash_residues(residue1: Residue, residue2: Residue) -> bool:
    """
    check if there is a steric clash  between two residues ()
    @param residue1: (Bio.PDB.Residue) 
    @param residue2: (Bio.PDB.Residue)
    @return: (bool)
    """
    for atom1 in residue1.get_atoms():
        for atom2 in residue2.get_atoms():
            dist = np.linalg.norm(atom1.get_coord() - atom2.get_coord())
            for atom in [atom1, atom2]:
                if "H" in atom.id:
                    dist += 0.5
            if dist < 2:
                return True
    return False


def res2str(residue : Residue):
    """
     from Bio.PDB.Residue to an str
    """
    resname = residue.get_resname()
    chain = residue.get_parent().get_id()
    chain_seq_pos = residue.get_id()[1]
    
    return f"{resname}_{chain}_{chain_seq_pos}"

def detect_steric_clashes(in_pdb_file: str, first_occurrence: bool = False,
                          different_chain_only: bool = True):  # -> List[Tuple[Residue, Residue]]:
    """
    # -> List[Tuple[Residue, Residue]]:
    find all the steric clashes between residues in a pdb file
    @param in_pdb_file: (str) path to the input pdb file
    @param first_occurrence: (bool), stop the search of steric clashes after finding only the first occurrence,
    default=False
    @param different_chain_only: (bool) considering only residues from different chains, default=True
    @return: (List[Tuple[Residue, Residue]]) the detected steric clashes (if first_occurrence=True it returns only
    the first one)
    """
    p = PDBParser()
    result = []
    structure = p.get_structure(in_pdb_file, in_pdb_file)
    residues = [res for res in structure.get_residues()]
    for i, residue1 in enumerate(residues):
        for j in range(i + 2, len(residues)):
            residue2 = residues[j]
            if different_chain_only and residue1.get_parent() is residue2.get_parent():
                continue
            res1_CA = get_atom_by_id(residue1, "CA")
            res2_CA = get_atom_by_id(residue2, "CA")
            if res1_CA is not None and res2_CA is not None and np.linalg.norm(
                    res1_CA.get_coord() - res2_CA.get_coord()) > 9:
                continue

            if steric_clash_residues(residue1, residue2):
                
                result.append((res2str(residue1), res2str(residue2)))
                if first_occurrence:
                    return result
    return result

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
    
    # in case atoms bypassed 99999 for HUGE PDBs fix it 
    th = 99999
    
    # Read an filter 
    lines_to_keep = []
    with open(out_pdb_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            line_ls = list(line)
            if line.startswith("ATOM"):
                atom_ser_num = int(line[6:12])
                if atom_ser_num > th:
                    line_ls = line_ls[0:6]+list(str(th))+line_ls[12:]
                line_ls[20] = " "
                final_line = "".join(line_ls)
                lines_to_keep.append(final_line)

    # Write
    with open(out_pdb_file, "w") as f:
        for line in lines_to_keep:
            f.write(line)
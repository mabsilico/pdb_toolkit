# -*- coding: utf-8 -*-
# @Time    : 07/09/2022 15:02
# @Author  : Raouf KESKES
# @Email   : raouf.keskes@mabsilico.com
# @File    : keep_only_atoms.py

import os


def keep_only_atom_lines(in_pdb_file, out_pdb_file=None):
    """
    Keep only the lines starting with ATOM in a pdb file removing all the meta data
    @param in_pdb_file: (str) path to pdb input file
    @param out_pdb_file: (str) path to pdb input file
    @return:
    """
    # Store the lines we need in a list
    lines_to_keep = []
    with open(in_pdb_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.lower().startswith("atom"):
                lines_to_keep.append(line)

    if out_pdb_file is None:
        out_pdb_file = in_pdb_file

    # Write all the links in our list to the file
    with open(os.path.join(out_pdb_file), "w") as f:
        for line in lines_to_keep:
            f.write(line)

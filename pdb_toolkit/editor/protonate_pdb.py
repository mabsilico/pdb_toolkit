# -*- coding: utf-8 -*-
# @Time    : 22/09/2022 14:46
# @Author  : Raouf KESKES
# @Email   : raouf.keskes@mabsilico.com
# @File    : protonate_pdb.py

import subprocess
from .unprotonate_pdb import unprotonate_pdb


def protonate_pdb(in_pdb_file, out_pdb_file=None):
    """
    protonate (i.e., add hydrogens/protons H+) to a pdb
    @param in_pdb_file: (str) path to input pdb file
    @param out_pdb_file: (str) path to output pdb file
    """

    if out_pdb_file is None:
        out_pdb_file = in_pdb_file

    # Remove protons first, in case the structure is already protonated using the Trim
    unprotonate_pdb(in_pdb_file, out_pdb_file)

    # Now protonate correctly.
    cmd = ["reduce", "-BUILD", out_pdb_file]
    ps = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    std_out, std_err = ps.communicate()
    with open(out_pdb_file, "w") as outfile:
        outfile.write(std_out.decode('utf-8').rstrip())

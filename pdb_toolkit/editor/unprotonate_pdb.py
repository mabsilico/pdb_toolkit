# -*- coding: utf-8 -*-
# @Time    : 17/10/2022 10:40
# @Author  : Raouf KESKES
# @Email   : raouf.keskes@mabsilico.com
# @File    : unprotonate_pdb.py

import subprocess


def unprotonate_pdb(in_pdb_file, out_pdb_file=None):
    """
    unprotonate (i.e., remove hydrogens/protons H+) from a pdb
    @param in_pdb_file: (str) path to input pdb file
    @param out_pdb_file: (str) path to output pdb file
    """

    if out_pdb_file is None:
        out_pdb_file = in_pdb_file

    cmd = ["reduce", "-Trim", in_pdb_file]
    ps = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    std_out, std_err = ps.communicate()
    with open(out_pdb_file, "w") as outfile:
        outfile.write(std_out.decode('utf-8').rstrip())

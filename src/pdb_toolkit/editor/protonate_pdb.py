# -*- coding: utf-8 -*-
# @Time    : 22/09/2022 14:46
# @Author  : Raouf KESKES
# @Email   : raouf.keskes@mabsilico.com
# @File    : protonate_pdb.py
from subprocess import Popen, PIPE


def protonate_pdb(in_pdb_file, out_pdb_file=None):
    """
    protonate (i.e., add hydrogens/protons H+) to a pdb
    @param in_pdb_file: (str) path to input pdb file
    @param out_pdb_file: (str) path to output pdb file
    """

    if out_pdb_file is None:
        out_pdb_file = in_pdb_file

    # Remove protons first, in case the structure is already protonated using the Trim
    args = ["reduce", "-Trim", in_pdb_file]
    p2 = Popen(args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p2.communicate()
    outfile = open(out_pdb_file, "w")
    outfile.write(stdout.decode('utf-8').rstrip())
    outfile.close()

    # Now protonate correctly.
    args = ["reduce", "-BUILD", out_pdb_file]
    p2 = Popen(args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p2.communicate()
    outfile = open(out_pdb_file, "w")
    outfile.write(stdout.decode('utf-8'))
    outfile.close()

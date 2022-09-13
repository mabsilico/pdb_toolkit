# -*- coding: utf-8 -*-
# @Time    : 13/09/2022 10:08
# @Author  : Raouf KESKES
# @Email   : raouf.keskes@mabsilico.com
# @File    : align.py
from pymol import cmd


def align(src_pdb_file: str, dest_pdb_file: str, out_pdb_file=None):
    """
    @param src_pdb_file: (str) path to the mobile pdb file
    @param dest_pdb_file: (str) path to the target/destination/static pdb file
    @param out_pdb_file: (str) path to the output pdb file that saves the "aligned" src_pdb_file
    @return: (float) rmsd distance in angstrom between the "aligned" src_pdb_file and dest_pdb_file
    """
    # init
    if not out_pdb_file:
        out_pdb_file = src_pdb_file

    # align
    cmd.load(dest_pdb_file, object="dest_pdb")
    cmd.load(src_pdb_file, object="src_pdb")
    rmsd = cmd.align(mobile="src_pdb", target="dest_pdb")[0]

    # save
    cmd.save(out_pdb_file, selection="src_pdb")
    return rmsd

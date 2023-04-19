# -*- coding: utf-8 -*-
# @Time    : 13/09/2022 10:08
# @Author  : Raouf KESKES
# @Email   : raouf.keskes@mabsilico.com
# @File    : align.py

# generic
from typing import List

# data processing
from pymol import cmd


def align(src_pdb_file: str, dst_pdb_file: str, src_chain: str = None,
          dst_chains: List[str] = None, out_pdb_file: str = None) -> float:
    """

    @param src_pdb_file: (str) path to the mobile pdb file
    @param dst_pdb_file: (str) path to the target/destination/static pdb file
    @param src_chain:  (str) source chain selection for the alignment
    @param dst_chains: list[str] destination chains selection for the alignment
    @param out_pdb_file: (str) path to the output pdb file that saves the "aligned" src_pdb_file
    @return: (float) rmsd distance in angstrom between the "aligned" src_pdb_file and dest_pdb_file
    """
    # init
    if not out_pdb_file:
        out_pdb_file = src_pdb_file

    # format chains in pymol str format
    src_chains_str = " and "+("chain " + ", chain ".join(src_chain)).strip() if src_chain else ""
    dst_chains_str = " and "+("chain " + ", chain ".join(dst_chains)).strip() if dst_chains else ""

    # align
    cmd.load(src_pdb_file, object="src_pdb")
    cmd.load(dst_pdb_file, object="dst_pdb")
    rmsd = cmd.align(mobile="src_pdb" + src_chains_str, target="dst_pdb" + dst_chains_str)[0]

    # save
    cmd.save(out_pdb_file, selection="src_pdb")
    return rmsd

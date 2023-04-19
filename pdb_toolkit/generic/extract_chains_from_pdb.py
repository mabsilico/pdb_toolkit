# -*- coding: utf-8 -*-
# @Time    : 07/09/2022 15:10
# @Author  : Raouf KESKES
# @Email   : raouf.keskes@mabsilico.com
# @File    : extract_chains_from_pdb.py

from pymol import cmd

from pdb_toolkit.editor import renumber_pdb, keep_only_atom_lines, sort_atoms, protonate_pdb


def extract_chains_from_pdb(in_pdb_file, in_chains, out_pdb_file=None, out_chain=None,
                            keep_only_atoms=True, renumber=False, protonate=False, sort=False):
    """
    the method is used to extract chains from an input pdb and save them in a custom way

    @param in_pdb_file: (str) path to pdb input file
    @param in_chains: (list of str) the list of chains to retain from the in_pdb_file  ["V", "H"]
    @param out_pdb_file: (str) path to pdb output file
    @param out_chain: (str) output chain
    @param keep_only_atoms: (boolean) to keep only atom lines in the output PDB and remove all the metadata,
     default=True
    @param renumber: (boolean) to reindex the residues from 1 and increment for all the successive residues chain by
     chain, it is highly recommended to use it when ou set  'out_chain' parameter, default=False
    @param protonate: (boolean) protonate (i.e., add hydrogens/protons H+) to a pdb
    @param sort: (boolean) resort atoms for each residue in a correct order like N, CA, C, O, etc.vss
    """

    # init
    if not out_pdb_file:
        out_pdb_file = in_pdb_file

    cmd.load(in_pdb_file)
    in_chains_str = ("chain " + ", chain ".join(in_chains)).strip()
    # to avoid the confusing case where out_chain exists initially in in_pdb_file
    # we will save the intermediate extracted chains in a tmp file
    cmd.save(filename=out_pdb_file, selection=in_chains_str)
    cmd.reinitialize()
    cmd.load(out_pdb_file)

    # user introduce the same chain selection as input and output
    if len(in_chains) == 1 and in_chains[0] == out_chain:
        out_chain = None

    if out_chain:
        out_chains_str = "chain " + out_chain
        cmd.alter(in_chains_str, "chain='{}'".format(out_chain))
        cmd.save(filename=out_pdb_file, selection=out_chains_str)
        cmd.reinitialize()
        renumber=True

    cmd.reinitialize()

    if keep_only_atoms:
        keep_only_atom_lines(in_pdb_file=out_pdb_file, out_pdb_file=out_pdb_file)

    if protonate:
        protonate_pdb(out_pdb_file)

    if renumber:
        renumber_pdb(out_pdb_file)

    if sort:
        sort_atoms(out_pdb_file)

    if keep_only_atoms:
        keep_only_atom_lines(in_pdb_file=out_pdb_file, out_pdb_file=out_pdb_file)

# -*- coding: utf-8 -*-
# @Time    : 07/09/2022 15:40
# @Author  : Raouf KESKES
# @Email   : raouf.keskes@mabsilico.com
# @File    : fix_pdb.py
import os
import time

from openmm.app import PDBFile
from pdbfixer import PDBFixer


def fix_pdb(in_pdb_file, out_pdb_file=None, chains_to_keep=None, overwrite=False, verbose=False):
    """
        fix a pdb sing pdbfixer module :
        - filter useful chains if need
        - find missing and non standards residues
        - find missing atoms
        - fix everything

    @param in_pdb_file: (str) path to pdb input file
    @param out_pdb_file: (str) path to pdb output file
    @param chains_to_keep: (list of str) the list of chains to retain from the in_pdb_file  ["V", "H"]
    @param overwrite: (boolean) if out_pdb_file exists, whether to overwrite it or not
    @param verbose: (boolean) print information or not
    """

    # init
    pdb_id = os.path.splitext(os.path.basename(in_pdb_file))[0]
    if not out_pdb_file:
        out_pdb_file = in_pdb_file

    t = time.time()
    if overwrite or not os.path.exists(out_pdb_file):
        fixer = PDBFixer(filename=in_pdb_file)
        if chains_to_keep:
            chains_to_keep_set = set(chains_to_keep)
            chain_id_set = set([str(c.id) for c in fixer.topology.chains()])
            chain_ids_to_remove = chain_id_set - chains_to_keep_set
            fixer.removeChains(chainIds=chain_ids_to_remove)
        fixer.findMissingResidues()
        fixer.findNonstandardResidues()
        fixer.replaceNonstandardResidues()
        fixer.findMissingAtoms()
        fixer.addMissingAtoms()
        with open(out_pdb_file, 'w') as f:
            PDBFile.writeFile(topology=fixer.topology,
                              positions=fixer.positions,
                              file=f,
                              keepIds=True)
    if verbose:
        print("fixing {} tooks {} seconds".format(pdb_id, round(time.time() - t, 2)))

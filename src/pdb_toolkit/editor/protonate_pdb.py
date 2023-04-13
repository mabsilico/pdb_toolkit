# -*- coding: utf-8 -*-
# @Time    : 22/09/2022 14:46
# @Author  : Raouf KESKES
# @Email   : raouf.keskes@mabsilico.com
# @File    : protonate_pdb.py
import subprocess

from pdb_toolkit.editor import unprotonate_pdb


def protonate_pdb(input_pdb_path, output_pdb_path=None):
    """
    Add protons (hydrogens) to a PDB file.
    :param input_pdb_path: (str) Path to the input PDB file.
    :param output_pdb_path: (str) Path to the output PDB file. If None, overwrite the input file.
    """
    if output_pdb_path is None:
        output_pdb_path = input_pdb_path

    # unprotonate in case it is protonated before
    unprotonate_pdb(input_pdb_path, output_pdb_path)

    # Use reduce command to add protons to PDB
    build_args = ["reduce", "-BUILD", output_pdb_path]
    proc = subprocess.Popen(build_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    # Write output to file
    with open(output_pdb_path, "w") as out_file:
        out_file.write(stdout.decode('utf-8'))

# -*- coding: utf-8 -*-
# @Time    : 17/10/2022 10:40
# @Author  : Raouf KESKES
# @Email   : raouf.keskes@mabsilico.com
# @File    : unprotonate_pdb.py


import subprocess


def unprotonate_pdb(input_pdb_path, output_pdb_path=None):
    """
    Remove protons (hydrogens) from a PDB file.
    :param input_pdb_path: (str) Path to the input PDB file.
    :param output_pdb_path: (str) Path to the output PDB file. If None, overwrite the input file.
    """
    if output_pdb_path is None:
        output_pdb_path = input_pdb_path

    # Use reduce command to remove protons from PDB
    reduce_args = ["reduce", "-Trim", input_pdb_path]
    proc = subprocess.Popen(reduce_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    # Write output to file
    with open(output_pdb_path, "w") as out_file:
        out_file.write(stdout.decode('utf-8').rstrip())

    return output_pdb_path

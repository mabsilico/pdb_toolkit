# -*- coding: utf-8 -*-
# @Time    : 13/09/2022 15:28
# @Author  : Raouf KESKES
# @Email   : raouf.keskes@mabsilico.com
# @File    : concat_pdbs.py

# generic
import glob
import os


def concat_pdbs(in_pdb_files, out_pdb_file):
    list_pdb_files = ""
    # if it is a directory of files to concatenate
    try:
        list_pdb_files = glob.glob(in_pdb_files + "/*.pdb")
    except:
        # else it is a list of files
        list_pdb_files = in_pdb_files

    # print("cat {} >> {}".format(" ".join(list_pdb_files), out_pdb_file))
    os.system("cat {} > {}".format(" ".join(list_pdb_files), out_pdb_file))

# -*- coding: utf-8 -*-
# @Time    : 08/09/2022 12:20
# @Author  : Raouf KESKES
# @Email   : raouf.keskes@mabsilico.com
# @File    : download_pdb.py

# generic
import os
import re
import shutil
import urllib

import requests
import wget

# data processing
from Bio.PDB import PDBList


def download_pdb(pdb_id: str, out_path: str, overwrite: bool = False):
    """
    download a pdb from its pdb_id using 3 different servers :
       - "https://files.rcsb.org"
       - "http://ftp.wwpdb.org"
    @param pdb_id: (str) defining the pdb_id to download like "1A01" , "2W05", etc.
    @param out_path: (str) defining the output path in which the downloaded pdb will be saved
                     it could be a directory or a pdb file
    @param overwrite: (boolean) to overwrite existing files or not
    @return: (str) the downloaded pdb path
    """

    if re.fullmatch("^[0-9][a-zA-Z0-9]{3}$", pdb_id):

        pdb_id = pdb_id.lower()
        # init
        pdb_filename = pdb_id + ".pdb"

        # Check if out_path is a directory or a custom filename
        if not out_path.endswith(".pdb"):
            os.makedirs(out_path, exist_ok=True)
            out_file = os.path.join(out_path, f'{pdb_id}.pdb')
        else:
            out_file = out_path

        # check existence
        if os.path.exists(out_file) and not overwrite:
            print(f"The structure '{pdb_id}'exists ! if you want to overwrite it please use overwrite=True")
            return out_file

        # download from RCSB
        try:
            url = "http://files.rcsb.org/download/{}.pdb".format(pdb_id)
            response = requests.get(url)
            print(f"Downloading PDB structure '{pdb_id}'...")
            # Write the PDB file to the output path
            with open(out_file, 'wb') as f:
                f.write(response.content)
            return out_file
        # else download from sabdab
        except Exception as err1:
            try:
                out_dir = os.path.dirname(out_file)
                pdb_list = PDBList(obsolete_pdb=False)
                pdb_path = pdb_list.retrieve_pdb_file(pdb_code=pdb_id, pdir=out_dir, file_format='pdb',
                                                      overwrite=overwrite, obsolete=False)
                if os.path.exists(pdb_path):
                    shutil.move(pdb_path, out_file)
                return out_file
            except Exception as err2:
                raise Exception("Download failed ! " + str(err2))
    else:
        raise ValueError("pdb code format error ! please type a correct pdb code like '7f4h', '4O51', etc. ")

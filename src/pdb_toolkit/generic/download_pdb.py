# -*- coding: utf-8 -*-
# @Time    : 08/09/2022 12:20
# @Author  : Raouf KESKES
# @Email   : raouf.keskes@mabsilico.com
# @File    : download_pdb.py
import os
import sys
import urllib
import wget
from Bio.PDB import PDBList


def download_pdb(pdb_id: str, output_dir: str, overwrite=False):
    """
    download a pdb from its pdb_id using 3 different servers :
       - "https://files.rcsb.org"
       - "http://opig.stats.ox.ac.uk/webapps/newsabdab/sabdab/"
       - "http://ftp.wwpdb.org"
    @param pdb_id: (str) defining the pdb_id to download like "1A01" , "2W05", etc.
    @param output_dir: (str) defining the output directory in which the downloaded pdb will be saved
    @param overwrite: (boolean) to overwrite existing files or not
    @return: (str) the downloaded pdb path
    """
    # init
    pdb_filename = pdb_id + ".pdb"
    pdb_path = os.path.join(output_dir, pdb_filename)

    # check existence
    if os.path.exists(pdb_path) and not overwrite:
        return pdb_path

    # download from RCSB
    try:
        # print("rcsb")
        url = "http://files.rcsb.org/download/{}.pdb".format(pdb_id)
        urllib.request.urlretrieve(url, pdb_path)
        return pdb_path
    # else download from sabdab
    except Exception:
        try:
            # print("opig")
            url = 'http://opig.stats.ox.ac.uk/webapps/newsabdab/sabdab/pdb/{}/?raw=true'.format(pdb_id)
            wget.download(url, pdb_path)
            return pdb_path
        except Exception as error:
            try:
                # print("wwpdb")
                url = "http://ftp.wwpdb.org"
                pdb_list = PDBList(url)
                pdb_path = pdb_list.retrieve_pdb_file(pdb_id, pdir=output_dir, file_format='pdb',
                                                      overwrite=overwrite, obsolete=True)
                return pdb_path

            except Exception as err:
                raise Exception("Download failed ! "+str(error))

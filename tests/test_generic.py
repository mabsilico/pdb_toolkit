import os
import shutil
import tempfile
import unittest
import warnings

from pdb_toolkit.editor import keep_only_atom_lines
from pdb_toolkit.generic import *


class TestGeneric(unittest.TestCase):
    def setUp(self):
        self.root_files_dir = "tests/testing_data/7vyt"
        self.in_file = os.path.join(self.root_files_dir, '7vyt.pdb')
        self.in_file_fixed = os.path.join(self.root_files_dir, '7vyt_fixed.pdb')
        self.out_file = os.path.join(self.root_files_dir, 'out_test.pdb')
        self.Ab_A_file = os.path.join(self.root_files_dir, 'antibody_7vyt.pdb')
        self.Ag_T_file = os.path.join(self.root_files_dir, 'target_7vyt.pdb')
        self.AbAg_HLT_file = os.path.join(self.root_files_dir, 'complex_7vyt.pdb')
        self.splitted_chains = os.path.join(self.root_files_dir, "splitted_chains", '7vyt_{}.pdb')
        self.chains = ["A", "B", "C", "H", "L", "T"]

    def tearDown(self):
        os.remove(self.out_file)

    # def test_download_pdb(self):
    #     pdb_id = "7vyt"
    #     tmp_dir = tempfile.gettempdir()
    #     tmp_downloaded = os.path.join(tmp_dir, "{}.pdb".format(pdb_id))

    #     download_pdb(pdb_id="7vyt", out_path=tmp_dir)
    #     shutil.move(tmp_downloaded, self.out_file)
    #     with open(self.out_file, 'r') as f1, open(self.in_file, 'r') as f2:
    #         out_lines = f1.readlines()
    #         expct_lines = f2.readlines()
    #     self.assertEqual(out_lines, expct_lines)

        # download_pdb(pdb_id="7vyt", output_dir=tmp_dir, overwrite=True, fix=True)
        # shutil.move(tmp_downloaded, self.out_file)
        # keep_only_atom_lines(self.out_file)
        # keep_only_atom_lines(self.in_file_fixed)
        # with open(self.out_file, 'r') as f1, open(self.in_file_fixed, 'r') as f2:
        #     out_lines = f1.readlines()
        #     expct_lines = f2.readlines()
        # self.assertEqual(out_lines, expct_lines)

    def test_extract_chains_from_pdb(self):
        warnings.filterwarnings("ignore")
        extract_chains_from_pdb(in_pdb_file=self.in_file, in_chains=["H", "L"],
                                out_pdb_file=self.out_file, out_chain="A",
                                keep_only_atoms=True, renumber=True, protonate=False, sort=False)
        with open(self.out_file, 'r') as f1, open(self.Ab_A_file, 'r') as f2:
            out_lines = f1.readlines()
            expct_lines = f2.readlines()
        self.assertEqual(out_lines, expct_lines)

        extract_chains_from_pdb(in_pdb_file=self.in_file, in_chains=["T"],
                                out_pdb_file=self.out_file, out_chain="T",
                                keep_only_atoms=True, renumber=True, protonate=False, sort=False)

        with open(self.out_file, 'r') as f1, open(self.Ag_T_file, 'r') as f2:
            out_lines = f1.readlines()
            expct_lines = f2.readlines()
        self.assertEqual(out_lines, expct_lines)

    def test_concat_pdbs(self):
        concat_pdbs([self.Ab_A_file, self.Ag_T_file], self.out_file)
        with open(self.out_file, 'r') as f1, open(self.AbAg_HLT_file, 'r') as f2:
            out_lines = f1.readlines()
            expct_lines = f2.readlines()
        self.assertEqual(out_lines, expct_lines)

    def test_align(self):
        warnings.filterwarnings("ignore")
        extract_chains_from_pdb(in_pdb_file=self.in_file, in_chains=["A"],
                                out_pdb_file=self.out_file,
                                keep_only_atoms=True, renumber=True, protonate=False, sort=False)

        rmsd1 = align(src_pdb_file=self.out_file, dst_pdb_file=self.Ag_T_file)
        self.assertLessEqual(rmsd1, 0.5)

        extract_chains_from_pdb(in_pdb_file=self.in_file, in_chains=["B", "C"],
                                out_pdb_file=self.out_file,
                                keep_only_atoms=True, renumber=True, protonate=False, sort=False)

        rmsd2 = align(src_pdb_file=self.out_file, dst_pdb_file=self.Ab_A_file)
        self.assertLessEqual(rmsd2, 0.5)

        extract_chains_from_pdb(in_pdb_file=self.in_file, in_chains=["A", "B", "C"],
                                out_pdb_file=self.out_file,
                                keep_only_atoms=True, renumber=True, protonate=False, sort=False)

        rmsd3 = align(src_pdb_file=self.out_file,
                      src_chain="A",
                      dst_pdb_file=self.AbAg_HLT_file,
                      dst_chains=["T"])
        self.assertLessEqual(rmsd3, 0.5)

    def test_split_chains(self):
        warnings.filterwarnings("ignore")
        for chain in self.chains:
            extract_chains_from_pdb(in_pdb_file=self.in_file, in_chains=[chain],
                                    out_pdb_file=self.out_file,
                                    keep_only_atoms=True, renumber=False, protonate=False, sort=True)
            with open(self.out_file, 'r') as f1,\
                    open(self.splitted_chains.replace("{}", chain), 'r') as f2:
                out_lines = f1.readlines()
                expct_lines = f2.readlines()
            self.assertEqual(out_lines, expct_lines)

        
if __name__ == '__main__':
    unittest.main()
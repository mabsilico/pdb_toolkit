import unittest
from pdb_toolkit.editor import *
import os
import warnings


class TestEditor(unittest.TestCase):
    def setUp(self):
        self.root_files_dir = "tests/testing_data/7vyt"
        self.in_file = os.path.join(self.root_files_dir, "7vyt.pdb")
        self.out_file = os.path.join(self.root_files_dir, "out_test.pdb")
        self.expected_fixed = os.path.join(self.root_files_dir, "7vyt_fixed_HL_T.pdb")
        self.expected_only_atoms = os.path.join(self.root_files_dir, "7vyt_only_atoms.pdb")
        self.expected_protonated = os.path.join(self.root_files_dir, "7vyt_protonated.pdb")
        self.expected_unprotonated = os.path.join(self.root_files_dir, "7vyt_unprotonated.pdb")
        self.expected_sorted = os.path.join(self.root_files_dir, "7vyt_sorted.pdb")
        self.expected_renumbered = os.path.join(self.root_files_dir, "7vyt_renumbered.pdb")

    def tearDown(self):
        os.remove(self.out_file)

    def test_keep_only_atom_lines(self):
        keep_only_atom_lines(in_pdb_file=self.in_file,
                             out_pdb_file=self.out_file)
        with open(self.out_file, 'r') as f1, open(self.expected_only_atoms, 'r') as f2:
            out_lines = f1.readlines()
            expct_lines = f2.readlines()
        self.assertEqual(out_lines, expct_lines)

    def test_protonate(self):
        protonate_pdb(in_pdb_file=self.in_file,
                      out_pdb_file=self.out_file)
        with open(self.out_file, 'r') as f1, open(self.expected_protonated, 'r') as f2:
            out_lines = f1.readlines()
            expct_lines = f2.readlines()
        self.assertEqual(out_lines, expct_lines)

    def test_unprotonate(self):
        unprotonate_pdb(in_pdb_file=self.expected_protonated,
                        out_pdb_file=self.out_file)
        with open(self.out_file, 'r') as f1, open(self.expected_unprotonated, 'r') as f2:
            out_lines = f1.readlines()
            expct_lines = f2.readlines()
        self.assertEqual(out_lines, expct_lines)

    def test_sort_atoms(self):
        warnings.filterwarnings("ignore")
        sort_atoms(in_pdb_file=self.in_file,
                   out_pdb_file=self.out_file)
        with open(self.out_file, 'r') as f1, open(self.expected_sorted, 'r') as f2:
            out_lines = f1.readlines()
            expct_lines = f2.readlines()
        self.assertEqual(out_lines, expct_lines)

    def test_renumber(self):
        renumber_pdb(in_pdb_file=self.in_file,
                     out_pdb_file=self.out_file)
        with open(self.out_file, 'r') as f1, open(self.expected_renumbered, 'r') as f2:
            out_lines = f1.readlines()
            expct_lines = f2.readlines()
        self.assertEqual(out_lines, expct_lines)

    def test_fix_pdb(self):
        fix_pdb(in_pdb_file=self.in_file,
                out_pdb_file=self.out_file,
                chains_to_keep=['H', 'L', 'T'])
        keep_only_atom_lines(self.out_file)
        with open(self.out_file, 'r') as f1, open(self.expected_fixed, 'r') as f2:
            out_lines = f1.readlines()
            expct_lines = f2.readlines()

        self.assertEqual(out_lines, expct_lines)
        
        
        
if __name__ == '__main__':
    unittest.main()
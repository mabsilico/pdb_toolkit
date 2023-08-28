import os
import unittest
import warnings

from pdb_toolkit.parser import *


class TestParser(unittest.TestCase):

    def setUp(self):
        self.root_files_dir = "tests/testing_data/7vyt"
        self.in_file = os.path.join(self.root_files_dir, '7vyt.pdb')
        self.out_file = os.path.join(self.root_files_dir, 'out_test.pdb')
        self.Ab_A_file = os.path.join(self.root_files_dir, 'antibody_7vyt.pdb')
        self.Ag_T_file = os.path.join(self.root_files_dir, 'target_7vyt.pdb')

    def tearDown(self):
        if os.path.exists(self.out_file):
            os.remove(self.out_file)

    def test_get_atoms_residues(self):
        atoms_data, atoms_residues_data, sorted_residues = get_atoms_residues(self.Ag_T_file)

        # Check that the function returns the correct number of atoms, atoms_residues, and sorted residues
        self.assertEqual(len(atoms_data), 796)
        self.assertEqual(len(atoms_residues_data), 796)
        self.assertEqual(len(sorted_residues), 104)

        # Check that the first atom has the correct name, coordinates, and serial number
        self.assertEqual(atoms_data[0][0], 'N')
        self.assertAlmostEqual(atoms_data[0][1][0], 19.279, places=3)
        self.assertAlmostEqual(atoms_data[0][1][1], 76.324, places=3)
        self.assertAlmostEqual(atoms_data[0][1][2], 51.169, places=3)
        self.assertEqual(atoms_data[0][2], 1)
        # Check that the middle atom has the correct name, coordinates, and serial number
        self.assertEqual(atoms_data[365][0], 'O')
        self.assertAlmostEqual(atoms_data[365][1][0], 24.369, places=3)
        self.assertAlmostEqual(atoms_data[365][1][1], 67.663, places=3)
        self.assertAlmostEqual(atoms_data[365][1][2], 73.228, places=3)
        self.assertEqual(atoms_data[365][2], 366)
        # Check that the last atom has the correct name, coordinates, and serial number
        self.assertEqual(atoms_data[795][0], 'OE2')
        self.assertAlmostEqual(atoms_data[795][1][0], 34.518, places=3)
        self.assertAlmostEqual(atoms_data[795][1][1], 98.728, places=3)
        self.assertAlmostEqual(atoms_data[795][1][2], 81.404, places=3)
        self.assertEqual(atoms_data[795][2], 796)

        # Check that the first residue has the correct name, chain, and position
        self.assertEqual(atoms_residues_data[0][0], 'GLY')
        self.assertEqual(atoms_residues_data[0][1], 'T')
        self.assertEqual(atoms_residues_data[0][2], 1)
        # Check that the middle residue has the correct name, chain, and position
        self.assertEqual(atoms_residues_data[365][0], 'GLY')
        self.assertEqual(atoms_residues_data[365][1], 'T')
        self.assertEqual(atoms_residues_data[365][2], 50)
        # Check that the last residue has the correct name, chain, and position
        self.assertEqual(atoms_residues_data[795][0], 'GLU')
        self.assertEqual(atoms_residues_data[795][1], 'T')
        self.assertEqual(atoms_residues_data[795][2], 104)

        # Check the first sorted residue
        self.assertEqual(sorted_residues[0][0], 'GLY')
        self.assertEqual(sorted_residues[0][1], 'T')
        self.assertEqual(sorted_residues[0][2], 1)
        # # Check the middle sorted residue
        self.assertEqual(sorted_residues[49][0], 'GLY')
        self.assertEqual(sorted_residues[49][1], 'T')
        self.assertEqual(sorted_residues[49][2], 50)
        # Check the last sorted residue
        self.assertEqual(sorted_residues[103][0], 'GLU')
        self.assertEqual(sorted_residues[103][1], 'T')
        self.assertEqual(sorted_residues[103][2], 104)

    def test_get_pdb_centroid(self):
        # Call the function to get the centroid
        central_atom, central_residue = get_pdb_centroid(self.Ab_A_file)

        # Check the atom
        expected_central_atom = ('CH2', [39.802, 55.076, 66.088], 865)
        expected_central_residue = ('TRP', 'A', 112)
        self.assertEqual(central_atom[0], expected_central_atom[0])
        for i in range(len(expected_central_atom[1])):
            self.assertAlmostEqual(central_atom[1][i], expected_central_atom[1][i], delta=0.00001)
        self.assertEqual(central_atom[2], expected_central_atom[2])

        # check the residue
        self.assertEqual(central_residue, expected_central_residue)

    def test_get_pdb_sequence(self):

        expected_result_1 = {
            "A": "GTIETTGNISAEKGGSIILQCHLSSTTAQVTQVNWEQQDQLLAICNADLGWHISPSFKDRVAPGPGLGLTLQSLTVNDTGEYFCIYHTYPDGTYTGRIFLEVLES",
            "B": "EVQLVQSGAEVKKPGASVKVSCKASGYTFTSYYMHWVRQAPGQGLEWMGIINPSGGSTSYAQKFQGRVTMTRDTSTSTVYMELSSLRSEDTAVYYCASRSGSGWFGALDYWGQGTLVTVS",
            "C": "EIVLTQSPGTLSLSPGERATLSCRASQSVSSSYLAWYQQKPGQAPRLLIYGASSRATGIPDRFSGSGSGTDFTLTISRLEPEDFAVYYCQQYGSSPGGTFGQGTKVEIKR",
            "H": "EVQLVQSGAEVKKPGASVKVSCKASGYTFTSYYMHWVRQAPGQGLEWMGIIPSGGSTSYAQKFQGRVTMTRDTSTSTVYMELRSEDTAVYYCASRSGSGLDYWGQGTLVTVS",
            "L": "EIVLTQSPGTLSLSPGERATLSCRASSVSSSYLAWYQQKPGQAPRLLIYGASSRATGIPDRFSGSGSGTDFTLTISRLEPEDFAVYYCQQYGSSGGTFGQGTKVEIKR",
            "T": "GTIETTGNISAEKGGSIILQCHLSSTTAQVTQVNWEQQDQLLAICNADLGWHISPSFKDRVAPGPGLGLTLQSLTVNDTGEYFCIYHTYPDGTYTGRIFLEVLE"}

        expected_result_2 = {
            "A": "________________________GTIETTGNISAEKGGSIILQCHLSSTTAQVTQVNWEQQDQLLAICNADLGWHISPSFKDRVAPGPGLGLTLQSLTVNDTGEYFCIYHTYPDGTYTGRIFLEVLES",
            "B": "EVQLVQSGAEVKKPGASVKVSCKASGYTFTSYYMHWVRQAPGQGLEWMGIINPSGGSTSYAQKFQGRVTMTRDTSTSTVYMELSSLRSEDTAVYYCASRSGSGWFGALDYWGQGTLVTVS",
            "C": "EIVLTQSPGTLSLSPGERATLSCRASQSVSSSYLAWYQQKPGQAPRLLIYGASSRATGIPDRFSGSGSGTDFTLTISRLEPEDFAVYYCQQYGSSPGGTFGQGTKVEIKR",
            "H": "EVQLVQSGAEVKKPGASVKVSCKASGYTFTSYYMHWVRQAPGQGLEWMGIIPSGGSTSYAQKFQGRVTMTRDTSTSTVYMELRSEDTAVYYCASRSGSGLDYWGQGTLVTVS",
            "L": "EIVLTQSPGTLSLSPGERATLSCRASSVSSSYLAWYQQKPGQAPRLLIYGASSRATGIPDRFSGSGSGTDFTLTISRLEPEDFAVYYCQQYGSSGGTFGQGTKVEIKR",
            "T": "________________________GTIETTGNISAEKGGSIILQCHLSSTTAQVTQVNWEQQDQLLAICNADLGWHISPSFKDRVAPGPGLGLTLQSLTVNDTGEYFCIYHTYPDGTYTGRIFLEVLE"}

        result1 = get_pdb_sequence(self.in_file, ignore_missing=True)
        result2 = get_pdb_sequence(self.in_file, ignore_missing=False)
        result3 = get_pdb_sequence(self.in_file, chains=["A"], ignore_missing=True)
        result4 = get_pdb_sequence(self.in_file, chains=["A"], ignore_missing=False)

        self.assertDictEqual(expected_result_1, result1)
        self.assertDictEqual(expected_result_2, result2)
        self.assertEqual(expected_result_1["A"], result3["A"])
        self.assertEqual(expected_result_2["A"], result4["A"])

    def test_split_residues_surface_boundary_core(self):
        warnings.filterwarnings("ignore")
        # Test case 1
        surface, boundary, core = split_residues_surface_boundary_core(self.in_file)
        self.assertEqual(len(surface), 256)
        self.assertEqual(len(boundary), 135)
        self.assertEqual(len(core), 283)

        # Test case 2
        surface, boundary, core = split_residues_surface_boundary_core(self.Ab_A_file)
        self.assertEqual(len(surface), 100)
        self.assertEqual(len(boundary), 41)
        self.assertEqual(len(core), 91)

        # Test case 3
        surface, boundary, core = split_residues_surface_boundary_core(self.Ag_T_file)
        self.assertEqual(len(surface), 50)
        self.assertEqual(len(boundary), 27)
        self.assertEqual(len(core), 27)

    # def test_detect_steric_clashes(self):
    #     warnings.filterwarnings("ignore")
    #     download_pdb(pdb_id="7nd4", out_path=self.root_files_dir, overwrite=False)
    #     expected_lens = [1, 1, 18, 49]
    #     i = 0
    #     for param1 in [True, False]:
    #         for param2 in [True, False]:
    #             ls = detect_steric_clashes(in_pdb_file=os.path.join(self.root_files_dir, "7nd4.pdb"),
    #                                        first_occurrence=param1, different_chain_only=param2)
    #             self.assertEqual(expected_lens[i], len(ls))
    #             i += 1



        
if __name__ == '__main__':
    unittest.main()
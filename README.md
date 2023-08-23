# pdb_toolkit
pdb_toolkit is an open-source python library that helps to manipulate pdb protein
files easily and smoothly with an extensive list of functions and tools, the
purpose of each tool could be inferred by its name, you could check the examples below 
for further details

the library is divided into 3 packages:
* **generic**: where the tools are general-purpose such as downloading a pdb,
or concatenating a list of pdbs or aligning a pdb on another pdb or ...
* **editor**: where the tools are dedicated to edit a pdb file for instance :
fixing/repairing a pdb, protonating a pdb, keeping only ATOM lines, sorting atoms, etc.
* **parser**: where the tools are dedicated to extract relevant information from a pdb,
such as extracting a specific chain, getting the sequence,

## Requirements



[//]: # ()
[//]: # (|        | 3.6     | 3.7 | 3.8 | 3.9 | 3.10    |)

[//]: # (|--------|---------|-----|-----|-----|---------|)

[//]: # (| python | passed 	✅ | passed 	✅ | passed 	✅ |     | Failed 🔴 |)


1) **python3**
2) **gcc** ```conda install -c conda-forge gcc```
2) **pymol**
   - < 2.5 (recommended)``` conda install -c schrodinger pymol ```
   - \>= 2.5 ``` conda install -c conda-forge -c schrodinger pymol-bundle```
3) **pdbfixer** ``` conda install -c conda-forge pdbfixer ```
4) **biopython**  ``` conda install -c conda-forge biopython
5) **dssp**  ```conda install -c salilab dssp```
5) **reduce** ``` conda install -c mx reduce ```
6) **scikit-learn** ```conda install -c conda-forge scikit-learn```
7) **wget**  ```pip install wget```

## Installation
git:
```
git clone https://github.com/raoufkeskes/pdb_toolkit && pip install ./pdb_toolkit/ && rm -rf ./pdb_toolkit/
```

pip:
```
pip install pdb-toolkit
```

conda:
```
TO DO
```
## Test

After installing make sure that everything is running correctly 

all in one : 
```commandline
bash tests/all_in_one.sh
```

one by one :

```commandline
python -m unittest tests/test_generic.py
```

```commandline
python -m unittest tests/test_editor.py
```

```commandline
python -m unittest tests/test_parser.py
```
## Usage

**1) generic**

```python
import os
import warnings

from pdb_toolkit.editor import fix_pdb
from pdb_toolkit.generic import *

warnings.filterwarnings("ignore")

work_dir = "./tests/testing_data/7nd4"

# download pdbs  and fix it if you want (we highly recommend it)
download_pdb(pdb_id="7nd4", out_path=work_dir, overwrite=True)

# extract specific chains
extract_chains_from_pdb(
    in_pdb_file=os.path.join(work_dir, "7nd4.pdb"),
    in_chains=["H", "L"],
    out_pdb_file=os.path.join(work_dir, "antibody_7nd4.pdb"),
    out_chain="A",
    keep_only_atoms=True,
    renumber=True,
    sort=True,
    protonate=False,
)

# extract specific chains
extract_chains_from_pdb(
    in_pdb_file=os.path.join(work_dir, "7nd4.pdb"),
    in_chains=["F", "G"],
    out_pdb_file=os.path.join(work_dir, "antibody2_7nd4.pdb"),
    keep_only_atoms=True,
    renumber=True,
    sort=True,
    protonate=False,
)

extract_chains_from_pdb(
    in_pdb_file=os.path.join(work_dir, "7nd4.pdb"),
    in_chains=["A", "B", "C"],
    out_pdb_file=os.path.join(work_dir, "target_7nd4.pdb"),
    out_chain="T",
    keep_only_atoms=True,
    renumber=True,
    sort=True,
    protonate=False,
)

# decompose a pdb and extract all chains
split_chains(in_pdb_file=os.path.join(work_dir, "7nd4.pdb"),
             output_dir=os.path.join(work_dir, "splitted_chains"))

# concat specific pdbs
concat_pdbs(in_pdb_files=[os.path.join(work_dir, "antibody_7nd4.pdb"),
                          os.path.join(work_dir, "target_7nd4.pdb")],
            out_pdb_file=os.path.join(work_dir, "complex_7nd4.pdb"))

# concat an entire directory containing pdbs
concat_pdbs(in_pdb_files=os.path.join(work_dir, "splitted_chains"),
            out_pdb_file=os.path.join(work_dir, "7nd4_concatenated.pdb"))

rmsd = align(
    src_pdb_file=os.path.join(work_dir, "antibody_7nd4.pdb"),
    src_chain="A",
    dst_pdb_file=os.path.join(work_dir, "antibody2_7nd4.pdb"),
    dst_chains=["F", "G"],
    out_pdb_file=os.path.join(work_dir, "antibody_7nd4_aligned.pdb")
)
print(f"RMSD : {rmsd}")
```

**2) editor**

```python
import os
import warnings
from pdb_toolkit.editor import *
from pdb_toolkit.generic import download_pdb

warnings.filterwarnings("ignore")

pdb_id = "7wsl"
work_dir = f"./tests/testing_data/{pdb_id}"

download_pdb(pdb_id=pdb_id, out_path=work_dir, overwrite=True)

# fix missing residues, atoms and other pdb problems etc.
# DISCLAIMER : FIXING COULD TAKE FROM FEW SECONDS TO FEW MINUTES IT DEPENDS ON THE STRUCTURE
fix_pdb(in_pdb_file=os.path.join(work_dir, f"{pdb_id}.pdb"),
        out_pdb_file=os.path.join(work_dir, f"{pdb_id}_D_fixed.pdb"),
        chains_to_keep=["D"],
        overwrite=True,
        verbose=True)

# protonate
protonate_pdb(in_pdb_file=os.path.join(work_dir, f"{pdb_id}_D_fixed.pdb"),
              out_pdb_file=os.path.join(work_dir, f"{pdb_id}_D_fixed_protonated.pdb"))

# #unprotonate
unprotonate_pdb(in_pdb_file=os.path.join(work_dir, f"{pdb_id}_D_fixed_protonated.pdb"),
                out_pdb_file=os.path.join(work_dir, f"{pdb_id}_D_fixed_unprotonated.pdb"))

# remove all meta data lines from pdb file and keep exclusively ATOM lines
keep_only_atom_lines(in_pdb_file=os.path.join(work_dir, f"{pdb_id}_D_fixed_protonated.pdb"),
                     out_pdb_file=os.path.join(work_dir, f"{pdb_id}_D_fixed_protonated_only_atoms.pdb"))

# sort atoms inside the pdb
sort_atoms(in_pdb_file=os.path.join(work_dir, f"{pdb_id}_D_fixed_protonated_only_atoms.pdb"),
           out_pdb_file=os.path.join(work_dir, f"{pdb_id}_D_fixed_protonated_only_atoms_sorted.pdb"))

# renumber/reindex all the residues in a pdb, chain by chain, starting from 1
renumber_pdb(in_pdb_file=os.path.join(work_dir, f"{pdb_id}_D_fixed_protonated_only_atoms_sorted.pdb"),
             out_pdb_file=os.path.join(work_dir, f"{pdb_id}_D_fixed_protonated_only_atoms_sorted_renumbered.pdb"))

```

**3) parser**


```python

import os
import time
import warnings
from pdb_toolkit.parser import *
from pdb_toolkit.generic import download_pdb, extract_chains_from_pdb

warnings.filterwarnings("ignore")

pdb_id = "7wsl"
work_dir = f"./tests/testing_data/{pdb_id}"


# 0)  init 
download_pdb(pdb_id=pdb_id, out_path=work_dir, overwrite=False)
extract_chains_from_pdb(in_pdb_file=os.path.join(work_dir, f"{pdb_id}.pdb"),
                        in_chains=["D"],
                        out_pdb_file=os.path.join(work_dir, f"{pdb_id}_D.pdb"),
                        keep_only_atoms=True,
                        renumber=False,
                        sort=True,
                        protonate=False)

# 1) get_pdb_sequence
sequences = get_pdb_sequence(os.path.join(work_dir, f"{pdb_id}.pdb"), ignore_missing=True)
print(sequences)
"""
{
    'H': 'EVQLLESGGGLVQPGGSLRLSCAASGFTFSSYDMSWVRQAPGKGLEWVSTISGGGSYTYYQDSVKGRFTISRDNSKNTLYLQMNSLRAEDTAVYYCASPYYAMDYWGQGTTVTVSSASTKGPSVFPLAPGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKKVEP',
    'L': 'DIQLTQSPSFLSAYVGDRVTITCKASQDVGTAVAWYQQKPGKAPKLLIYWASTLHTGVPSRFSGSGSGTEFTLTISSLQPEDFATYYCQHYSSYPWTFGQGTKLEIKRTVAAPSVFIFPPSDEQLKSGTASVVCLLNNFYPREAKVQWKVDNALQSGNSQESVTEQDSKDSTYSLSSTLTLSKADYEKHKVYACEVTHQGLSSPVTKSFNRG',
    'D': 'PWNPPTFSPALLVVTEGDNATFTCSFSNTSESFVLNWYRMSPSNQTDKLAAFPEDRSQSRFRVTQLPNGRDFHMSVVRARRNDSGTYLCGAISLAPKAQIKESLRAELRVTER'
}
# """

sequences = get_pdb_sequence(os.path.join(work_dir, f"{pdb_id}.pdb"), ignore_missing=False)
print(sequences)
"""
{
    'H': 'EVQLLESGGGLVQPGGSLRLSCAASGFTFSSYDMSWVRQAPGKGLEWVSTISGGGSYTYYQDSVKGRFTISRDNSKNTLYLQMNSLRAEDTAVYYCASPYYAMDYWGQGTTVTVSSASTKGPSVFPLAP_______GTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKKVEP',
    'L': 'EVQLLESGGGLVQPGGSLRLSCAASGFTFSSYDMSWVRQAPGKGLEWVSTISGGGSYTYYQDSVKGRFTISRDNSKNTLYLQMNSLRAEDTAVYYCASPYYAMDYWGQGTTVTVSSASTKGPSVFPLAP_______GTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKKVEP',
    'D': '______________________________PWNPPTFSPALLVVTEGDNATFTCSFSNTSESFVLNWYRMSPSNQTDKLAAFPEDRSQ____SRFRVTQLPNGRDFHMSVVRARRNDSGTYLCGAISLAPKAQIKESLRAELRVTER'
}
# """

# 2) get pdb  centroid
central_atom, central_residue = get_pdb_centroid(os.path.join(work_dir, f"{pdb_id}_D.pdb"))

print("central atom of the chain D : ", central_atom)
print("central residue of the chain D: ", central_residue)

"""
central atom :  ('CD1', array([ 0.323, -0.531,  1.606], dtype=float32), 280)
central residue :  ('TRP', 'D', 67)
"""

# 3) get all the atoms and residues information from a pdb to a list
atoms_data, atoms_residues_data, sorted_residues = get_atoms_residues(os.path.join(work_dir, f"{pdb_id}_D.pdb"),
                                                                      sort_residues=True)
print("number of atoms : ", len(atoms_data))
print(atoms_data[0])
print(atoms_data[-1])

print("number of atoms_residues : ", len(atoms_residues_data))
print(atoms_residues_data[0])
print(atoms_residues_data[-1])

print("number of unique sorted residues : ", len(sorted_residues))
print(sorted_residues[0])
print(sorted_residues[-1])

"""
number of atoms :  896
('N', array([-12.107,  20.104,   6.297], dtype=float32), 1)
('NH2', array([  4.976, -14.999, -12.652], dtype=float32), 896)
number of atoms_residues :  896
('PRO', 'D', 31)
('ARG', 'D', 147)
number of unique sorted residues :  113
('PRO', 'D', 31)
('ARG', 'D', 147)
"""

# 4) split residues into surface, core and in between
surf_res_idxs, bndr_res_idx, core_res_idxs = split_residues_surface_boundary_core(
    os.path.join(work_dir, f"{pdb_id}_D.pdb"))

print("number of surface residues : ", len(surf_res_idxs))
print("number of boundary residues : ", len(bndr_res_idx))
print("number of core residues : ", len(core_res_idxs))

"""
number of surface residues :  56
number of boundary residues :  31
number of core residues :  26
"""

# 5) Detect steric clashes
for first_occurrence in [True, False]:
    for different_chain_only in [True, False]:
        t0 = time.time()
        res = detect_steric_clashes(os.path.join(work_dir, f"{pdb_id}.pdb"), first_occurrence, different_chain_only)

        print(f"first_occurrence={first_occurrence}, different_chain_only={different_chain_only}")
        print(f"count steric clashes : {len(res)}")
        print(f"computation time in seconds : {time.time() - t0} s")
        print("-----------------------------------------------")


"""
first_occurrence=True, different_chain_only=True
count steric clashes : 0
computation time in seconds : 12.59 s
-----------------------------------------------
first_occurrence=True, different_chain_only=False
count steric clashes : 1
computation time in seconds : 7.39 s
-----------------------------------------------
first_occurrence=False, different_chain_only=True
count steric clashes : 0
computation time in seconds : 12.49 s
-----------------------------------------------
first_occurrence=False, different_chain_only=False
count steric clashes : 7
computation time in seconds : 19.84 s
-----------------------------------------------
"""

```



## Authors

- **Raouf KESKES** : [Github](https://github.com/raoufkeskes)   [Linkedin](https://www.linkedin.com/in/raouf-keskes/)
[Email](mailto:raoufkeskes@gmail.com)



## License
[MIT](https://choosealicense.com/licenses/mit/)
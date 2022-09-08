# pdb_toolkit
a project to manipulate pdb files

**a more detail documentation is coming**




## Requirements

1) **Python >= 3.6**
2) **pdbfixer** ``` conda install -c conda-forge pdbfixer ```
2) **biopython**  ``` conda install -c conda-forge biopython ```
3) **pymol**  ``` conda install -c schrodinger pymol ```
4) **wget**  ```pip install wget```

## Installation
```
git clone https://github.com/raoufkeskes/pdb_toolkit
cd pdb_toolkit
pip install .
```

## Usage

the library is divided into 3 packages 


**1) generic**
```python
from pdb_toolkit.generic import download_pdb, extract_chains_from_pdb


download_pdb(pdb_id="7nd4", output_dir="./Downloads/", overwrite=True)

extract_chains_from_pdb(
        in_pdb_file="./Downloads/7nd4.pdb",
        in_chains=["H", "L"],
        out_pdb_file="./Downloads/7nd4_antibody.pdb",
        out_chain=["A"],
        keep_only_atoms=True,
        renumber=True
    )
```

**2) fixer**
```python

from pdb_toolkit.fixer import fix_pdb, sort_atoms, renumber_pdb, keep_only_atom_lines

# fix missing residues, atoms and other pdb problems etc.
fix_pdb(in_pdb_file="./Downloads/7nd4.pdb",
        out_pdb_file="./Downloads/7nd4_A.pdb",
        chains_to_keep=["A"],
        overwrite=False,
        verbose=True)

# remove all meta data lines from pdb file and keep exclusively ATOM lines
keep_only_atom_lines(in_pdb_file="./Downloads/7nd4_A_fixed.pdb",
                     out_pdb_file="./Downloads/7nd4_A_only_atoms.pdb")

# sort atoms inside the pdb
sort_atoms(in_pdb_file="./Downloads/7nd4_A_only_atoms.pdb",
           out_pdb_file="./Downloads/7nd4_A_only_atoms_sorted.pdb")

# renumber/reindex all the residues in a pdb, chain by chain, starting from 1
renumber_pdb(in_pdb_file="./Downloads/7nd4_A_only_atoms_sorted.pdb",
             out_pdb_file="./Downloads/7nd4_A_only_atoms_sorted_renumbered.pdb")

```

**3) parser**

```python
from pdb_toolkit.parser import get_pdb_sequence

sequences = get_pdb_sequence("./Downloads/7nd4_HL_sorted.pdb")

print(sequences)
"""
{'H': '____QESGPGLVKPSQTLSLTCTVSGGSISSGSYNWTWIRQPAGKGLEWIGRIYNSGSTNYNPSLKSRVTISVDTSKNQLSLKVRSVTAADTAVYYCARHCSGGTCYPKYYYGMDVWGQGTTVTVSSA',
 'L': '___LTQPPSVSEAPRQRVTISCSGSSSNIGNNAVNWYQQFPGKAPKLLIYYDDLLPSGVSDRFSGSKSGTSASLAISGVQSEDEADYYCAAWDDSLNVVVFGGGTK____GQP'}
"""

sequences = get_pdb_sequence("./Downloads/7nd4_HL_sorted.pdb", ignore_missing=True)

print(sequences)
"""
{'H': 'QESGPGLVKPSQTLSLTCTVSGGSISSGSYNWTWIRQPAGKGLEWIGRIYNSGSTNYNPSLKSRVTISVDTSKNQLSLKVRSVTAADTAVYYCARHCSGGTCYPKYYYGMDVWGQGTTVTVSSA',
 'L': 'LTQPPSVSEAPRQRVTISCSGSSSNIGNNAVNWYQQFPGKAPKLLIYYDDLLPSGVSDRFSGSKSGTSASLAISGVQSEDEADYYCAAWDDSLNVVVFGGGTKGQP'}
"""
```
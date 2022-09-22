# pdb_toolkit
a project to manipulate pdb files

**a more detail documentation is coming**




## Requirements

1) **Python >= 3.6**
2) **pdbfixer** ``` conda install -c conda-forge pdbfixer ```
2) **biopython**  ``` conda install -c conda-forge biopython ```
3) **pymol**  ``` conda install -c schrodinger pymol ```
4) **reduce** ``` conda install -c mx reduce ```
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
from pdb_toolkit.generic import download_pdb, extract_chains_from_pdb, concat_pdbs, align

download_pdb(pdb_id="7nd4", output_dir="./Downloads/", overwrite=True)

extract_chains_from_pdb(
    in_pdb_file="./Downloads/7nd4.pdb",
    in_chains=["H", "L"],
    out_pdb_file="/PATH/TO/OUTDIR/7nd4_antibody.pdb",
    out_chain=["A"],
    keep_only_atoms=True,
    renumber=True
)

# concatenating a list of pdb files
root_path = "PATH/TO/PDBs/"
concat_pdbs(
    in_pdb_files=[root_path + "antibody_1.pdb", root_path + "target_1.pdb"],
    out_pdb_file="/PATH/TO/OUTDIR/complex_1_concat.pdb"
)
# concatenating an entire folder of pdbs
to_concat_path = "PATH/TO/TO_CONCAT_PDBs/pdb_chains/"
concat_pdbs(
    in_pdb_files=to_concat_path,
    out_pdb_file="/PATH/TO/OUTDIR/complex_1_concat.pdb"
)

rmsd = align(
    src_pdb_file="/PATH/TO/complex_1.pdb",
    src_chains=["A"],
    dst_pdb_file="/PATH/TO/complex_2.pdb",
    dst_chains=["A"],
    out_pdb_file="/PATH/TO/OUTDIR/out_aligned.pdb"
)
print("RMSD : {} Å".format(rmsd))


```

**2) fixer**
```python

from pdb_toolkit.fixer import fix_pdb, sort_atoms, renumber_pdb, keep_only_atom_lines, protonate

# fix missing residues, atoms and other pdb problems etc.
fix_pdb(in_pdb_file="./Downloads/7nd4.pdb",
        out_pdb_file="./Downloads/7nd4_A_fixed.pdb",
        chains_to_keep=["A"],
        overwrite=False,
        verbose=True)

#protonate 
protonate(in_pdb_file="./Downloads/7nd4_A_fixed.pdb",
          out_pdb_file="./Downloads/7nd4_A_fixed_protonated.pdb")

# remove all meta data lines from pdb file and keep exclusively ATOM lines
keep_only_atom_lines(in_pdb_file="./Downloads/7nd4_A_fixed_protonated.pdb",
                     out_pdb_file="./Downloads/7nd4_A_only_atoms.pdb")

# sort atoms inside the pdb
sort_atoms(in_pdb_file="./Downloads/7nd4_A_only_atoms.pdb",
           out_pdb_file="./Downloads/7nd4_A_only_atoms_sorted.pdb")

# renumber/reindex all the residues in a pdb, chain by chain, starting from 1
renumber_pdb(in_pdb_file="./Downloads/7nd4_A_only_atoms_sorted.pdb",
             out_pdb_file="./Downloads/7nd4_A_only_atoms_sorted_renumbered.pdb")

```

**3) parser**

get_pdb_sequence : 
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


detect steric clashes:
```python

from pdb_toolkit.parser import detect_steric_clash


res = detect_steric_clash("/PATH/TO/complex_ATI_285_Ab14.pdb",
                          different_chain_only=True,
                          first_occurrence=False)

for steric_clash in res:
    print(steric_clash)

"""
(<Residue TYR het=  resseq=112 icode= >, <Residue SER het=  resseq=55 icode= >)
(<Residue TYR het=  resseq=112 icode= >, <Residue ILE het=  resseq=56 icode= >)
(<Residue ASN het=  resseq=176 icode= >, <Residue TRP het=  resseq=315 icode= >)
(<Residue THR het=  resseq=179 icode= >, <Residue ALA het=  resseq=59 icode= >)
(<Residue THR het=  resseq=179 icode= >, <Residue HIS het=  resseq=61 icode= >)

"""
```

split pdb chains : 
```python

from pdb_toolkit.generic import download_pdb
from pdb_toolkit.parser import split_chains


download_pdb(pdb_id="4o51", output_dir="/PATH/TO/")
split_chains(
    in_pdb_file="/PATH/TO/4o51.pdb",
    output_dir="/PATH/TO/OUTDIR/"
)
```

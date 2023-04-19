# Correspondance between the 3 and the 1 letter representation for the 20 amino acids
d3to1 = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
         'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N',
         'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W',
         'ALA': 'A', 'VAL': 'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}

# Correspondance between the 1 and the 3 letters representation for the 20 amino acids
d1to3 = {'C': 'CYS', 'D': 'ASP', 'S': 'SER', 'Q': 'GLN', 'K': 'LYS',
         'I': 'ILE', 'P': 'PRO', 'T': 'THR', 'F': 'PHE', 'N': 'ASN',
         'G': 'GLY', 'H': 'HIS', 'L': 'LEU', 'R': 'ARG', 'W': 'TRP',
         'A': 'ALA', 'V': 'VAL', 'E': 'GLU', 'Y': 'TYR', 'M': 'MET'}

# secondary structure mapper 
dssp_mapper = {"G": "H", "H": "H", "I": "H", "B": "S", "E": "S", "S": "L", "T": "L", "P": "L", "-": "L"}

# residue weights to split the surface from the core
res_weights = {
    'CYS': 167, 'ASP': 193, 'SER': 155, 'GLN': 225, 'LYS': 236,
    'ILE': 197, 'PRO': 159, 'THR': 172, 'PHE': 240, 'ASN': 195,
    'GLY': 104, 'HIS': 224, 'LEU': 201, 'ARG': 274, 'TRP': 285,
    'ALA': 129, 'VAL': 174, 'GLU': 223, 'TYR': 263, 'MET': 224
}


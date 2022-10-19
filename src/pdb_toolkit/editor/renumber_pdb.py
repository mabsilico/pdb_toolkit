# -*- coding: utf-8 -*-
# @Time    : 07/09/2022 15:06
# @Author  : Raouf KESKES
# @Email   : raouf.keskes@mabsilico.com
# @File    : renumber_pdb.py


def renumber_pdb(in_pdb_file, out_pdb_file=None):
    """
    renumber/reindex all the residues in a pdb, chain by chain, starting from 1
    @param in_pdb_file: (str) path to pdb input file
    @param out_pdb_file: (str) path to pdb output file
    """

    # init
    if not out_pdb_file:
        out_pdb_file = in_pdb_file

    new_lines = []
    with open(in_pdb_file, "r") as f:
        lines = f.readlines()
        prev_chain, prev_res, prev_letter, prev_idx, prev_pdb_pos = "", "", "", 1, 1
        curr_chain, curr_res, curr_pdb_pos, curr_letter = "", "", 0, ""
        for line in lines:
            if line.startswith("ATOM"):
                prev_chain, prev_res, prev_pdb_pos, prev_letter = curr_chain, curr_res, curr_pdb_pos, curr_letter
                curr_res, curr_chain, curr_pdb_pos, curr_letter = line[17:21], line[21], int(line[22:26]), line[26]

                # we could just consider the pdb position to assume same residue but it is ok to endorse this condition
                same_residue = (curr_res == prev_res and curr_pdb_pos == prev_pdb_pos
                                and curr_letter == prev_letter)

                if curr_chain == prev_chain and same_residue:
                    curr_idx = prev_idx
                elif curr_chain != prev_chain:
                    curr_idx = prev_idx = 1
                elif not same_residue:
                    curr_idx = prev_idx + 1
                    prev_idx = curr_idx

                # print((curr_chain, curr_res, str(curr_idx).rjust(4)))
                new_line = list(line)
                new_line[22:26] = list(str(curr_idx).rjust(4))
                new_line[26] = " "
                new_line = "".join(new_line)

                new_lines.append(new_line)

    with open(out_pdb_file, "w") as f:
        f.writelines(new_lines)
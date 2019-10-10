import re

edge_splitter =re.compile("\s+")

#ccs_1_4194529   @m54238_180901_011437/4194529/ccs   3   chr1:19248531_G_A_a;chr1:19255094_T_C_a
def parse_edge_map(edge_map_str):
    (id, rid, hid, edge) = re.split(edge_splitter, edge_map_str)
    return [ hid, rid, parse_chr_loc(edge) ]

#-- parse_edge_map

def parse_chr_loc(loc):
    (start, stop) = loc.split(";")
    return [ parse_chr_pos(start), parse_chr_pos(stop) ]

#-- parse_chr_loc

def parse_chr_pos(pos):
    tokens = pos.split("_")
    chr_and_pos = tokens.pop(0).split(":")
    return chr_and_pos + tokens

#-- parse_chr_pos

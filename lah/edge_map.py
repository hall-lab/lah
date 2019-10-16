import re

edge_splitter =re.compile("\s+")

class EdgeMap():
    def __init__(self, hid, rid):
        self.hid = hid
        self.rid = rid

#-- EdgeMap

def parse_edge_map(line):
    line = line.rstrip()
    (short_rid, rid, hid) = re.split(edge_splitter, line)
    if rid.startswith("@"):
        rid = rid[1:]
    return EdgeMap(hid=hid, rid=rid)

#-- parse_edge_map

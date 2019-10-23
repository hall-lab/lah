import re

edge_splitter =re.compile("\s+")

class HaplotypeIterator():
    def __init__(self, edge_map_fn):
        self.edge_map_f = open(edge_map_fn, "r")
        line = self.edge_map_f.readline()
        line = line.rstrip()
        self.prev_edge = self.parse_edge_map(line)

    def __del__(self):
        self.edge_map_f.close()

    def __iter__(self):
        return self

    def __next__(self):
        if not self.prev_edge:
            raise StopIteration()

        hid = self.prev_edge["hid"]
        rids = [self.prev_edge["rid"]]
        self.prev_edge = None
        while True:
            line = self.edge_map_f.readline()
            if not line: # EOF
                break
            edge = self.parse_edge_map(line)
            if edge["hid"] != hid: # new haplotype, save edge, break to return haplotype
                self.prev_edge = edge
                break
            else:
                rids.append(edge["rid"])

        if len(rids) > 0:
            return {"hid": hid, "rids": rids}
        else:
            raise StopIteration()

    @staticmethod
    def parse_edge_map(line):
        line = line.rstrip()
        (short_rid, rid, hid) = re.split(edge_splitter, line)
        if rid.startswith("@"):
            rid = rid[1:]
        return {"hid": str(hid), "rid": rid}

#-- HaplotypeIterator

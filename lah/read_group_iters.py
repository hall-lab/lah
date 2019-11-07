import re

edge_splitter = re.compile("\s+")

class ReadGroupIterator():
    def __init__(self, in_fn):
        self.in_f = open(in_fn, "r")
        line = self.in_f.readline()
        line = line.rstrip()
        self.prev = self.parse_line(line)

    def __del__(self):
        self.in_f.close()

    def __iter__(self):
        return self

    def __next__(self):
        if not self.prev:
            raise StopIteration()

        rg_id = self.prev["rg_id"]
        rids = [self.prev["rid"]]
        self.prev = None
        while True:
            line = self.in_f.readline()
            if not line: # EOF
                break
            rg = self.parse_line(line)
            if rg["rg_id"] != rg_id: # save read group, break to return read_group
                self.prev = rg
                break
            else:
                rids.append(rg["rid"])

        if len(rids) > 0:
            rids.sort()
            return {"rg_id": rg_id, "rids": rids}
        else:
            raise StopIteration()

    @staticmethod
    def parse_line(line):
        line = line.rstrip()
        (short_rid, rid, rg_id) = re.split(edge_splitter, line)
        if rid.startswith("@"):
            rid = rid[1:]
        return {"rg_id": str(rg_id), "rid": rid}

#-- ReadGroupIterator

import lah.edge_map

class Haplotype():
    def __init__(self, id, rids):
        self.id = str(id)
        self.rids = rids

    def __len__(self):
        raise Exception("FIXME")

    def from_edges(edges):
        hids = set()
        rids = set()
        for edge in edges:
            hids.add(edge.hid)
            rids.add(edge.rid)
        if len(hids) != 1:
            raise Exception("Multiple haplotypes in edges! {}".format(hids))
        return Haplotype(id=hids.pop(), rids=rids)

    def reads(self):
        rds = list(self.rids)
        rds.sort()
        return rds

#-- Haplotype

class HaplotypeIterator():
    def __init__(self, edge_map_fn):
        self.edge_map_f = open(edge_map_fn, "r")
        line = self.edge_map_f.readline()
        line = line.rstrip()
        self.prev_edge = lah.edge_map.parse_edge_map(line)

    def __del__(self):
        self.edge_map_f.close()

    def __iter__(self):
        return self

    def __next__(self):
        if not self.prev_edge:
            raise StopIteration()

        hid = self.prev_edge.hid
        edges = [ self.prev_edge ]
        self.prev_edge = None
        while True:
            line = self.edge_map_f.readline()
            if not line: # EOF
                break
            edge = lah.edge_map.parse_edge_map(line)
            if edge.hid != hid: # new haplotype, save edge, break to return haplotype
                self.prev_edge = edge
                break
            else: # add to edges
                edges.append(edge)

        if len(edges) > 0:
            return lah.haplotype.Haplotype.from_edges(edges=edges)
        else:
            raise StopIteration()

#-- HaplotypeReader

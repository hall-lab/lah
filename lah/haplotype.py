class Haplotype():
    def __init__(self, id, chr, start, stop, rids):
        self.id = id
        self.chr = chr
        self.start = start
        self.stop = stop
        self.length = self.stop - self.start
        self.rids = rids

    def from_edges(edges):
        hids = set()
        chr = edges[0].start[0]
        start = edges[0].start[1]
        stop = edges[0].stop[1]
        rids = set()
        for edge in edges:
            hids.add(edge.hid)
            rids.add(edge.rid)
            if edge.start[1] < start:
                start = edge.start[1]
            if edge.stop[1] > stop:
                stop = edge.stop[1]
        if len(hids) != 1:
            raise Exception("Multiple haplotypes in edges! {}".format(hids))
        return Haplotype(id=hids.pop(), chr=chr, start=start, stop=stop, rids=rids)

    def reads(self):
        rds = list(self.rids)
        rds.sort()
        return rds

#-- Haplotype

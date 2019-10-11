
class Haplotype():
    def __init__(self, edges):
        hids = set()
        self.chr = edges[0].start[0]
        self.start = edges[0].start[1]
        self.stop = edges[0].stop[1]
        self.rids = set()
        for edge in edges:
            hids.add(edge.hid)
            self.rids.add(edge.rid)
            if edge.start[1] < self.start:
                self.start = edge.start[1]
            if edge.stop[1] > self.stop:
                self.stop = edge.stop[1]
        if len(hids) != 1:
            raise Exception("Multiple haplotypes in edges! {}".format(hids))
        self.id = hids.pop()
        self.length = self.stop - self.start

    def reads(self):
        rds = list(self.rids)
        rds.sort()
        return rds

#-- Haplotype

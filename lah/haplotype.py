
class Haplotype():
    def __init__(self, edges):
        hids = set()
        self.chr = edges[0][2][0][0]
        self.start = edges[0][2][0][1]
        self.stop = edges[0][2][1][1]
        self.rids = set()
        for edge in edges:
            hids.add(edge[0])
            self.rids.add(edge[1])
            if edge[2][0][1] < self.start:
                self.start = edge[2][0][1]
            if edge[2][1][1] > self.stop:
                self.stop = edge[2][1][1]
        if len(hids) != 1:
            raise Exception("Multiple haplotypes in edges!")
        self.id = hids.pop()
        self.length = self.stop - self.start

    def reads(self):
        rds = list(self.rids)
        rds.sort()
        return rds

#-- Haplotype

import os, unittest

from .context import lah
import lah.edge_map, lah.haplotype

class LahHaplotypeTest(unittest.TestCase):
    def setUp(self):
        self.id = "3"
        self.chr = "chr1"
        self.start = 19338752
        self.stop = 19391199
        self.rids = ['m54238_180914_183539/11207193/ccs', 'm54238_180914_183539/11665587/ccs', 'm54238_180914_183539/17171007/ccs']

    def test1_haplotype(self):
        haplotype = lah.haplotype.Haplotype(id=self.id, chr=self.chr, start=self.start, stop=self.stop, rids=self.rids)
        self.assertIsNotNone(haplotype)

    def test2_haplotype_from_edges(self):
        edges = []
        edge_map_fn = os.path.join(os.path.dirname(__file__), "data", "lah_haplotype", "hap3.edge-map.tsv")
        with open(edge_map_fn, "r") as f:
            for line in f.readlines():
                line = line.rstrip()
                edges.append(lah.edge_map.parse_edge_map(line))
        hap = lah.haplotype.Haplotype.from_edges(edges=edges)

        self.assertEqual(hap.id, self.id)
        self.assertEqual(hap.chr, self.chr)
        self.assertEqual(hap.start, self.start)
        self.assertEqual(hap.stop, self.stop)
        self.assertEqual(hap.length, (self.stop - self.start))
        self.assertEqual(hap.reads(), self.rids)

# -- LahHaplotypeTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__

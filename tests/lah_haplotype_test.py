import os, unittest

from .context import lah
import lah.edge_map, lah.haplotype

class LahHaplotypeTest(unittest.TestCase):

    def test1_haplotype(self):
        edges = []
        edge_map_fn = os.path.join(os.path.dirname(__file__), "data", "lah_haplotype", "hap3.edge-map.tsv")
        with open(edge_map_fn, "r") as f:
            for line in f.readlines():
                line = line.rstrip()
                edges.append(lah.edge_map.parse_edge_map(line))
        hap = lah.haplotype.Haplotype(edges=edges)
        self.assertEqual(hap.id, "3")
        rds = ['m54238_180914_183539/11207193/ccs', 'm54238_180914_183539/11665587/ccs', 'm54238_180914_183539/17171007/ccs']
        self.assertEqual(hap.reads(), rds)
        self.assertEqual(hap.chr, "chr1")
        self.assertEqual(hap.start, 19338752)
        self.assertEqual(hap.stop, 19391199)
        self.assertEqual(hap.length, 52447)

# -- LahHaplotypeTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__

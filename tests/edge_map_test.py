import os, unittest

from .context import lah
import lah.edge_map

class LahEdgeMapTest(unittest.TestCase):

    def test1_parse_edge_map(self):
        edge_map = lah.edge_map.HaplotypeIterator.parse_edge_map("ccs_31_21627397 @m54329_180927_232921/21627397/ccs  401_0_1_0")
        self.assertEqual(edge_map["hid"], "401_0_1_0")
        self.assertEqual(edge_map["rid"], "m54329_180927_232921/21627397/ccs")

    def test2_haplotype_iterator(self):
        edge_map_fn = os.path.join(os.path.dirname(__file__), "data", "haplotype", "chr20.edge-map.tsv")
        haplotype_iter = lah.edge_map.HaplotypeIterator(edge_map_fn)
        self.assertIsNotNone(haplotype_iter)

        haplotypes = []
        for h in haplotype_iter:
            haplotypes.append(h)

        self.assertEqual(len(haplotypes), 4)
        self.assertEqual(haplotypes[0]["hid"], "401_0_1_0")
        self.assertEqual(len(haplotypes[0]["rids"]), 1)
        self.assertEqual(haplotypes[1]["hid"], "401_0_2_0")
        self.assertEqual(len(haplotypes[1]["rids"]), 2)
        self.assertEqual(haplotypes[2]["hid"], "402_0_1_0")
        self.assertEqual(len(haplotypes[2]["rids"]), 8)
        self.assertEqual(haplotypes[3]["hid"], "402_0_2_0")
        self.assertEqual(len(haplotypes[3]["rids"]), 14)


# -- LahEdgeMapTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__

import os, unittest

from .context import lah
import lah.edge_map, lah.haplotype

class LahHaplotypeTest(unittest.TestCase):
    def test1_haplotype(self):
        haplotype = lah.haplotype.Haplotype(id="3", rids=set(['m54238_180914_183539/11207193/ccs', 'm54238_180914_183539/11665587/ccs', 'm54238_180914_183539/17171007/ccs']))
        self.assertIsNotNone(haplotype)
        self.assertEqual(haplotype.id, "3")
        expected_reads = list(haplotype.rids)
        expected_reads.sort()
        self.assertEqual(haplotype.reads(), expected_reads)

    def test2_haplotype_iterator(self):
        edge_map_fn = os.path.join(os.path.dirname(__file__), "data", "haplotype", "chr20.edge-map.tsv")
        haplotype_iter = lah.haplotype.HaplotypeIterator(edge_map_fn)
        self.assertIsNotNone(haplotype_iter)

        haplotypes = []
        try:
            for h in haplotype_iter:
                haplotypes.append(h)
        except StopIteration:
            pass

        self.assertEqual(len(haplotypes), 4)

        self.assertEqual(haplotypes[0].id, "401_0_1_0")
        self.assertEqual(len(haplotypes[0].rids), 1)
        self.assertEqual(len(haplotypes[0].reads()), 1)
        self.assertEqual(haplotypes[1].id, "401_0_2_0")
        self.assertEqual(len(haplotypes[1].rids), 2)
        self.assertEqual(len(haplotypes[1].reads()), 2)
        self.assertEqual(haplotypes[2].id, "402_0_1_0")
        self.assertEqual(len(haplotypes[2].rids), 8)
        self.assertEqual(len(haplotypes[2].reads()), 8)
        self.assertEqual(haplotypes[3].id, "402_0_2_0")
        self.assertEqual(len(haplotypes[3].rids), 14)
        self.assertEqual(len(haplotypes[3].reads()), 14)

# -- LahHaplotypeTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
